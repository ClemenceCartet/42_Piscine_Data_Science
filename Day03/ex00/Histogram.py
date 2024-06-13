import os
import pandas as pd
import matplotlib.pyplot as plt


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
    test_knight = load("Test_knight.csv")
    if test_knight is not None:
        test_knight.hist(figsize=(17, 17), grid=False, color='g')
        plt.show()

    train_knight = load("Train_knight.csv")
    if train_knight is not None:
        grouped = train_knight.groupby("knight")
        jedi_data = grouped.get_group('Jedi')
        sith_data = grouped.get_group('Sith')
        axes = jedi_data.hist(figsize=(17, 17), alpha=0.5, label='Jedi', color='b')
        sith_data.hist(ax=axes.ravel(), figsize=(17, 17), alpha=0.5, label='Sith', color='r')
        # plt.legend(labels=('Jedi','Sith'))
        plt.show()


if __name__ == "__main__":
    main()
