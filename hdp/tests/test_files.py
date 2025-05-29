import pytest
from hdp.process.files import load_files

def test_load_files_no_exception_empty_list():
    try:
        assert load_files([]) is None
    except Exception as e:
        pytest.fail(f"Function raised an exception: {e}")

def test_load_files_no_exception_dummy_path():
    try:
        assert load_files(["dummy/path/file.csv"]) is None
    except Exception as e:
        pytest.fail(f"Function raised an exception: {e}")
