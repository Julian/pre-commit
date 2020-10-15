import pytest

import pre_commit.constants as C
from pre_commit.languages import lean
from pre_commit.prefix import Prefix


def test_healthy_global_lean(tmpdir):
    prefix = Prefix(str(tmpdir))
    assert lean.healthy(prefix, C.DEFAULT)
