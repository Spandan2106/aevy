import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from aevy.__main__ import run, run_file
from aevy.interpreter import Interpreter
from aevy.lexer import Lexer
from aevy.parser import Parser


class ModuleAndFileIOTests(unittest.TestCase):
    def test_import_executes_module_and_exposes_function(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "helpers.aevy").write_text(
                'func double(n) {\n    return n * 2\n}\nshow("module loaded")\n',
                encoding="utf-8",
            )
            main = 'import "helpers.aevy"\nshow(double(21))\n'
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                run(main, base_dir=root)
            self.assertEqual(output.getvalue().splitlines(), ["module loaded", "42"])

    def test_import_is_only_executed_once(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "once.aevy").write_text('show("once")\n', encoding="utf-8")
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                run('import "once.aevy"\nimport "once.aevy"\n', base_dir=root)
            self.assertEqual(output.getvalue().splitlines(), ["once"])

    def test_circular_import_reports_error(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a.aevy").write_text('import "b.aevy"\n', encoding="utf-8")
            (root / "b.aevy").write_text('import "a.aevy"\n', encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "Circular module import"):
                run('import "a.aevy"\n', base_dir=root)

    def test_import_cannot_escape_project_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "project"
            root.mkdir()
            outside = Path(directory) / "outside.aevy"
            outside.write_text('show("no")\n', encoding="utf-8")
            with self.assertRaisesRegex(PermissionError, "stay inside"):
                run('import "../outside.aevy"\n', base_dir=root)

    def test_text_file_builtins(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = '''
write_text("notes.txt", "hello")
append_text("notes.txt", " world")
show(file_exists("notes.txt"))
show(read_text("notes.txt"))
'''
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                run(source, base_dir=root)
            self.assertEqual(output.getvalue().splitlines(), ["True", "hello world"])
            self.assertEqual((root / "notes.txt").read_text(encoding="utf-8"), "hello world")

    def test_file_paths_cannot_escape_project_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "project"
            root.mkdir()
            with self.assertRaisesRegex(PermissionError, "stay inside"):
                run('write_text("../unsafe.txt", "x")\n', base_dir=root)

    def test_file_builtin_argument_validation(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(TypeError, "must be text"):
                run('read_text(123)\n', base_dir=directory)

    def test_missing_import_is_clear_runtime_error(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(RuntimeError, "Cannot import module"):
                run('import "missing.aevy"\n', base_dir=directory)

    def test_import_requires_quoted_aevy_path(self):
        with self.assertRaisesRegex(SyntaxError, "quoted module path"):
            Parser(Lexer('import helper\n').scan_tokens()).parse()
        with self.assertRaisesRegex(SyntaxError, "must end with .aevy"):
            Parser(Lexer('import "helper.txt"\n').scan_tokens()).parse()


    def test_imported_syntax_error_shows_module_source_line(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "broken.aevy").write_text('show("ok")\n@\n', encoding="utf-8")
            with self.assertRaises(SyntaxError) as caught:
                run('import "broken.aevy"\n', base_dir=root)
            self.assertEqual(getattr(caught.exception, "aevy_source", None), 'show("ok")\n@\n')

    def test_cli_file_io_and_import_work_together(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "helper.aevy").write_text('func answer() {\n    return 42\n}\n', encoding="utf-8")
            (root / "main.aevy").write_text(
                'import "helper.aevy"\nwrite_text("result.txt", text(answer()))\nshow(read_text("result.txt"))\n',
                encoding="utf-8",
            )
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                code = run_file(root / "main.aevy")
            self.assertEqual(code, 0)
            self.assertEqual(output.getvalue().strip(), "42")


if __name__ == "__main__":
    unittest.main()
