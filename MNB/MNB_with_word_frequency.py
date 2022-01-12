import math
import numpy as np
import csv
import random
from collections import Counter


class NaiveBayesClassifier():
    """
    Implementation of the Multinominal Naive Bayes document classifier
    """
    def __init__(self):
        self._likelihoods = None
        self._priors = None
        self._classes = [] # unique classes in the training set

    def fit(self, X:list, y:list, countWordClassDict:dict, countClassDict:dict, wordFrequencyDict:dict):
        """
        Fits the training data to the model to learn off

        Paramaters:
        X (list): A list representing features for each example in the training set
        y (list): A list representing the class for each example in the training set
        countWordClassDict (dict): dictionary containing the unique word frequencies that appear in each class
        countClassDict (dict): contains the total number of words that appear in documents of each class
        wordFrequencyDict (dict): contains the total frequency of a word across all classes 
        """
        p = Preprocessor()
        priors = p.calculatePriors(y)
        likelihoods = p.calculateLikelihoods(countWordClassDict, countClassDict, wordFrequencyDict)
        for label in countWordClassDict: self._classes.append(label) # set unique classes
        self._priors = priors
        self._likelihoods = likelihoods

    def classify(self, document:list) -> str:
        """
        Returns the most probable class for a given document

        Paramaters:
        document(list): An example to classify

        Returns:
        str: The most probable class
        """
        predictions = []
        for y in self._classes:
            probability = math.log(self._priors[y]) # Logging probabilities
            for word in document:
                try:
                    probability = probability + (math.log(self._likelihoods[y][word]) * document.count(word)) # Logging probabilities
                except:
                    pass
            predictions.append((y, probability))
        predictions = sorted(predictions, key=lambda tup: tup[1], reverse=True) # to get most likely class
        return predictions[0][0] # return the most probable class
