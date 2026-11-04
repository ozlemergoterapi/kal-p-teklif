"""Display tessellation and sampled axial accessibility; never manufacturing approval."""
import contextlib
import json
import sys
import numpy as np

def load(filename):
    from OCP.STEPControl import STEPControl_Reader
    from OCP.IFSelect import IFSelect_RetDone
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopAbs import TopAbs_SOLID
    from OCP.TopoDS import TopoDS, TopoDS_Compound
    from OCP.BRep import BRep_Builder
    from OCP.BRepCheck import BRepCheck_Analyzer
    r=STEPControl_Reader()
    if r.ReadFile(filename)!=IFSelect_RetDone or not r.TransferRoots():
        raise ValueError('STEP dosyası okunamadı.')
    compound=TopoDS_Compound();builder=BRep_Builder();builder.MakeCompound(compound)
    exp=TopExp_Explorer(r.OneShape(),TopAbs_SOLID);count=0
    while exp.More():
        solid=TopoDS.Solid_s(exp.Current())
        if not BRepCheck_Analyzer(solid).IsValid():
            raise ValueError('Geçersiz katı görüntüleme için kabul edilmedi.')
        builder.Add(compound,solid);count+=1;exp.Next()
    if not count:raise ValueError('Kapalı katı bulunamadı.')
    return compound,count

