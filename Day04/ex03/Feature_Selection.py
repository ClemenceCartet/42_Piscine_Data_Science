import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def load(path: str):
    """Load a data file using pandas library"""
    try:
        assert isinstance(path, str), "your path is not valid."
        assert os.path.exists(path), "your file doesn't exist."
        assert os.path.isfile(path), "your 'file' is not a file."
        assert path.lower().endswith(".csv"), "file format is not .csv."
        data = pd.read_csv(path)
        print(f"Loading dataset of dimensions {data.shape}")
        return data
    except AssertionError as msg:
        print(f"{msg.__class__.__name__}: {msg}")
        return None


def standardize(data):
    for col in data.columns:
        if not pd.api.types.is_string_dtype(data[col]):
            data[col] = (
                data[col].subtract(data[col].mean()).divide(data[col].std())
            )


def main():
    """Main function"""
    data = load("Test_knight.csv")
    # data.drop(columns="knight", inplace=True)
    if data is not None:
        data_var = data.var()


        # plt.show()


if __name__ == "__main__":
    main()
