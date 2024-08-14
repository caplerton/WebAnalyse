import os
import pandas as pd

from plot_page.data.global_variables import DATAFRAME_STORE


# , data_table: pd.DataFrame
# def check_query(query: str) -> tuple[str]:

#     splitted_query

#     compare_split = comparison.split(" ")
#     if len(compare_split) != 2:
#         return None
#     compare_operator, compare_value = compare_split
#     if compare_operator not in ["<", "<=", ">", ">=", "=", "!="]:
#         return None
#     return (attribute, compare_operator, compare_value)


def query_table(selected_table: str, queries: list[str]) -> pd.DataFrame:
    data_table = pd.read_pickle(os.path.join(DATAFRAME_STORE, f"{selected_table}.pkl"))
    for query in queries:
        try:
            tmp_result = data_table.query(query)
            data_table = tmp_result
        except Exception:
            pass
    return data_table
