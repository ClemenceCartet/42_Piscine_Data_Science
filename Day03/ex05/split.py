import os
import pandas as pd

# import numpy as np
from sklearn.model_selection import train_test_split


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


def main():
    """Main function"""
    data = load("Train_knight.csv")
    if data is not None:
        # shuffled = data.sample(frac=1)  # mix all lines
        # result = np.array_split(shuffled, 2)
        x_train, x_val, y_train, y_val = train_test_split(
            data.iloc[:, :-1],
            data.iloc[:, -1:],
            test_size=0.2,
            random_state=42,
        )
        training = pd.concat(
            [x_train.reset_index(drop=True), y_train.reset_index(drop=True)],
            axis=1,
        )
        validation = pd.concat(
            [x_val.reset_index(drop=True), y_val.reset_index(drop=True)],
            axis=1,
        )
        training.to_csv("Training_knight.csv", index=False)
        validation.to_csv("Validation_knight.csv", index=False)


if __name__ == "__main__":
    main()
