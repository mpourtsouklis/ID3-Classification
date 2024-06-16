class Node:
    # Constructor
    def __init__(self, word):
        self.word = word
        self.falseNode = None
        self.trueNode = None

# Getters
    def getWord(self):
        return self.word

    def getFalseNode(self):
        return self.falseNode

    def getTrueNode(self):
        return self.trueNode

# Setters
    def setFalseNode(self, falseNode):
        self.falseNode = falseNode

    def setTrueNode(self, trueNode):
        self.trueNode = trueNode