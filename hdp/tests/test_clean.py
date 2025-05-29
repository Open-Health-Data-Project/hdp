import pytest
from hdp.process.clean import convert_time, convert_date, convert_units, clean_data

def test_convert_time_no_exception():
    try:
        assert convert_time("10:00:00", "%H:%M:%S", "some_mode") is None
    except Exception as e:
        pytest.fail(f"Function raised an exception: {e}")

def test_convert_date_no_exception():
    try:
        assert convert_date("2023-10-26", "%Y-%m-%d", "some_mode") is None
    except Exception as e:
        pytest.fail(f"Function raised an exception: {e}")

def test_convert_units_no_exception():
    try:
        assert convert_units([]) is None
    except Exception as e:
        pytest.fail(f"Function raised an exception: {e}")

def test_clean_data_no_exception():
    try:
        assert clean_data([], [], {}, []) is None
    except Exception as e:
        pytest.fail(f"Function raised an exception: {e}")
