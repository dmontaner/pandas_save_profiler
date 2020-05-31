# Pandas Save Profiler

`pandas_save_profiler` helps you evaluating and comparing the performance of different pandas read and write methods.

## Install

    pip install pandas-save-profiler

## Usage

Load pandas and a dataframe you want to save.

    import pandas as pd
    data = pd.util.testing.makeMissingDataframe()

Load `pandas_save_profiler` and use it to evaluate pandas performance saving a _pickle_ file:

    import pandas_save_profiler
    data.save_profiler('to_pickle')

The output is a pandas series:

```
format                                                 pickle
writer                                              to_pickle
reader                                            read_pickle
writer_args                      {'path': '/tmp/tmppk7nkivk'}
reader_args        {'filepath_or_buffer': '/tmp/tmppk7nkivk'}
writer_time                                         0.0798338
reader_time                                         0.0294895
writer_memory                                     1.09087e+08
reader_memory                                     1.09118e+08
df_memory                                                 288
file_size                                                1122
writer_memory_h                                      109.1 MB
reader_memory_h                                      109.1 MB
df_memory_h                                         288 Bytes
file_size_h                                            1.1 kB
repeats                                                     5
reads_the_same                                           True
dtype: object
```

Values in the series indicate:

- The __format__ used to persist the dataframe and the writing and reading options.
- Writing and reading __times__ in seconds.
- Writing and reading __memory__ increment.
- Size of the dataframe in memory.
- __Size__ of the saved file.

Memory values are in __bytes__ but a "humanized" version is also reported.
The saving and reloading process is __repeated__ 5 times and average values are returned.
The flag `reads_the_same` indicates whether the reloaded file is exactly the same as the original one or has some differences.


To __compare several writing options__ you can use the `save_profiler` function on each of them
and combine the results into a results dataframe:

```
pd.DataFrame([
    data.save_profiler('to_csv'),
    data.save_profiler('to_pickle'),
    data.save_profiler('to_parquet'),
])

```

returns:

```
    format      writer        reader                          writer_args  \
0      csv      to_csv      read_csv  {'path_or_buf': '/tmp/tmpsedehjob'}   
1   pickle   to_pickle   read_pickle         {'path': '/tmp/tmp_vhue2q7'}   
2  parquet  to_parquet  read_parquet         {'path': '/tmp/tmp0zn8qsnk'}   

                                  reader_args  writer_time  reader_time  \
0  {'filepath_or_buffer': '/tmp/tmpsedehjob'}     0.031842     0.039830   
1  {'filepath_or_buffer': '/tmp/tmp_vhue2q7'}     0.025705     0.028469   
2                {'path': '/tmp/tmp0zn8qsnk'}     0.039009     0.052447   

   writer_memory  reader_memory  df_memory  file_size writer_memory_h  \
0    110149632.0    110599372.8        288        139        110.1 MB   
1    110813184.0    110813184.0        288       1122        110.8 MB   
2    116892467.2    118014771.2        288       3449        116.9 MB   

  reader_memory_h df_memory_h file_size_h  repeats  reads_the_same  
0        110.6 MB   288 Bytes   139 Bytes        5           False  
1        110.8 MB   288 Bytes      1.1 kB        5            True  
2        118.0 MB   288 Bytes      3.4 kB        5            True  
```
