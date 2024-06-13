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
    train_knight = load("Train_knight.csv")
    if test_knight is not None and train_knight is not None:
        grouped = train_knight.groupby("knight")
        jedi_data = grouped.get_group('Jedi')
        sith_data = grouped.get_group('Sith')
        jf = jedi_data.get(["Survival"])
        jp = jedi_data.get(["Deflection"])
        sf = sith_data.get(["Survival"])
        sp = sith_data.get(["Deflection"])

        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 8))
        # axes[0, 1].scatter(jf, range(len(jf)), color="blue", label="Jedi", s=30, alpha=0.4, edgecolors='white')
        # axes[0, 1].scatter(sf, range(len(sf)), color="red", label="Sith", s=30, alpha=0.4, edgecolors='white')
        axes[0, 1].scatter(jf, jp, color="blue", s=30, alpha=0.4, edgecolors='white')
        axes[0, 1].scatter(sf, sp, color="red", s=30, alpha=0.4, edgecolors='white')
        axes[0, 1].set_xlabel("Friendship")
        axes[0, 1].set_ylabel("Power")
        axes[0, 1].legend(labels=('Jedi','Sith'))
        plt.show()


if __name__ == "__main__":
    main()
