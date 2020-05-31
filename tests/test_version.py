import pandas_save_profiler

# import pandas as pd
# def test_pandas_version():
#     assert pd.__version__ == '1.0.3'


def test_version():
    """Test that the version exists"""
    assert '__version__' in dir(pandas_save_profiler)
