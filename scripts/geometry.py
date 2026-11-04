"""STEP solid signature for retrieval, not proof of shape equality or tooling design."""
import contextlib
import json
import sys


def analyze(filename):
    import numpy as np
    from OCP.STEPControl import STEPControl_Reader
    from OCP.IFSelect import IFSelect_RetDone
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopAbs import TopAbs_SOLID
    from OCP.TopoDS import TopoDS, TopoDS_Compound
    from OCP.BRep import BRep_Builder
    from OCP.BRepCheck import BRepCheck_Analyzer
    from OCP.BRepGProp import BRepGProp
    from OCP.GProp import GProp_GProps
    from OCP.Bnd import Bnd_Box
    from OCP.BRepBndLib import BRepBndLib

    reader = STEPControl_Reader()
    if reader.ReadFile(filename) != IFSelect_RetDone:
        raise ValueError('STEP dosyası okunamadı.')
    if not reader.TransferRoots():
        raise ValueError('STEP geometrisi aktarılamadı.')
    explorer = TopExp_Explorer(reader.OneShape(), TopAbs_SOLID)
    compound = TopoDS_Compound()
    builder = BRep_Builder()
    builder.MakeCompound(compound)
    count = 0
    while explorer.More():
        solid = TopoDS.Solid_s(explorer.Current())
        if not BRepCheck_Analyzer(solid).IsValid():
            raise ValueError('Geçersiz katı geometri; imza oluşturulmadı.')
        builder.Add(compound, solid)
        count += 1
        explorer.Next()
    if not count:
        raise ValueError('Karşılaştırılabilir kapalı katı bulunamadı.')
    mass, surface = GProp_GProps(), GProp_GProps()
    BRepGProp.VolumeProperties_s(compound, mass)
    BRepGProp.SurfaceProperties_s(compound, surface)
    matrix = mass.MatrixOfInertia()
    inertia = sorted(float(v) for v in np.linalg.eigvalsh([[matrix.Value(i, j) for j in range(1, 4)] for i in range(1, 4)]))
    bbox = Bnd_Box()
    BRepBndLib.AddOptimal_s(compound, bbox)
    x0, y0, z0, x1, y1, z1 = bbox.Get()
    result = dict(version='solid-invariants-v1', units='mm', solids=count,
                  volume=mass.Mass(), area=surface.Mass(), inertia=inertia,
                  bounds=[x1-x0, y1-y0, z1-z0])
    if not all(np.isfinite(v) and v > 0 for v in [result['volume'], result['area'], *inertia, *result['bounds']]):
        raise ValueError('Geometri özellikleri hesaplanamadı.')
    return result

if __name__ == '__main__':
    try:
        with contextlib.redirect_stdout(sys.stderr):
            result = analyze(sys.argv[1])
        print(json.dumps(result, allow_nan=False))
    except Exception:
        print(json.dumps({'error': 'Geçerli bir STEP katısı analiz edilemedi.'}))
        sys.exit(1)
