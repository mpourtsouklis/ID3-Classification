class Validator:
    def __init__(self):
        self.total = 0
        self.TN = 0
        self.FN = 0
        self.TP = 0
        self.FP = 0

    def check(self, resultsPath, expectedResult):
        with open(resultsPath, 'r', encoding="utf-8") as text:
            results = text.read().split("\n")

        if (expectedResult == "Negative"):
            for result in results:
                if (result != ""):
                    if (result == expectedResult):
                        self.TN += 1
                    else:
                        self.FP += 1
        else:
            for result in results:
                if (result != ""):
                    if (result == expectedResult):
                        self.TP += 1
                    else:
                        self.FN += 1

    def validate(self):
        accuracy = ((self.TP + self.TN) / (self.TP +
                    self.TN + self.FP + self.FN)) * 100
        precision = (self.TP / (self.TP + self.FP)) * 100
        recall = (self.TP / (self.TP + self.FN)) * 100
        f1 = 2 * ((precision * recall) / (precision + recall)) * 100

        print("Accuracy = {:.2f}%".format(accuracy))
        print("Precision = {:.2f}%".format(precision))
        print("Recall = {:.2f}%".format(recall))
        print("F1 = {:.2f}%".format(f1))

        return accuracy, precision, recall, f1
