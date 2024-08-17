"""This file is used for storing and loading panda dataframes."""

import os

import pandas as pd


DATAFRAME_STORE = os.path.join(".", "Data")
os.makedirs(DATAFRAME_STORE, exist_ok=True)


#####################################################################################################################################################
def store_dataframe(data: pd.DataFrame, name_dataset: str) -> None:
    """This function is used to store data in pickle.

    Args:
        data (pd.DataFrame): The dataframe that should be stored.
        name_dataset (str): The name that should be used to store the data.
    """
    data.to_pickle(os.path.join(DATAFRAME_STORE, f"{name_dataset}.pkl"))


#####################################################################################################################################################
def load_dataframe(name_dataset: str) -> pd.DataFrame:
    """Load data from file.

    Args:
        name_dataset (str): Name of the dataframe that should be used.

    Returns:
        pd.DataFrame: The loaded dataframe.
    """
    if not name_dataset.endswith(".pkl"):
        name_dataset = f"{name_dataset}.pkl"
    return pd.read_pickle(os.path.join(DATAFRAME_STORE, name_dataset))


#####################################################################################################################################################
def list_dataframes() -> list[str]:
    """List all dataframe files.

    Returns:
        list[str]: A list of all dataframe files in DATAFRAME_STORE.
    """
    return os.listdir(DATAFRAME_STORE)


#####################################################################################################################################################
def remove_dataframe(name_dataset: str) -> None:
    """Remove the dataset from the stored files.

    Args:
        name_dataset (str): Name of the dataset that should be deleted.
    """
    file_path = os.path.join(DATAFRAME_STORE, f"{name_dataset}.pkl")
    if os.path.exists(file_path):
        os.remove(file_path)
