import os
import sys
sys.path.insert(0, '../src')
import pytest
import pandas as pd
import pandas_save_profiler as savep
import tempfile
import sqlalchemy

print(pd.__version__)
print(pd.__file__)

rep = 1
slp = 0.1

tmp_dir = tempfile.TemporaryDirectory()

formats = [
    'to_pickle',
    'to_parquet',
    'to_feather',
    'to_csv',
    # 'to_excel',
]


@pytest.fixture
def data():
    data = pd.util.testing.makeMissingDataframe()
    data = data.rename_axis('text').reset_index()
    data = data.rename_axis('integer').reset_index()
    data['date'] = pd.util.testing.makeDateIndex(data.shape[0])
    data['bool'] = pd.util.testing.makeBoolIndex(data.shape[0]).values.astype(bool)
    return data


if hasattr(sys, 'ps1'):  # interactive mode
    data = data.__wrapped__()


@pytest.mark.parametrize('fmt,', formats)
def test_save_profiler(data, fmt):
    res = savep.save_profiler(data, fmt, repeats=rep, sleep_time=slp)
    assert res['writer'] == fmt


@pytest.mark.parametrize('fmt,', formats)
def test_df_save_profiler(data, fmt):
    res = data.save_profiler(fmt, repeats=rep, sleep_time=slp)
    assert res['writer'] == fmt


def test_param_read_back(data):
    assert data.save_profiler('to_csv'   , repeats=rep, sleep_time=slp)['reads_the_same'] is False
    assert data.save_profiler('to_pickle', repeats=rep, sleep_time=slp)['reads_the_same'] is True
    assert data.save_profiler('to_pickle', repeats=rep, sleep_time=slp, reader=None)['reads_the_same'] is None
    assert data.save_profiler('to_pickle', repeats=rep, sleep_time=slp, test_read_back=False)['reads_the_same'] is None


def test_write_read_arguments(data):
    assert savep.save_profiler(
        data, repeats=rep, sleep_time=slp,
        writer='to_csv',
        reader='read_csv',
        writer_args={'index': False},
        reader_args={'parse_dates': ['date']},
    )['reads_the_same'] is True

    assert savep.save_profiler(
        data, repeats=rep, sleep_time=slp,
        writer='to_csv',
        reader='read_csv',
        index=False,
        parse_dates=['date'],
    )['reads_the_same'] is True

    assert savep.save_profiler(
        data, repeats=rep, sleep_time=slp,
        writer='to_pickle',
        index=False,
        parse_dates=['date'],
    )['reads_the_same'] is True


def test_sql(data):
    '''SQL is still an edge case because the first parameter is the table name instead of the file path'''
    engine = sqlalchemy.create_engine('sqlite://')
    assert data.save_profiler('to_sql', repeats=rep, sleep_time=slp, con=engine)['reads_the_same'] is False
    assert data.save_profiler('to_sql', repeats=rep, sleep_time=slp, con=engine, index=False)['reads_the_same'] is True
    assert data.save_profiler('to_sql', repeats=rep, sleep_time=slp, con=engine, index=False, keep=True, path='mytable1')['reads_the_same'] is True
    assert data.save_profiler('to_sql', repeats=2  , sleep_time=slp, con=engine, index=False, keep=True, path='mytable2', if_exists='replace')['reads_the_same'] is True


def test_excel(data):
    # assert data.save_profiler('to_sql', repeats=rep, sleep_time=slp, con=engine)['reads_the_same'] is False
    data.save_profiler('to_excel', repeats=rep, sleep_time=slp, path=os.path.join(tmp_dir.name, 'test_excel.xls'))
    data.save_profiler('to_excel', repeats=rep, sleep_time=slp, path=os.path.join(tmp_dir.name, 'test_excel.xlsx'))
    # data.save_profiler('to_excel', repeats=rep, sleep_time=slp, engine='openpyxl')
    # data.save_profiler('to_excel', repeats=rep, sleep_time=slp, engine='openpyxl')


def test_concatenate(data):
    engine = sqlalchemy.create_engine('sqlite://')

    res = pd.DataFrame([
        data.save_profiler('to_csv'    , repeats=rep, sleep_time=slp),
        data.save_profiler('to_pickle' , repeats=rep, sleep_time=slp),
        data.save_profiler('to_parquet', repeats=rep, sleep_time=slp),
        data.save_profiler('to_excel'  , repeats=rep, sleep_time=slp, path=os.path.join(tmp_dir.name, 'test_excel.xls')),
        data.save_profiler('to_sql'    , repeats=rep, sleep_time=slp, con=engine),
    ])

    assert res.shape[0] == 5
    assert all(res['df_memory'] == data.memory_usage().sum())
