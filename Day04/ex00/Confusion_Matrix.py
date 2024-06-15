import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def preprocess_data(data):
    new_data = []
    for elmt in data:
        if elmt == "Sith":
            new_data.append(0)
        else:
            new_data.append(1)

    return new_data


def main():
    """Main function"""
    pred = preprocess_data(np.loadtxt("predictions.txt", dtype=str))
    truth = preprocess_data(np.loadtxt("truth.txt", dtype=str))

    tn, fn, fp, tp = 0, 0, 0, 0
    for i in range(len(truth)):
        if pred[i] == 0 and truth[i] == 0:
            tn += 1
        elif pred[i] == 0 and truth[i] == 1:
            fn += 1
        elif pred[i] == 1 and truth[i] == 0:
            fp += 1
        elif pred[i] == 1 and truth[i] == 1:
            tp += 1

    matrix_confusion = [[tp, fn], [fp, tn]]

    jedi_precision = round(tp / (tp + fp), 2)
    jedi_recall = round(tp / (tp + fn), 2)
    jedi_f1_score = round(
        2 * ((jedi_precision * jedi_recall) / (jedi_precision + jedi_recall)),
        2,
    )

    sith_precision = round(tn / (tn + fn), 2)
    sith_recall = round(tn / (tn + fp), 2)
    sith_f1_score = round(
        2 * ((sith_precision * sith_recall) / (sith_precision + sith_recall)),
        2,
    )

    accuracy = (tn + tp) / len(truth)

    print(
        f"Jedi: {jedi_precision=}, {jedi_recall=}, {jedi_f1_score=}, total={truth.count(1)}"
    )
    print(
        f"Sith: {sith_precision=}, {sith_recall=}, {sith_f1_score=}, total={truth.count(0)}"
    )
    print(f"{accuracy=}")
    print(matrix_confusion[0])
    print(matrix_confusion[1])
    sns.heatmap(matrix_confusion, annot=True)
    plt.show()


if __name__ == "__main__":
    main()
