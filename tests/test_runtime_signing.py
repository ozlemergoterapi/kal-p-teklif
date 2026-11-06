import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('runtime_signing', Path(__file__).resolve().parents[1]/'scripts/sign-macos-runtime.py')
signing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(signing)

class RuntimeSigningTests(unittest.TestCase):
    def test_relocated_executable_and_dylib_signed_but_symlinks_and_data_skipped(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for name in ['python','libpython.dylib']:
                (root/name).write_bytes(bytes.fromhex('cffaedfe')+b'relocated prefix')
            (root/'data.json').write_text('{}')
            with patch.object(signing.subprocess,'run') as run:
                signing.sign_runtime(root)
            self.assertEqual(run.call_count,4)
            self.assertEqual(sum('--verify' in c.args[0] for c in run.call_args_list),2)
            self.assertTrue(all(c.kwargs['check'] for c in run.call_args_list))
    def test_bad_signature_stops_packaging(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory)/'python').write_bytes(bytes.fromhex('cffaedfe')+b'relocated prefix')
            with patch.object(signing.subprocess,'run',side_effect=subprocess.CalledProcessError(1,['codesign'],stderr='bad signature')):
                with self.assertRaises(subprocess.CalledProcessError):signing.sign_runtime(directory)
