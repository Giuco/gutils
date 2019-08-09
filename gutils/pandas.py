from typing import Optional, List, Dict, Any

import pandas as pd
import numpy as np
from IPython.core.display import display
from pandas.core.dtypes.common import is_datetime64_any_dtype, is_string_dtype

MB = (1024 ** 2)


def display_all(df: pd.DataFrame):
    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        display(df)


def add_date_parts_to_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    attrs = ['year', 'month', 'week', 'day', 'dayofweek', 'dayofyear', 'is_month_end',
             'is_month_start', 'is_quarter_end', 'is_quarter_start', 'is_year_end', 'is_year_start']

    df = df.copy()
    for attr in attrs:
        df[f"{column}_{attr}"] = getattr(df[column].dt, attr)

    return df


def add_date_parts(df: pd.DataFrame, columns: Optional[List[str]] = None, drop=False) -> pd.DataFrame:
    df = df.copy()

    if not columns:
        columns = [c for c in list(df.columns) if is_datetime64_any_dtype(df[c])]

    for column in columns:
        df = add_date_parts_to_column(df, column)

    if drop:
        df = df.drop(columns, axis=1)

    return df


def transform_columns_to_categorical(df: pd.DataFrame, ordered: Dict = None) -> pd.DataFrame:
    if not ordered:
        ordered = {}

    df = df.copy()

    for n, c in df.items():
        if is_string_dtype(c):
            df[n] = c.astype('category').cat.as_ordered()

            if n in ordered:
                df[n] = df[n].cat.set_categories(ordered[n], ordered=True)

    return df


def separate_features_by_dtype(df: pd.DataFrame) -> Dict[str, List[str]]:
    dtypes_df = pd.DataFrame(df.dtypes).reset_index().rename(columns={0: "dtype"})
    dtypes_df["dtype"] = dtypes_df["dtype"].map(str)
    return dtypes_df.groupby("dtype")["index"].apply(list).to_dict()


def reduce_df_mem_usage(df: pd.DataFrame, deep=False):
    """
    Reduces the amount of memory used by the DataFrame

    :param df: The DataFrame to be reduced
    :param deep: If you want to show deep memory usage or not
    :return:
    """
    start_mem_usage = df.memory_usage(deep=deep).sum() / MB
    print(f"DataFrame memory usage {int(start_mem_usage)} MB")

    for column in df.columns:
        correct_dtype = find_best_dtype(df[column])
        df[column] = df[column].astype(correct_dtype)

    end_mem_usage = df.memory_usage(deep=deep).sum() / MB
    print(f"DataFrame memory usage after completion {int(end_mem_usage)} MB")
    print(f"{int((end_mem_usage / start_mem_usage) * 100)}% memory usage reduction")


def find_best_dtype(col: pd.Series) -> Any:
    col_type = col.dtype

    if col_type == object:
        return object

    col_min = col.min()
    col_max = col.max()

    if str(col_type)[:3] == "int":
        if col_min > np.iinfo(np.int8).min and col_max < np.iinfo(np.int8).max:
            best_dtype = np.int8
        elif col_min > np.iinfo(np.int16).min and col_max < np.iinfo(np.int16).max:
            best_dtype = np.int16
        elif col_min > np.iinfo(np.int32).min and col_max < np.iinfo(np.int32).max:
            best_dtype = np.int32
        elif col_min > np.iinfo(np.int64).min and col_max < np.iinfo(np.int64).max:
            best_dtype = np.int64
    else:
        if col_min > np.finfo(np.float16).min and col_max < np.finfo(np.float16).max:
            best_dtype = np.float16
        elif col_min > np.finfo(np.float32).min and col_max < np.finfo(np.float32).max:
            best_dtype = np.float32
        else:
            best_dtype = np.float64

    return best_dtype