def sample_accessibility(vertices,triangles,face_ids,faces,minimum,maximum):
    tri=vertices[triangles];centers=tri.mean(axis=1)
    crosses=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);areas=np.linalg.norm(crosses,axis=1)/2
    normals=crosses/np.maximum(2*areas[:,None],1e-15)
    epsilon=max(float(np.max(maximum-minimum))*1e-5,1e-4)
    points=[];owners=[]
    # Up to 8 spatially dispersed triangle samples per face; still finite sampling.
    for f in faces:
        ids=np.where(face_ids==f['id'])[0]
        pool=ids[np.argsort(areas[ids])[-64:]]
        selected=[int(pool[-1])]
        while len(selected)<min(8,len(pool)):
            distance=np.min(np.sum((centers[pool,None,:]-centers[selected][None,:,:])**2,axis=2),axis=1)
            choice=int(pool[int(np.argmax(distance))])
            if choice in selected:break
            selected.append(choice)
        for i in selected:
            points.append(centers[i]+normals[i]*epsilon);owners.append(f['id'])
    points=np.asarray(points);owners=np.asarray(owners);blocked=[]
    for axis in range(3):
        uv=[i for i in range(3) if i!=axis];a=tri[:,0][:,uv];b=tri[:,1][:,uv];c=tri[:,2][:,uv]
        lo=tri[:,:,uv].min(axis=1);hi=tri[:,:,uv].max(axis=1)
        v0=b-a;v1=c-a;det=v0[:,0]*v1[:,1]-v0[:,1]*v1[:,0]
        valid=np.abs(det)>1e-12
        grid={};bins=24;extent=np.maximum(maximum[uv]-minimum[uv],1e-9)
        cell_lo=np.clip(((lo-minimum[uv])/extent*bins).astype(int),0,bins-1);cell_hi=np.clip(((hi-minimum[uv])/extent*bins).astype(int),0,bins-1)
        for t in np.flatnonzero(valid):
            for x in range(cell_lo[t,0],cell_hi[t,0]+1):
                for y in range(cell_lo[t,1],cell_hi[t,1]+1):grid.setdefault((x,y),[]).append(t)
        grid={k:np.asarray(v,dtype=int) for k,v in grid.items()}
        flags=[]
        for p in points:
            cell=tuple(np.clip(((p[uv]-minimum[uv])/extent*bins).astype(int),0,bins-1));pool=grid.get(cell,np.array([],dtype=int))
            ids=pool[np.all(lo[pool]<=p[uv]+1e-9,axis=1)&np.all(hi[pool]>=p[uv]-1e-9,axis=1)]
            if not len(ids):flags.append([False,False]);continue
            delta=p[uv]-a[ids];u=(delta[:,0]*v1[ids,1]-delta[:,1]*v1[ids,0])/det[ids]
            v=(v0[ids,0]*delta[:,1]-v0[ids,1]*delta[:,0])/det[ids]
            inside=(u>=-1e-8)&(v>=-1e-8)&(u+v<=1+1e-8)
            depth=tri[ids,0,axis]+u*(tri[ids,1,axis]-tri[ids,0,axis])+v*(tri[ids,2,axis]-tri[ids,0,axis])
            flags.append([bool(np.any(inside&(depth>p[axis]+epsilon/10))),bool(np.any(inside&(depth<p[axis]-epsilon/10)))])
        blocked.append(np.asarray(flags))
    # Face adjacency from shared tessellation vertices, independent of face numbering.
    vertex_faces={};adjacency={f['id']:set() for f in faces}
    for vertex,face in zip(triangles,face_ids):
        for point in vertices[vertex]:vertex_faces.setdefault(tuple(np.round(point,6)),set()).add(int(face))
    for group in vertex_faces.values():
        for face in group:adjacency[face].update(group-{face})
    result=[]
    for axis,letter in enumerate('XYZ'):
        ids=[];groups={};profiles=[]
        for f in faces:
            indices=np.flatnonzero(owners==f['id'])
            occluded=np.all(blocked[axis][indices],axis=1)
            face_tri=np.flatnonzero(face_ids==f['id'])
            angles=np.degrees(np.arcsin(np.clip(np.abs(normals[face_tri,axis]),0,1)))
            profiles.append(dict(faceId=f['id'],sampleCount=len(indices),bothBlocked=int(np.sum(occluded)),plusBlocked=int(np.sum(blocked[axis][indices,0])),minusBlocked=int(np.sum(blocked[axis][indices,1])),minimumDraftDegrees=float(np.min(angles)),nearParallelArea=float(np.sum(areas[face_tri][angles<.5]))))
            if not np.any(occluded):continue
            ids.append(f['id'])
            choices=[]
            for lateral in range(3):
                if lateral==axis:continue
                for sign in [1,-1]:
                    free=int(np.sum(~blocked[lateral][indices,0 if sign==1 else 1]))
                    choices.append((free,lateral,sign))
            choices.sort(reverse=True);free,lateral,sign=choices[0]
            key=('XYZ'[lateral]+('+' if sign==1 else '-')) if free else 'review'
            groups.setdefault(key,[]).append(f)
        regions=[]
        for key,items in groups.items():
            remaining={f['id'] for f in items};byid={f['id']:f for f in items}
            while remaining:
                queue=[remaining.pop()];component=[]
                while queue:
                    current=queue.pop();component.append(byid[current]);neighbors=remaining&adjacency[current];remaining-=neighbors;queue.extend(neighbors)
                mn=np.min([f['min'] for f in component],axis=0);mx=np.max([f['max'] for f in component],axis=0)
                regions.append(dict(direction=key,faceIds=[f['id'] for f in component],min=mn.tolist(),max=mx.tolist(),reason='Bağlantılı yüz grubunda iki açılma yönünde de örneklenmiş engel bulundu.'))
        total=sum(f['area'] for f in faces)
        area=sum(f['area'] for f in faces if f['id'] in ids)
        result.append(dict(axis=letter,candidateFaceIds=ids,areaRatio=area/max(total,1e-12),regions=regions,profiles=profiles,nearParallelArea=sum(p['nearParallelArea'] for p in profiles),requiresReview=True))
    return dict(method='spatial-axis-rays-v2',recommendedAxis=min(result,key=lambda r:r['areaRatio'])['axis'],axes=result,sampleCount=len(points),limitations='Yalnız X/Y/Z ve yüz başına en çok 8 uzamsal örnek. Bağlantılı bölgeler ayrılır; 0,5° altı yüzeyler inceleme için raporlanır, zorunlu tasarım kuralı değildir. Sıfır aday, maçasız üretim kanıtı değildir. Soğutma, çekme açısı, itici, yolluk, çarpışma ve dayanım doğrulanmadı.')