class Preprocessor():
    """
    Preprocesses the training and test data before it is used in model training and classification

    """
    def __init__(self):
        self.stopWords = self.importStopWords("stopwords.txt")

    def importStopWords(self, path='stopwords.txt')->list:
        """
        Reads list of common english words from a text files 

        Paramaters:
        path (str): The path to the .txt file of stopword (one word per line)

        Returns:
        list[str]: A list of stop words
        """
        with open('stopwords.txt', encoding='utf8') as f:
            lines = f.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].replace('\n', '')
        return lines

    def getCountWordClassDict(self, trainingSetDict:dict, y:list) -> dict:
        """
        Returns a dictionary containing the unique word frequencies that appear in each class
        e.g. How many times the word x appears across all documents of class y

        Paramaters:
        trainingSetDict (dict) : A dictionary representing the training set 

        Returns:
        dict: A dictionary of word frequencies for unique words appearing in each class
        """
        countWordClassDict = {}
        for label in y:
            if label not in countWordClassDict:
                countWordClassDict[label] = {}
        for documentID in trainingSetDict.keys():
            label = list(trainingSetDict[documentID].keys())[0]
            documentWords = list(trainingSetDict[documentID][label].keys())
            for word in documentWords:
                if word not in countWordClassDict[label]:
                    countWordClassDict[label][word] = trainingSetDict[documentID][label][word]
                else:
                    countWordClassDict[label][word] += trainingSetDict[documentID][label][word]
        return countWordClassDict

    def getCountClassDict(self, countWordClassDict:dict)->dict:
        """
        Creates a dictionary that contains the total number of words that appear in documents of each class.

        Paramaters:
        countWordClassDict (dict): Dictionary of frequencies for each word that appears in a class (for each class)

        Returns:
        dict: frequencies for each unique word
        """
        countClassDict = {}
        for y in countWordClassDict:
            totalWords = 0
            for word in countWordClassDict[y]:
                wordCount = countWordClassDict[y][word]
                totalWords += wordCount
            countClassDict[y] = totalWords
        return countClassDict

    def calculatePriors(self, y:list)->dict:
        """
        Calculates prior probabilities for each class

        Paramaters:
        y (list): A list of class strings for each training example

        Returns:
        dict: A dictionary containing the prior probability for each unique class
        """
        priors = {}
        for label in y:
            if label not in priors:
                priors[label] = 0
        for label in y:
            priors[label] += 1
        for label in priors:
            priors[label] = priors[label] / len(y)

        return priors

    def getWordFrequencyDict(self, countWordClassDict:dict) -> dict:
        """
        Creates a dictionary containing the total frequency of a word across all classes 

        Paramaters:
        countWordClassDict (dict): A dictionary of word frequencies by class

        Returns:
        dict: dictionary containing the total frequency of a word across all classes 
        """
        wordFrequencyDict = {}
        for y in countWordClassDict:
            for word in countWordClassDict[y]:
                if word not in wordFrequencyDict:
                    wordFrequencyDict[word] = countWordClassDict[y][word]
                else:
                    wordFrequencyDict[word] += countWordClassDict[y][word]
        return wordFrequencyDict

    def transformTermFrequency(self, trainingSetDict:dict) -> dict:

        for document in trainingSetDict:
            label = list(trainingSetDict[document].keys())[0]
            for word in trainingSetDict[document][label]:
                frequency = trainingSetDict[document][label][word]
                frequency = math.log(frequency + 1) # TF transform s 4.1 d_ij = log(d_ij + 1)
                trainingSetDict[document][label][word] = frequency
        return trainingSetDict

    def inverseDocumentFrequencyTransform(self, trainingSetDict:dict) -> dict:
        """
        Inverse document frequency transform as described in section 4.2 of Rennie at el. (2003)

        Paramaters:
        trainingSetDict (dict): training set

        Returns:
        dict: Transformed training set
        """
        wordDocumentFrequencyDict = {}
        for documentID in trainingSetDict:
            label = list(trainingSetDict[documentID].keys())[0]
            for word in trainingSetDict[documentID][label].keys():
                if word not in wordDocumentFrequencyDict:
                    wordDocumentFrequencyDict[word] = 1
                else:
                    wordDocumentFrequencyDict[word] += 1
        numDocuments = len(trainingSetDict)
        for documentID in trainingSetDict:
            label = list(trainingSetDict[documentID].keys())[0]
            for word in trainingSetDict[documentID][label].keys():
                trainingSetDict[documentID][label][word] = trainingSetDict[documentID][label][word] * math.log(numDocuments / wordDocumentFrequencyDict[word])
        return trainingSetDict

    def transformLength(self, trainingSetDict:dict) -> dict:
        """
        This updates each word frequency by dividing it by the sqrt of the sum of squares for each word

        Paramaters:
        trainingSetDict (dict): training set

        Returns:
        dict: Transformed training set
        """
        for documentID in trainingSetDict:
            label = list(trainingSetDict[documentID].keys())[0]
            # Calculate document length
            length = 0
            for word in trainingSetDict[documentID][label].keys():
                length += pow(trainingSetDict[documentID][label][word], 2)
            length = math.sqrt(length)
            # Normalise document
            for word in trainingSetDict[documentID][label].keys():
                trainingSetDict[documentID][label][word] = trainingSetDict[documentID][label][word] / length
        return trainingSetDict

    def calculateLikelihoods(self, countWordClassDict:dict, countClassDict:dict, wordFrequencyDict:dict)->dict:
        """
        Creates a dictionary of conditional probabilities for each word given a class.


        Paramaters:
        countWordClassDict (dict): word frequencies for unique words appearing in each class
        countClassDict (dict): frequencies for each unique word
        wordFrequencyDict (dict): total frequency of a word across all classes by word

        Returns:
        dict: Conditional probabilities for each word given a class
        """
        likelihoodDict = {}
        for word in wordFrequencyDict:
            for y in countWordClassDict:
                if y not in likelihoodDict:
                    likelihoodDict[y] = {}
                if word not in countWordClassDict[y]:
                    countWordClass = 0
                else:
                    countWordClass = countWordClassDict[y][word]
                likelihoodDict[y][word] = (countWordClass + 1) / (countClassDict[y] + len(wordFrequencyDict))
        return likelihoodDict
    
    def removeStopWords(self, wordFrequencyDict:dict)->dict:
        """
        Removes all common english words from the dictionary so that they are not used in 
        classification of an new document

        Paramaters:
        wordFrequencyDict (dict): total frequency of a word across all classes by word

        Return:
        dict: Cleaned wordFrequencyDict (with stop words removed)
        """
        for stopWord in self.stopWords:
            if stopWord in wordFrequencyDict:
                wordFrequencyDict.pop(stopWord)
        return wordFrequencyDict

    def getTopXWords(self, wordFrequencyDict:dict, X:int=1000) -> dict:
        """
        Finds and returns a dictionary of the top most frequent words in the training data

        Paramaters:
        wordFrequencyDict (dict): total frequency of a word across all classes by word
        X (int): top number of words to find e.g. X = 10 -> find top 10 words

        Returns:
        dict: A dictionary of the top X words
        """
        topWordsDict = {}
        while (len(topWordsDict) != X):
            key = max(wordFrequencyDict, key=lambda word: wordFrequencyDict[word])
            topWordsDict[key] = wordFrequencyDict[key]
            wordFrequencyDict.pop(key)
        return topWordsDict

    def getTrainingSetDict(self, attributeIDs:list, X:list, y:list) -> dict:
        """
        Returns a dictionary of training examples 
        TrainingSetDic = {attributeID:{class:word:wordCount}}

        Paramaters:
        attributeIDs(list): A list of IDs for each document
        X (list[list[str]]): A list of word (features) for each example
        y (list[str]): A list class labels

        Returns:
        dict: training examples in dict form
        """
        trainingSetDict = {}
        for i in range(len(attributeIDs)):
            document = X[i]
            label = y[i]
            documentId = attributeIDs[i]
            trainingSetDict[documentId] = {label: {}}
            for word in document:
                frequency = document.count(word)
                trainingSetDict[documentId][label][word] = frequency
        return trainingSetDict

