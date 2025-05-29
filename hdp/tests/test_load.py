import pytest
from hdp.process.load import (
    clean_up,
    load_csv,
    load_json,
    load_xlsx,
    load_xls,
    load_gpx,
    load_tcx,
    load_jpg
)

def test_clean_up_no_exception():
    try:
        assert clean_up([]) is None
    except Exception as e:
        pytest.fail(f"Function raised an exception: {e}")

def test_load_csv_no_exception():
    try:
        assert load_csv([]) is None
    except Exception as e:
        pytest.fail(f"Function raised an exception: {e}")

def test_load_json_no_exception():
    try:
        assert load_json([]) is None
    except Exception as e:
        pytest.fail(f"Function raised an exception: {e}")

def test_load_xlsx_no_exception():
    try:
        assert load_xlsx([]) is None
    except Exception as e:
        pytest.fail(f"Function raised an exception: {e}")

def test_load_xls_no_exception():
    try:
        assert load_xls([]) is None
    except Exception as e:
        pytest.fail(f"Function raised an exception: {e}")

def test_load_gpx_no_exception():
    try:
        assert load_gpx([]) is None
    except Exception as e:
        pytest.fail(f"Function raised an exception: {e}")

def test_load_tcx_no_exception():
    try:
        assert load_tcx([]) is None
    except Exception as e:
        pytest.fail(f"Function raised an exception: {e}")

def test_load_jpg_no_exception():
    try:
        assert load_jpg([]) is None
    except Exception as e:
        pytest.fail(f"Function raised an exception: {e}")
