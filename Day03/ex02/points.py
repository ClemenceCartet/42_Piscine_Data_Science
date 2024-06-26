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
    train_knight = load("Train_knight.csv")
    test_knight = load("Test_knight.csv")
    if train_knight is not None and test_knight is not None:
        grouped = train_knight.groupby("knight")
        jedi_data = grouped.get_group("Jedi")
        sith_data = grouped.get_group("Sith")
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 8))

        features: list[tuple] = [
            ("Sensitivity", "Power"),
            ("Burst", "Hability"),
        ]

        for i, trait in enumerate(features):
            js, jp = jedi_data[trait[0]], jedi_data[trait[1]]
            ss, sp = sith_data[trait[0]], sith_data[trait[1]]
            ks, kp = test_knight[trait[0]], test_knight[trait[1]]
            axes[0, i].scatter(
                js, jp, color="blue", s=30, alpha=0.4, edgecolors="white"
            )
            axes[0, i].scatter(
                ss, sp, color="red", s=30, alpha=0.4, edgecolors="white"
            )
            axes[0, i].set_xlabel(trait[0])
            axes[0, i].set_ylabel(trait[1])
            axes[0, i].legend(labels=("Jedi", "Sith"))

            axes[1, i].scatter(
                ks, kp, color="green", s=30, alpha=0.4, edgecolors="white"
            )
            axes[1, i].set_xlabel(trait[0])
            axes[1, i].set_ylabel(trait[1])
            axes[1, i].legend(labels=("Knight",))

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    main()
