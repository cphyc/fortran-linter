import shutil
import tempfile
from pathlib import Path

import pytest

from fortran_linter.cli import main

HERE = Path(__name__).parent.absolute()


class TestAutoFixing:
    WDIR = None
    OWDIR = None
    TEST_FILE = None

    def setup(self):
        self.WDIR = tempfile.mkdtemp()
        orig_test_file = HERE / "tests" / "test.f90"
        shutil.copy2(orig_test_file, self.WDIR)
        self.TEST_FILE = Path(self.WDIR) / "test.f90"

    def test_fail_with_error(self):
        with pytest.raises(SystemExit):
            main([str(self.TEST_FILE), "--stdout"])

    def tearDown(self):
        pass
