import sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from cad_convert import convert
class CADConvertTests(unittest.TestCase):
    def test_iges_solid_conversion(self):
        from OCP.IGESControl import IGESControl_Writer
        from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
        from mesh import tessellate
        with tempfile.TemporaryDirectory() as d:
            source=Path(d)/'part.igs';target=Path(d)/'part.step';w=IGESControl_Writer('MM',1);w.AddShape(BRepPrimAPI_MakeBox(10,20,30).Shape());w.Write(str(source));convert(source,target);self.assertEqual(tessellate(str(target))['solids'],1)
