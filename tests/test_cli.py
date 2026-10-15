import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class AevyCliTests(unittest.TestCase):
    def run_cli(self, *args):
        env = os.environ.copy()
        env["PYTHONPATH"] = str(PROJECT_ROOT / "src")
        return subprocess.run(
            [sys.executable, "-m", "aevy", *map(str, args)],
            cwd=PROJECT_ROOT,
            env=env,
            text=True,
            capture_output=True,
            timeout=10,
        )

    def test_runs_source_file(self):
        with tempfile.TemporaryDirectory() as directory:
            source_file = Path(directory) / "hello.aevy"
            source_file.write_text('show("Hello from Aevy")\n', encoding="utf-8")
            result = self.run_cli(source_file)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "Hello from Aevy")

    def test_reports_runtime_error_without_python_traceback(self):
        with tempfile.TemporaryDirectory() as directory:
            source_file = Path(directory) / "bad.aevy"
            source_file.write_text('show(missing)\n', encoding="utf-8")
            result = self.run_cli(source_file)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Name error: Undefined variable 'missing'", result.stderr)
        self.assertNotIn("Traceback (most recent call last)", result.stderr)

    def test_missing_file_returns_nonzero(self):
        result = self.run_cli("this-file-does-not-exist.aevy")
        self.assertEqual(result.returncode, 2)
        self.assertIn("cannot read", result.stderr)

    def test_bundled_example_runs(self):
        result = self.run_cli(PROJECT_ROOT / "examples" / "hello.aevy")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Hello, Aevy", result.stdout)
        self.assertIn("4", result.stdout.splitlines())

    def test_no_argument_runs_demo(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("1500", result.stdout)


if __name__ == "__main__":
    unittest.main()
