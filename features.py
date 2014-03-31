class Features:
    """Get information from the dependencies list"""

    def __init__(self, dependenciesList):
        self.__dependenciesList = dependenciesList
        self.__apposDictionary = {}
        self.__copDictionary = {}
        self.process()


    def process(self):
        """Process the features from the dependencies list"""

        text = self.__dependenciesList[0][1].entireText
        nextrcmodTuple = []
        nextnsubjTuple = []
        for dependency in self.__dependenciesList:
            left = dependency[1]
            right = dependency[2]

            if dependency[0] == 'appos':
                self.__apposDictionary[left.range] = right.range

            if dependency[0] == 'nsubj':
                nextnsubjTuple = []
                nextnsubjTuple.append(left.range)
                nextnsubjTuple.append(right.range)

            if dependency[0] == 'cop':
                self.__copDictionary[nextnsubjTuple[1]] = nextnsubjTuple[0]



    def getAppositiveRelations(self):
        """Retrieve all appositive features"""
        return self.__apposDictionary


    def getCopulativeRelations(self):
        """Retrieve all copulative features"""
        return self.__copDictionary
