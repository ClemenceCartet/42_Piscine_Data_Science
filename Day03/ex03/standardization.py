import os
import pandas as pd
import matplotlib.pyplot as plt

# from sklearn.preprocessing import StandardScaler


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
        print(data.head(2))
        for col in data.columns:
            if not pd.api.types.is_string_dtype(data[col]):
                data[col] = (
                    data[col]
                    .subtract(data[col].mean())
                    .divide(data[col].std())
                )
        print(data.head(2))

        # scaler = StandardScaler()
        # scaler.fit(test_knight)
        # # print(scaler.scale_)
        # standard_data = scaler.transform(test_knight)
        # print(standard_data)
        grouped = data.groupby("knight")
        jedi_data = grouped.get_group("Jedi")
        sith_data = grouped.get_group("Sith")
        js, jp = jedi_data["Sensitivity"], jedi_data["Power"]
        ss, sp = sith_data["Sensitivity"], sith_data["Power"]
        plt.scatter(js, jp, color="blue", s=30, alpha=0.4, edgecolors="white")
        plt.scatter(ss, sp, color="red", s=30, alpha=0.4, edgecolors="white")
        plt.xlabel("Sensitivity")
        plt.ylabel("Power")
        plt.legend(labels=("Jedi", "Sith"))
        plt.show()


if __name__ == "__main__":
    main()
