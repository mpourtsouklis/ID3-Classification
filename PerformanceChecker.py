from Data import Data
from ID3 import ID3
from Validator import Validator
from tabulate import tabulate
import matplotlib.pyplot as plt


class PerformanceChecker:
    def __init__(self, m, n, k):
        self.m = m
        self.n = n
        self.k = k

        self.dataNumbers = []
        self.accuracies = []
        self.precisions = []
        self.recalls = []
        self.F1s = []

    def checkTrain(self, start=500, end=12500, step=3000):
        for dataNumber in range(start, end+1, step):
            self.dataNumbers.append(dataNumber)

            dataset = Data()
            dataset.load("aclImdb/train/neg", "aclImdb/train/pos", dataNumber)
            dataset.filter(self.m, self.n, self.k)
            dataset.convertTrain("aclImdb/train/neg", 0, "vectors")
            dataset.convertTrain("aclImdb/train/pos", 1, "vectors")

            id3 = ID3()
            id3.train("vectors/negative.txt", "vectors/positive.txt",
                      "vocabulary.txt")
            id3.build()

            validator = Validator()

            dataset.convertTest("aclImdb/train/pos", "vectors", dataNumber)
            id3.classify("vectors/test.txt")
            validator.check("results.txt", "Positive")

            dataset.convertTest("aclImdb/train/neg", "vectors", dataNumber)
            id3.classify("vectors/test.txt")
            validator.check("results.txt", "Negative")

            accuracy, precision, recall, f1 = validator.validate()

            self.accuracies.append(accuracy)
            self.precisions.append(precision)
            self.recalls.append(recall)
            self.F1s.append(f1)

        table = []
        for i in range(len(self.dataNumbers)):
            table.append([self.dataNumbers[i], self.accuracies[i],
                         self.precisions[i], self.recalls[i], self.F1s[i]])

        print(tabulate(table, ["Data", "Accuracy",
              "Precision", "Recall", "F1"], "fancy_grid"))

        fig = plt.figure()
        fig.suptitle("ID3")

        plt.subplot(2, 2, 1)
        plt.plot(self.dataNumbers, self.accuracies)
        plt.xlabel("training data")
        plt.ylabel("accuracy (%)")

        plt.subplot(2, 2, 2)
        plt.plot(self.dataNumbers, self.precisions)
        plt.xlabel("training data")
        plt.ylabel("precision (%)")

        plt.subplot(2, 2, 3)
        plt.plot(self.dataNumbers, self.recalls)
        plt.xlabel("training data")
        plt.ylabel("recall (%)")

        plt.subplot(2, 2, 4)
        plt.plot(self.dataNumbers, self.F1s)
        plt.xlabel("training data")
        plt.ylabel("F1 (%)")

        plt.show()

    def checkTest(self, start=500, end=12500, step=3000):
        for dataNumber in range(start, end+1, step):
            self.dataNumbers.append(dataNumber)

            dataset = Data()
            dataset.load("aclImdb/train/neg", "aclImdb/train/pos", dataNumber)
            dataset.filter(self.m, self.n, self.k)
            dataset.convertTrain("aclImdb/train/neg", 0, "vectors")
            dataset.convertTrain("aclImdb/train/pos", 1, "vectors")

            id3 = ID3()
            id3.train("vectors/negative.txt", "vectors/positive.txt",
                      "vocabulary.txt")
            id3.build()

            validator = Validator()

            dataset.convertTest("aclImdb/test/pos", "vectors")
            id3.classify("vectors/test.txt")
            validator.check("results.txt", "Positive")

            dataset.convertTest("aclImdb/test/neg", "vectors")
            id3.classify("vectors/test.txt")
            validator.check("results.txt", "Negative")

            accuracy, precision, recall, f1 = validator.validate()

            self.accuracies.append(accuracy)
            self.precisions.append(precision)
            self.recalls.append(recall)
            self.F1s.append(f1)

        table = []
        for i in range(len(self.dataNumbers)):
            table.append([self.dataNumbers[i], self.accuracies[i],
                         self.precisions[i], self.recalls[i], self.F1s[i]])

        print(tabulate(table, ["Data", "Accuracy",
              "Precision", "Recall", "F1"], "fancy_grid"))

        fig = plt.figure()
        fig.suptitle("ID3")

        plt.subplot(2, 2, 1)
        plt.plot(self.dataNumbers, self.accuracies)
        plt.xlabel("training data")
        plt.ylabel("accuracy (%)")

        plt.subplot(2, 2, 2)
        plt.plot(self.dataNumbers, self.precisions)
        plt.xlabel("training data")
        plt.ylabel("precision (%)")

        plt.subplot(2, 2, 3)
        plt.plot(self.dataNumbers, self.recalls)
        plt.xlabel("training data")
        plt.ylabel("recall (%)")

        plt.subplot(2, 2, 4)
        plt.plot(self.dataNumbers, self.F1s)
        plt.xlabel("training data")
        plt.ylabel("F1 (%)")

        plt.show()
