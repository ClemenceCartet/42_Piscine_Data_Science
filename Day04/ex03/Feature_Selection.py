import os
import pandas as pd
from sklearn.linear_model import LinearRegression


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


def train_to_find_vif(data):
    features = data.columns
    vif_dict: dict = {}
    for feature in features:
        y = data[feature]
        x = data.drop(columns=feature)
        model = LinearRegression().fit(x, y)
        r_squared = model.score(x, y)
        tolerance = round((1 - r_squared), 6)
        vif = round((1 / tolerance), 6)
        vif_dict[feature] = (vif, tolerance)

    df = pd.DataFrame.from_dict(vif_dict, orient="index")
    df.columns = ["VIF", "Tolerance"]

    return df


def main():
    """Main function"""
    data = load("Test_knight.csv")
    if data is not None:
        all_features = train_to_find_vif(data)
        all_features_sorted = all_features.sort_values(
            by="VIF", ascending=False
        )
        print(all_features_sorted)

        # test1 = data.drop(
        #     columns=[
        #         "Slash",
        #         "Pull",
        #         "Sensitivity",
        #         "Recovery",
        #         "Awareness",
        #         "Prescience",
        #         "Delay",
        #         "Dexterity",
        #         "Empowered",
        #         "Attunement",
        #     ]
        # )
        # all_features = train_to_find_vif(test1)
        # all_features_sorted = all_features.sort_values(by="VIF", ascending=False)
        # print(all_features_sorted)

        test2 = data.drop(
            columns=[
                "Prescience",
                "Push",
                "Deflection",
                "Survival",
                "Midi-chlorien",
                "Grasping",
                "Pull",
                "Awareness",
                "Repulse",
                "Attunement",
                "Empowered",
                "Dexterity",
                "Delay",
                "Slash",
                "Sprint",
                "Sensitivity",
                "Stims",
                "Strength",
                "Recovery",
                "Hability",
                "Agility",
            ]
        )
        all_features = train_to_find_vif(test2)
        all_features_sorted = all_features.sort_values(
            by="VIF", ascending=False
        )
        print(all_features_sorted)


if __name__ == "__main__":
    main()
