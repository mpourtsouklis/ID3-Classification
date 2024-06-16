# Artificial Intelligence Project: ID3-Classification

## Course Information
-  **Course:** Artificial Intelligence
-  **Department:** Computer Science
-  **Institution:** Athens University of Economics and Business
-  **Semester:** 3rd Year's Fall (2021-22)
-  **Instructor:** Ion Androutsopoulos

## Overview
An implementation of the ID3 algorithm for natural language processing and machine learning tasks using the IMDB review database. 

The ID3 algorithm is used to construct decision trees based on textual data to classify movie reviews as positive or negative.

## Modules
### **Data:** Manages the vocabulary construction and data conversion
-  **load:** Constructs the initial vocabulary from the negative and positive training data files
-  **filter:** Refines the vocabulary by removing the most frequent `n` and rarest `k` words and keeps the top `m` frequent words, saving the final vocabulary to `vocabulary.txt`
-  **convertTrain:** Converts training data into vectors based on the constructed vocabulary, generating `positive.txt` and `negative.txt`
-  **convertTest:** Converts test data into vectors based on the constructed vocabulary, generating `test.txt`

### ID3Node: Implements nodes used in the ID3 decision tree, with getters and setters for node properties

### **ID3:** Handles the training and usage of the ID3 decision treeon
-  **train:** Takes paths to negative and positive training data along with the vocabulary and converts them into arrays
-  **build:** Constructs the decision tree based on the trained data
-  **classify:** Classifies test data vectors using the ID3 decision tree and saves results to a specified path

### **Validator:** Calculates accuracy, precision, recall, and F1 score for ID3 decision tree results
-  **check:** Computes true positives, true negatives, false positives, and false negatives from ID3 results
-  **validate:** Calculates and prints accuracy, precision, recall, and F1 score based on the computed metrics

-  ### **PerformanceChecker:** Evaluates ID3 decision tree performance iteratively
-  **checkTrain:** Evaluates ID3 algorithm performance across different sizes of training data, generating tables and charts
-  **checkTest:** Evaluates ID3 algorithm performance across different sizes of test data, generating tables and charts

## Examples
> Training data, removing the 500 most frequent and the 300 rarest words and keeping the 300 most frequent words

![image](https://github.com/mpourtsouklis/ID3-Classification/assets/103905458/8139f221-f257-40f8-8e34-a628b10bbf90) ![image](https://github.com/mpourtsouklis/ID3-Classification/assets/103905458/b687e770-94d2-4f02-b96e-fdbca34269c0)

> Test data, removing the 500 most frequent and the 300 rarest words and keeping the 300 most frequent words

![image](https://github.com/mpourtsouklis/ID3-Classification/assets/103905458/30dba9bd-1555-4021-91fc-6fae7c34f33e) ![image](https://github.com/mpourtsouklis/ID3-Classification/assets/103905458/c4eaf733-e9e1-407b-8a4b-1cc1569eaac3)

