import os
import pandas as pd


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
    train_knight = load("Train_knight.csv")
    if train_knight is not None:
        train_knight = train_knight.replace({'knight': 'Jedi'}, 1)
        train_knight = train_knight.replace({'knight': 'Sith'}, 0)
        res = train_knight.corr()['knight'].sort_values(ascending=False)
        print(res)


if __name__ == "__main__":
    main()
