from document import Document
from cluster import Cluster
from parser import Parser
from features import Features
from ner import NER

class Reader:
    """Returns object to read files stored on specified path"""
    
    def __init__(self, path):
        self.__document = Document()
        self.__path = path
        self.__parser = Parser()

    def read(self, textFile, mentionsFile):
        """Read files containing the text and mentions, returning an object of them having 'text' and 'cluster list' as attributes"""
 
        ls = []
        text = ""
        mentions = ""
        tuples = []
        mentionClustersList = []
        clusterCount = 0
        mentionToClusterMap = {}
        with open(self.__path + textFile) as f_text:
            text = f_text.read()
        temp = text.splitlines()

        if len(temp[-1]) == 0:
            temp.pop()

        text = " ".join(temp)
        self.__parser.process(text)
        dependenciesList = self.__parser.getDependencies()
        
        print "Index Map to be used when creating mentions file:"
        for i, j in enumerate(text):
            print i, j
        raw_input("\nPlease enter the indices of the mentions in the mentions file: <Press enter to continue process>")

        with open(self.__path + mentionsFile) as f_mention:
            mentions = f_mention.read()
        ls = mentions.splitlines()

        if len(ls[-1]) == 0:
            ls.pop()
        
        for line in ls:
            line = line.split()
            new_tuple = int(line[0]), int(line[1])
            tuples.append(new_tuple)

        for element in tuples:
            left = element[0]
            right = element[1]
            mentions = text[left:right]
            mentionClustersList.append(Cluster(mentions, element))
            mentionToClusterMap[element] = mentionClustersList[-1]
            clusterCount = clusterCount + 1
        
        n = NER()
        print"\nThis may take some time. Please wait...\n"
        n.process(self.__path + textFile)
        NERMap = n.getNERRelations()
        NESet = set(NERMap.keys())
        feature = Features(dependenciesList)
        self.__document.setText(text)
        self.__document.setTextPath(self.__path + textFile)
        self.__document.setMentionClustersList(mentionClustersList)
        self.__document.setFeatures(feature.getAppositiveRelations(), feature.getCopulativeRelations())
        self.__document.setMentionToClusterMap(mentionToClusterMap)
        self.__document.setParserObject(self.__parser)
        self.__document.setNERMap(NERMap)
        self.__document.setNESet(NESet)
        return self.__document
        
        
