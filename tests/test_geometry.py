import importlib.util
import tempfile
import unittest
from pathlib import Path
import numpy as np
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCP.gp import gp_Trsf, gp_Ax1, gp_Pnt, gp_Dir, gp_Vec
spec=importlib.util.spec_from_file_location('geometry',Path(__file__).resolve().parents[1]/'scripts/geometry.py')
geometry=importlib.util.module_from_spec(spec)
spec.loader.exec_module(geometry)
def write(shape,filename):
 writer=STEPControl_Writer();writer.Transfer(shape,STEPControl_AsIs);writer.Write(str(filename))
class GeometryTests(unittest.TestCase):
 def test_rotated_renamed_export(self):
  with tempfile.TemporaryDirectory() as folder:
   shape=BRepPrimAPI_MakeBox(10,20,30).Shape()
   rotate=gp_Trsf();rotate.SetRotation(gp_Ax1(gp_Pnt(0,0,0),gp_Dir(1,2,3)),.82)
   move=gp_Trsf();move.SetTranslation(gp_Vec(100,-200,500))
   transformed=BRepBuilderAPI_Transform(BRepBuilderAPI_Transform(shape,rotate,True).Shape(),move,True).Shape()
   first=Path(folder)/'original.step';second=Path(folder)/'different-name.step'
   write(shape,first);write(transformed,second)
   a,b=geometry.analyze(str(first)),geometry.analyze(str(second))
   self.assertNotEqual(first.read_bytes(),second.read_bytes())
   for k in ['volume','area']:self.assertAlmostEqual(a[k],b[k],places=5)
   np.testing.assert_allclose(a['inertia'],b['inertia'],rtol=1e-7)
 def test_invalid_file(self):
  with tempfile.TemporaryDirectory() as folder:
   p=Path(folder)/'bad.step';p.write_text('not a STEP file')
   with self.assertRaises(ValueError):geometry.analyze(str(p))
if __name__=='__main__':unittest.main()
