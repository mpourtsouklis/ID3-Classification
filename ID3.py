import time
from ID3Node import Node
import math
import os


class ID3:
    # Constructor
    def __init__(self):
        self.negativeVectors = []
        self.positiveVectors = []
        self.vocabulary = []
        self.root = None

    # Main functions
    def train(self, negativePath, positivePath, vocabularyPath):
        timeStart = time.time()

        # Convert vectors' files to arrays
        self.negativeVectors = self.getVectors(negativePath)
        self.positiveVectors = self.getVectors(positivePath)
        # Convert vocabulary's file to array
        self.vocabulary = self.getVocabulary(vocabularyPath)

        timeEnd = time.time()

        print("Trained ID3 algorithm in {:.2f} seconds.".format(
            ((timeEnd - timeStart))))

    def build(self):
        timeStart = time.time()

        # Built ID3 decision tree
        self.root = self.id3(self.negativeVectors,
                             self.positiveVectors, self.vocabulary)

        timeEnd = time.time()

        print("Built ID3 decision tree in {:.2f} seconds.".format(
            ((timeEnd - timeStart))))

    def classify(self, testsPath, resultsPath="."):
        timeStart = time.time()

        # Convert test data file to array
        vectors = self.getVectors(testsPath)

        results = []  # Results from classification

        for vector in vectors:
            # Start from ID3's tree root
            node = self.root

            # While current node is not an answer
            while ((node != True) and (node != False)):
                # If vector is 0
                if (vector[self.vocabulary.index(node.getWord())] == 0):
                    # Go to current node's negative node
                    node = node.getFalseNode()

                else:
                    # Else, go to current node's positive node
                    node = node.getTrueNode()

            # If answer is positive
            if (node == True):
                # Add positive answer to results
                results.append("Positive")

            else:
                # Else, add negative answer to results
                results.append("Negative")

        # Create the converted file
        filename = "{}/results.txt".format(resultsPath)

        with open(filename, "w", encoding='utf-8') as text:
            # Write each result in the file
            for result in results:
                text.write(result + "\n")

        timeEnd = time.time()

        print("Classified data in {:.2f} seconds.".format(
            ((timeEnd - timeStart))))

    # Side functions
    def getVectors(self, path):

        with open(path, 'r', encoding="utf-8") as text:

            rows = text.read().split("\n")

            vectors = []

            for row in rows:

                if (row != ""):

                    words = row.split(" ")

                    vector = []

                    for word in words:
                        if (word != ""):

                            vector.append(int(word))

                    vectors.append(vector)

        return vectors

    def getVocabulary(self, vocabularyPath):

        with open(vocabularyPath, 'r', encoding="utf-8") as text:

            rows = text.read().split("\n")

            vocabulary = []

            for row in rows:
                if (row != ""):

                    vocabulary.append(row)

        return vocabulary

    def id3(self, negativeExamples, positiveExamples, properties, default=None):
        # If there are no more examples
        if ((not negativeExamples) and (not positiveExamples)):
            # Return default category
            return default
        # Else, if all examples are positive
        elif (not negativeExamples):
            # Return positive answer
            return True
        # Else, if all examples are negative
        elif (not positiveExamples):
            # Return negative answer
            return False
        # Else, if there are no more properties
        elif (not properties):
            # Return the more frequent category of the examples
            return self.moreFrequent(positiveExamples, negativeExamples)
        # Else,
        else:
            # Find the best property based on information gain
            best = self.getBest(properties, negativeExamples, positiveExamples)

            # Create new tree with the best property as root
            tree = Node(properties[best])

            # Find the most frequent category of the examples
            frequentCategory = self.moreFrequent(
                positiveExamples, negativeExamples)

            # For each possible answer of the property
            for value in [0, 1]:
                # Negative examples = {negative examples|best property = answer}
                negExamples = []
                for example in negativeExamples:
                    if (example[best] == value):
                        negExamples.append(example[:best]+example[best+1:])

                # Positive examples = {positive examples|best property = answer}
                posExamples = []
                for example in positiveExamples:
                    if (example[best] == value):
                        posExamples.append(example[:best]+example[best+1:])

                # Sub-tree = ID3(negative examples, positive examples, properties, most frequent category)
                subtree = self.id3(negExamples, posExamples,
                                   (properties[:best]+properties[best+1:]), frequentCategory)

                # If answer is negative
                if (value == 0):
                    # Set sub-tree as the tree root's negative node
                    tree.setFalseNode(subtree)
                else:
                    # Else, set sub-tree as the tree root's positive node
                    tree.setTrueNode(subtree)

            # Return decision tree
            return tree

    def moreFrequent(self, aList, bList):
        # If possitive examples are more
        if (len(aList) >= len(bList)):
            # Return positive answer
            return True
        # Else, return negative answer
        return False

    def getBest(self, properties, negativeExamples, positiveExamples):
        # Calculate information gain of each word
        IGs = self.getInfoGains(properties, negativeExamples, positiveExamples)

        return IGs.index(max(IGs))

    def getInfoGains(self, vocabulary, negativeExamples, positiveExamples):
        # Information gains
        IGs = []

        # All negative examples
        negativeAll = len(negativeExamples)
        # All positive examples
        positiveAll = len(positiveExamples)

        # Calculate P(C=1)
        probability = positiveAll / (positiveAll + negativeAll)
        # Calculate H(C)
        entropy = self.getEntropy(probability)

        # For each word in the vocabulary
        for word in range(len(vocabulary)):
            # Negative examples that include the word
            negativeWith = 0

            for example in negativeExamples:
                if (example[word] == 1):
                    negativeWith += 1

            # Positive examples that do not include the word
            positiveWithout = 0
            # Positive examples that include the word
            positiveWith = 0

            for example in positiveExamples:
                if (example[word] == 0):
                    positiveWithout += 1
                else:
                    positiveWith += 1

            # Calculate P(W=word)
            probability = (negativeWith + positiveWith) / \
                (negativeAll + positiveAll)

            # Calculate P(C=1|W!=word)
            probabilityWithout = positiveWithout / positiveAll

            # Calculate H(C|W!=word)
            entropyWithout = self.getEntropy(probabilityWithout)

            # Calculate P(C=1|W=word)
            probabilityWith = positiveWith / positiveAll

            # Calculate H(C|W=word)
            entropyWith = self.getEntropy(probabilityWith)

            # Calculate word's information gain
            IGs.append(entropy - (probability * entropyWith) -
                       ((1 - probability) * entropyWithout))

        return IGs

    def getEntropy(self, probability):
        if ((probability == 0) or (probability == 1)):
            return 0

        return (-(probability * math.log(probability, 2)) - ((1-probability) * math.log(1-probability, 2)))
