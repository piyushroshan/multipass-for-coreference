import stanford_parser

class Parser:
    """Parses the text using stanford_parser"""
    
    def __init__(self):
        self.__parsedText = ""
        self.__mentionPOSMap = {}

    def process(self, text):
        parser = stanford_parser.Parser()
        self.__parsedText = parser.parseToStanfordDependencies(text)
        for key in self.__parsedText.tokensToPosTags.keys():
            self.__mentionPOSMap[key.range] = self.__parsedText.tokensToPosTags[key]
        
    def getDependencies(self):
        """Returns dependencies list"""
        return self.__parsedText.dependencies
    
    def getMentionPOSMap(self):
        """Returns dictionary of token to POS tag"""
        return self.__mentionPOSMap
               

