import importlib.util
import tempfile
import unittest
from pathlib import Path
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox,BRepPrimAPI_MakeCylinder
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.STEPControl import STEPControl_Writer,STEPControl_AsIs
from OCP.gp import gp_Ax2,gp_Pnt,gp_Dir
spec=importlib.util.spec_from_file_location('mesh',Path(__file__).resolve().parents[1]/'scripts/mesh.py');mesh=importlib.util.module_from_spec(spec);spec.loader.exec_module(mesh)
class MeshTests(unittest.TestCase):
 def export(self,shape,path):
  w=STEPControl_Writer();w.Transfer(shape,STEPControl_AsIs);w.Write(str(path))
 def test_box_mesh_and_sampled_opening(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'box.step';self.export(BRepPrimAPI_MakeBox(10,20,30).Shape(),p);m=mesh.tessellate(str(p));self.assertEqual(m['version'],'step-mesh-v1');self.assertEqual(len(m['faceIds']),len(m['triangles'])//3);self.assertTrue(len(m['triangles'])>0);self.assertEqual(m['solids'],1);self.assertEqual(m['suggestions']['method'],'spatial-axis-rays-v2');self.assertTrue(all(a['profiles'] for a in m['suggestions']['axes']));self.assertTrue(all(not a['candidateFaceIds'] for a in m['suggestions']['axes']))
 def test_transverse_hole_generates_candidate_regions(self):
  with tempfile.TemporaryDirectory() as d:
   box=BRepPrimAPI_MakeBox(10,20,30).Shape();hole=BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(-1,10,15),gp_Dir(1,0,0)),3,12).Shape();shape=BRepAlgoAPI_Cut(box,hole).Shape();p=Path(d)/'hole.step';self.export(shape,p);m=mesh.tessellate(str(p));axes={a['axis']:a for a in m['suggestions']['axes']};self.assertTrue(axes['Z']['candidateFaceIds']);self.assertEqual(len(axes['X']['candidateFaceIds']),0)
if __name__=='__main__':unittest.main()