def tessellate(filename):
    from OCP.BRepMesh import BRepMesh_IncrementalMesh
    from OCP.BRepTools import BRepTools
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopAbs import TopAbs_FACE,TopAbs_REVERSED
    from OCP.TopoDS import TopoDS
    from OCP.BRep import BRep_Tool
    from OCP.TopLoc import TopLoc_Location
    from OCP.BRepAdaptor import BRepAdaptor_Surface
    from OCP.Bnd import Bnd_Box
    from OCP.BRepBndLib import BRepBndLib
    from OCP.GProp import GProp_GProps
    from OCP.BRepGProp import BRepGProp
    shape,solids=load(filename);box=Bnd_Box();BRepBndLib.AddOptimal_s(shape,box)
    x0,y0,z0,x1,y1,z1=box.Get();minimum=np.array([x0,y0,z0]);maximum=np.array([x1,y1,z1])
    tolerance=max(float(np.max(maximum-minimum))/700,.05)
    for attempt in range(5):
        if attempt:BRepTools.Clean_s(shape)
        BRepMesh_IncrementalMesh(shape,tolerance,False,.35,True)
        vertices=[];triangles=[];face_ids=[];faces=[];exp=TopExp_Explorer(shape,TopAbs_FACE)
        while exp.More():
            face=TopoDS.Face_s(exp.Current());loc=TopLoc_Location();mesh=BRep_Tool.Triangulation_s(face,loc)
            if mesh is not None:
                offset=len(vertices);points=[]
                for i in range(1,mesh.NbNodes()+1):
                    p=mesh.Node(i).Transformed(loc.Transformation());points.append([p.X(),p.Y(),p.Z()])
                points=np.asarray(points);indices=[]
                for i in range(1,mesh.NbTriangles()+1):
                    a,b,c=mesh.Triangle(i).Get();indices.append([a-1,c-1,b-1] if face.Orientation()==TopAbs_REVERSED else [a-1,b-1,c-1])
                indices=np.asarray(indices,dtype=int)
                if len(indices):
                    tris=points[indices];cross=np.cross(tris[:,1]-tris[:,0],tris[:,2]-tris[:,0]);areas=np.linalg.norm(cross,axis=1)/2;keep=areas>1e-12;indices=indices[keep];cross=cross[keep];areas=areas[keep]
                    if len(indices):
                        identifier=len(faces);normal=cross.sum(axis=0)
                        if np.linalg.norm(normal)<1e-8:normal=cross[int(np.argmax(areas))]
                        normal/=max(np.linalg.norm(normal),1e-15)
                        faces.append(dict(id=identifier,type=str(BRepAdaptor_Surface(face).GetType()).split('.')[-1],area=float(areas.sum()),center=np.average(points[indices].mean(axis=1),axis=0,weights=areas).tolist(),normal=normal.tolist(),min=points.min(axis=0).tolist(),max=points.max(axis=0).tolist()))
                        vertices.extend(points.tolist());triangles.extend((indices+offset).tolist());face_ids.extend([identifier]*len(indices))
            exp.Next()
        if len(triangles)<=100000:break
        tolerance*=2
    if not triangles or len(triangles)>100000 or len(faces)>3000:raise ValueError('Görüntüleme ayrıntı sınırı aşıldı; sadeleştirilmiş STEP kullanın.')
    vertices=np.asarray(vertices);triangles=np.asarray(triangles);face_ids=np.asarray(face_ids)
    props=GProp_GProps();BRepGProp.VolumeProperties_s(shape,props)
    suggestions=sample_accessibility(vertices,triangles,face_ids,faces,minimum,maximum)
    return dict(version='step-mesh-v1',units='mm',solids=solids,volume=props.Mass(),min=minimum.tolist(),max=maximum.tolist(),positions=np.round(vertices,6).ravel().tolist(),triangles=triangles.ravel().tolist(),faceIds=face_ids.tolist(),faces=faces,suggestions=suggestions,tolerance=tolerance)

if __name__=='__main__':
    try:
        with contextlib.redirect_stdout(sys.stderr):result=tessellate(sys.argv[1])
        print(json.dumps(result,allow_nan=False,separators=(',',':')))
    except Exception as error:
        print(json.dumps({'error':str(error)}));sys.exit(1)
