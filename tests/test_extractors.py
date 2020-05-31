import sys
sys.path.insert(0, '../src')
sys.path.insert(0, 'src')
import pytest
import pandas as pd
from pandas_save_profiler import extractors as ext

pd_major_version = pd.__version__.split('.')[0]

formats2paths = {
    '0': [
        # format    writer          reader
        ('pickle' , 'path'        , 'path'),
        ('parquet', 'fname'       , 'path'),
        ('feather', 'fname'       , 'path'),
        ('csv'    , 'path_or_buf' , 'filepath_or_buffer'),
        ('excel'  , 'excel_writer', 'io'),
    ],
    '1': [
        # format    writer          reader
        ('pickle' , 'path'        , 'filepath_or_buffer'),
        ('parquet', 'path'        , 'path'),
        ('feather', 'path'        , 'path'),
        ('csv'    , 'path_or_buf' , 'filepath_or_buffer'),
        ('excel'  , 'excel_writer', 'io'),
    ],
}


@pytest.mark.parametrize('fmt,w,r', formats2paths[pd_major_version])
def test_extract_writer_path_argument(fmt, w, r):
    assert w == ext.extract_writer_path_argument('to_' + fmt)
    assert r == ext.extract_reader_path_argument('read_' + fmt)
