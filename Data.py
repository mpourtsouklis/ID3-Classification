# Imports
import time
import os
import math


class Data:
    # Constructor
    def __init__(self):
        # Dictionary storing words and array with their appearances [neg,pos] in data
        self.words = {}
        self.maxData = None  # Number of train data

# Main functions
    def load(self, negativePath, positivePath, maxData=None):
        self.maxData = maxData
        timeStart = time.time()

        dataUsed = 0  # Number of negative train data loaded

        # For each text in the negative folder
        for text in os.listdir(negativePath):
            # If reached max number of train data
            if (dataUsed == self.maxData):
                # Stop loading negative data
                break

            # Else, increase number of train data loaded
            dataUsed += 1
            # Read text
            with open(os.path.join(negativePath, text), 'r', encoding="utf-8") as text:
                # Split text to words
                words = text.read().split(" ")

                checkedWords = []  # Words checked in this text

                # For every word
                for word in words:
                    # Remove punctuation marks & capitalize
                    rawWord = word.strip(".,:;?()[]'!-</>").upper()
                    # If it was not included in this text before
                    if rawWord not in checkedWords:
                        # If it was not included in any text before
                        if rawWord not in self.words.keys():
                            # Add it to included words with 1 negative appearance
                            self.words[rawWord] = [1, 0]
                        else:
                            # Else, increase its negative appearances
                            self.words[rawWord][0] += 1

                        # Add it to this text's checked words
                        checkedWords.append(rawWord)

        timeEnd = time.time()

        print("Loaded {} negative data in {:.2f} seconds.".format(
            dataUsed, ((timeEnd - timeStart))))

        dataUsed = 0  # Number of positive train data loaded

        timeStart = time.time()

        # For each text in the positive folder
        for text in os.listdir(positivePath):

            # If reached max number of train data
            if (dataUsed == self.maxData):
                # Stop loading positive data
                break

            # Else, increase number of train data loaded
            dataUsed += 1
            # Read text
            with open(os.path.join(positivePath, text), 'r', encoding="utf-8") as text:
                # Split text to words
                words = text.read().split(" ")

                checkedWords = []  # Words checked in this text

                # For every word
                for word in words:
                    # Remove punctuation marks & capitalize
                    rawWord = word.strip(".,:;?()[]'!-</>").upper()
                    # If it was not included in this text before
                    if rawWord not in checkedWords:
                        # If it was not included in any text before
                        if rawWord not in self.words.keys():
                            # Add it to included words with 1 positive appearance
                            self.words[rawWord] = [0, 1]
                        else:
                            # Else, increase its positive appearances
                            self.words[rawWord][1] += 1

                        # Add it to this text's checked words
                        checkedWords.append(rawWord)

        timeEnd = time.time()

        print("Loaded {} positive data in {:.2f} seconds.".format(
            dataUsed, ((timeEnd - timeStart))))

    def filter(self, m, n, k, vocabularyPath="."):
        timeStart = time.time()

        # If words are less than (m), after removing (n) more frequent and (k) less frequent words
        if ((len(self.words) - n - k) < m):
            # Return error
            return False

        # Sort words by appearances in descending order
        self.words = dict(
            sorted(self.words.items(), key=lambda x: (x[1][0] + x[1][1]), reverse=True))

        # Remove (n) more frequent words
        for i in range(n):
            self.words.pop(next(iter(self.words)))

        # Remove (k) less frequent words
        for i in range(k):
            self.words.popitem()

        # Remove all except (m) more frequent words
        for i in range(len(self.words) - m):
            self.words.popitem()

        # Create text including the vocabulary
        textname = "{}/vocabulary.txt".format(vocabularyPath)

        with open(textname, "w", encoding='utf-8') as text:
            # For each word in the vocabulary
            for word in self.words.keys():
                # Write it
                text.write(word + "\n")

        timeEnd = time.time()

        print("Filtered vocabulary in {:.2f} seconds.".format(
            ((timeEnd - timeStart))))

        return True

    def convertTrain(self, importPath, result, exportPath="."):
        timeStart = time.time()

        vectors = []
        # For each text in the folder
        for text in os.listdir(importPath):
            # If reached max number of train data
            if (len(vectors) == self.maxData):
                # Stop converting
                break

            vector = {}

            for word in self.words.keys():
                vector[word] = 0

            # Read text
            with open(os.path.join(importPath, text), 'r', encoding="utf-8") as text:
                # Split text to words
                words = text.read().split(" ")

                checkedWords = []  # Words checked in this text

                # For every word
                for word in words:
                    # Remove punctuation marks & capitalize
                    rawWord = word.strip(".,:;?()[]'!-</>").upper()

                    # If it was not included in this text before
                    if rawWord not in checkedWords:
                        # If it is included in the dictionary
                        if rawWord in self.words.keys():
                            # Set its vector to 1
                            vector[rawWord] = 1

                        # Add it to this text's checked words
                        checkedWords.append(rawWord)

                vectors.append(vector)

        # Create the converted text
        textname = "{}/{}.txt".format(exportPath,
                                      "positive" if result else "negative")

        with open(textname, "w", encoding='utf-8') as text:
            # For each text
            for vector in vectors:
                # For each word in the dictionary
                for word in vector:
                    # Write if included
                    text.write(str(vector[word]) + " ")
                # Write the result
                text.write("\n")

        timeEnd = time.time()
        print("Converted {} {} train data in {:.2f} seconds.".format(
            len(vectors), "positive" if result else "negative", ((timeEnd - timeStart))))

    def convertTest(self, importPath, exportPath=".", maxData=None):
        timeStart = time.time()

        vectors = []

        # For each text in the folder
        for text in os.listdir(importPath):
            # If reached max number of data
            if (len(vectors) == maxData):
                # Stop converting
                break

            vector = {}

            for word in self.words.keys():
                vector[word] = 0

            # Read text
            with open(os.path.join(importPath, text), 'r', encoding="utf-8") as text:
                # Split text to words
                words = text.read().split(" ")

                checkedWords = []  # Words checked in this text

                # For every word
                for word in words:
                    # Remove punctuation marks & capitalize
                    rawWord = word.strip(".,:;?()[]'!-</>").upper()

                    # If it was not included in this text before
                    if rawWord not in checkedWords:
                        # If it is included in the dictionary
                        if rawWord in self.words.keys():
                            #
                            vector[rawWord] = 1

                        # Add it to this text's checked words
                        checkedWords.append(rawWord)

                vectors.append(vector)

        # Create the converted text
        textname = "{}/test.txt".format(exportPath)

        with open(textname, "w", encoding='utf-8') as text:
            # For each text
            for vector in vectors:
                # For each word in the dictionary
                for word in vector:
                    # Write if included
                    text.write(str(vector[word]) + " ")
                # Write the result
                text.write("\n")

        timeEnd = time.time()
        print("Converted {} test data in {:.2f} seconds.".format(
            len(vectors), ((timeEnd - timeStart))))
