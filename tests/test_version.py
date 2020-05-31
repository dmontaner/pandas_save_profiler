import pandas as pd
import pandas_save_profiler


def test_version():
    """Test that the version exists"""
    assert '__version__' in dir(pandas_save_profiler)


# def test_pandas_version():
#     assert pd.__version__ == '1.0.3'
