class Document:
    """Sets and Retrieves Text and Mentions"""

    def __init__(self):
        self.__text = ""
        self.__textPath = ""
        self.__mentionClustersList = []
        self.__apposDict = {}
        self.__copDict = {}
        self.__mentionToClusterMap = {}
        self.__parserObj = None
        self.__NERMap = {}
        self.__NERSet = set([])
        
    def setText(self, string):
        """Adds the text to the object"""
        self.__text = string
        
    def getText(self):
        """Retrieves text from the object"""
        return self.__text
    
    def setTextPath(self, string):
        """Updates the path of input text file"""
        self.__textPath = string
    
    def getTextPath(self):
        """Retrieves the path of the input text file"""
        return self.__textPath
        
    def setMentionClustersList(self, mentionClustersList):
        """Updates the mention clusters list of the document"""
        self.__mentionClustersList = mentionClustersList
        
    def getMentionClustersList(self):
        """Retrieves mention cluster list from the object"""
        return self.__mentionClustersList

    def setFeatures(self, apposDict, copDict):
        """Adds feature relationship in the form of dictionary""" 

        self.__apposDict = apposDict
        self.__copDict = copDict
        
    def getAppositiveRelations(self):
        """Retrieves indices related as appositives"""
        return self.__apposDict
    
    def getCopulativeRelations(self):
        """Retrieves indices related as copulatives"""
        return self.__copDict
        
    def setMentionToClusterMap(self, mentionToClusterMap):
        """Updates the map from mentions to the clusters they belong"""
        self.__mentionToClusterMap = mentionToClusterMap
    
    def getMentionToClusterMap(self):
        """Retrieves a map from the mentions to the clusters they belong"""
        return self.__mentionToClusterMap
    
    def setParserObject(self, parserObj):
        """Sets parserObj"""
        self.__parserObj = parserObj
        
    def getParserObject(self):
        """Returns parserObj"""
        return self.__parserObj
    
    def setNERMap(self, NERMap):
        """Sets NERMap"""
        self.__NERMap = NERMap
        
    def getNERMap(self):
        """Returns NERMap"""
        return self.__NERMap

    def setNESet(self, NERSet):
        """Sets NERSet"""
        self.__NERSet = NERSet
        
    def getNESet(self):
        """Returns NERSet"""
        return self.__NERSet