def importData(path:str, labelsInSet:bool=True) -> tuple:
    """
    Paramaters:
    path (str): A path to the .txt file
    labelsInSet (bool): if the dataset doesn't contain labels set to false

    Returns:
    tuple: A tuple of lists for attributeIDs, features and labels if labelsInSet = True

    """
    attributeIDs = []
    labels = []
    features = []
    with open(path, newline='') as f:
        reader = csv.reader(f)
        reader.__next__() # skip the attribute names line
        for row in reader:
            if labelsInSet:
                ID = row[0]
                label = row[1].upper()
                words = row[2].lower().split()
                attributeIDs.append(ID)
                labels.append(label)
                features.append(words)
            else:
                ID = row[0]
                words = row[1].lower().split()
                attributeIDs.append(ID)
                features.append(words)
    if labelsInSet:
        return attributeIDs, labels, features
    else:
        return attributeIDs, features



def main():
    p = Preprocessor()

    skipTest = False # for main process

    print("Importing data")
    attributeIDs, y, X = importData('training_set.csv')
    testAttributeIDs, X_test = importData('testing_set.csv', labelsInSet=False)


    
    # Classify tst.csv
    if not skipTest:
        print("Processing training data...")
        trainingSetDict = p.getTrainingSetDict(attributeIDs, X, y)
        trainingSetDict = p.inverseDocumentFrequencyTransform(trainingSetDict)  # IDF Extention
        countWordClassDict = p.getCountWordClassDict(trainingSetDict, y)
        countClassDict = p.getCountClassDict(countWordClassDict)
        wordFrequencyDict = p.getWordFrequencyDict(countWordClassDict)
        wordFrequencyDict = p.removeStopWords(wordFrequencyDict) # SW Extention
        
        print("Classifying test set & outputting to CSV...")
        nb = NaiveBayesClassifier()
        nb.fit(X, y, countWordClassDict, countClassDict, wordFrequencyDict)
        with open('Results.csv', 'w', newline='') as f:
                writer = csv.writer(f, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(['ID', 'Sentiment'])
                for i in range(len(X_test)):
                    print(str(round(i / len(X_test) * 100, 2)) + "%", end="")
                    print("\r", end="")
                    prediction = nb.classify(X_test[i])
                    ID = testAttributeIDs[i]
                    writer.writerow([ID, prediction])
        print("Classification Complete.")

'''
Insert word frequency code here
'''
def count_word(file_name):
    with open(file_name, encoding="utf-8") as f:
        return Counter(f.read().split())

print("Frequency :", count_word("testing_set.csv"))

if __name__ == "__main__":
    main()
