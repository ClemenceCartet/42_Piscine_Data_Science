import os
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from sklearn.preprocessing import StandardScaler
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
        x = train_knight.drop(columns='knight')
        scaler = StandardScaler()
        x = scaler.fit_transform(x)
        y = train_knight['knight']
        x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.2, random_state=42)

        model = KNeighborsClassifier(n_neighbors=9)
        model.fit(x_train, y_train)
        predicted_val = model.predict(x_val)
        accuracy = accuracy_score(y_val, predicted_val)
        print(f"Accuracy: {accuracy}")
        print(f"F1_score: {round(f1_score(y_val, predicted_val, average='macro'), 4)}")

        predicted_test = model.predict(test_knight)
        with open("Voting.txt", "w") as output:
            for item in predicted_test:
                output.write(item + "\n")

        acc_list = []
        for k in range(1, 30):
            model = KNeighborsClassifier(n_neighbors=k)
            model.fit(x_train, y_train)
            predicted_val = model.predict(x_val)
            acc_list.append(accuracy_score(y_val, predicted_val))

        plt.plot(acc_list)
        plt.xlabel("k values")
        plt.ylabel("accuracy")
        plt.show()


if __name__ == "__main__":
    main()
