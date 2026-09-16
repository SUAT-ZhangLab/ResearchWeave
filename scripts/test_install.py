"""Installer copies a working skill and preserves existing user files."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('researchweave_installer', ROOT/'install.py')
installer=importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)

class InstallTests(unittest.TestCase):
    def test_self_contained_install_and_repeat(self):
        with tempfile.TemporaryDirectory(prefix='researchweave-') as temp:
            dest=Path(temp)/'another agent space'/ 'researchweave'
            result=installer.install(dest)
            self.assertTrue(result['doctor']['success'])
            self.assertEqual(result['doctor']['project'],str(dest.resolve()))
            self.assertEqual(installer.install(dest)['status'],'already_installed')
            (dest/'user-note.txt').write_text('keep me')
            with self.assertRaises(ValueError):
                installer.install(dest)
            self.assertEqual((dest/'user-note.txt').read_text(),'keep me')

    def test_destination_must_not_overlap_source(self):
        for destination in [ROOT, ROOT/'nested-install', ROOT.parent]:
            with self.subTest(destination=destination), self.assertRaises(ValueError):
                installer.install(destination)

    def test_default_locations(self):
        self.assertEqual(installer.default_destination('codex'),Path.home()/'.agents/skills/researchweave')
        self.assertEqual(installer.default_destination('claude'),Path.home()/'.claude/skills/researchweave')

    def test_container_command_modes(self):
        import era_sandbox
        import os
        with patch.dict(os.environ,{'RESEARCHWEAVE_DOCKER_MODE':'native'}):
            self.assertEqual(era_sandbox.DockerSandbox()._command(['version']),['docker','version'])
        with patch.dict(os.environ,{'RESEARCHWEAVE_DOCKER_MODE':'wsl','RESEARCHWEAVE_WSL_DISTRO':'CustomDistro'}):
            command=era_sandbox.DockerSandbox()._command(['version'])
            self.assertEqual(command[0],'wsl.exe')
            self.assertEqual(command[2],'CustomDistro')
        with patch.dict(os.environ,{'RESEARCHWEAVE_DOCKER_MODE':'auto'}), patch.object(era_sandbox.shutil,'which',return_value='/usr/bin/docker'):
            self.assertEqual(era_sandbox.DockerSandbox()._command(['version']),['docker','version'])

if __name__=='__main__':
    unittest.main()
