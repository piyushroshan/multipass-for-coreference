from sieve import Sieve
from decorators import override
from informationfiller import InformationFiller
import codecs

class PreciseConstructsSieve(Sieve):
    """Pass 2 of multi-sieve model.
    This sieve merges 2 clusters if they have, any of the following relations
    Appositive, Copulative, Demonym, Acronym

    """

    def __init__(self):
        self.__mentionToClusterMap = {}
        self.__mentionClusterList = []
        self.__mentions = set([])
        self.__demonymsMap = {}
        text = ""
        f = codecs.open("Lists/demonyms.txt", "r", "utf-8")
        with f:
            text = f.read()
        text = text.splitlines()
        for line in text:
            ls = line.split("\t")
            for item in ls:
                self.__demonymsMap[item] = ls[0]
        self.__demonymKeySet = set(self.__demonymsMap.keys())
        
    def mergeByRelation(self, relationMap):
        """Merges two clusters by a relation specified by relationMap"""
        
        for mention in relationMap.keys():
            if mention in self.__mentions:
                relation = relationMap[mention]
                if relation not in self.__mentions:
                    continue
                clusterA = self.__mentionToClusterMap[mention] 
                clusterB = self.__mentionToClusterMap[relation]
                headMentionA = clusterA.getHeadMention()
                headMentionB = clusterB.getHeadMention()
                if headMentionA != headMentionB:
                    clusterA.mergeCluster(clusterB)
                    self.__mentionClusterList.remove(clusterB)
                    self.__mentionToClusterMap[relation] = clusterA
    
    def getAcronymOf(self, string):
        """Creates two acronyms for 'string', one dotted and another not"""
        
        letterList = []
        for c in string:
            if c.isalpha() and c.isupper():
                letterList.append(c)
        if len(letterList) == 1:
            letterList = []
        return "".join(letterList), (".".join(letterList) + ".")

    def mergeClusters(self, clusterA, clusterB):
        """Merges two clusters and updates mentionToClusterMap, mentionClusterList"""
        
        a, b = clusterA, clusterB
        firstA = a.getHeadSpan()
        firstB = b.getHeadSpan()
        if firstB[0] <= firstA[0] and firstB[1] >= firstB[1]:
            a, b = b, a
        a.mergeCluster(b)
        self.__mentionClusterList.remove(b)
        self.__mentionToClusterMap[b] = a

    @override(Sieve)
    def process(self, docObj):
        """Merges clusters by each relation of pass 2 sequentially"""

        self.__mentionToClusterMap = docObj.getMentionToClusterMap()
        self.__mentionClusterList = docObj.getMentionClustersList()
        self.__mentions = set(self.__mentionToClusterMap.keys())
        text = docObj.getText()
        apposRelationMap = docObj.getAppositiveRelations()
        copRelationMap = docObj.getCopulativeRelations()
        
        self.mergeByRelation(apposRelationMap)
        self.mergeByRelation(copRelationMap)
        
        demonymMentionMap = {}
        acronymMap = {}
        for mention in self.__mentions:
            left = mention[0]
            right = mention[1]
            string = text[left:right]
            if string in self.__demonymKeySet:
                key = self.__demonymsMap[string]
                if demonymMentionMap.has_key(key):
                    demonymMentionMap[key].append(mention)
                else:
                    demonymMentionMap[key] = [mention]
            if string.isupper():
                if acronymMap.has_key(string):
                    acronymMap[string].append(mention)
                else:
                    acronymMap[string] = [mention]
        acronymSet = set(acronymMap.keys())
        
        for key in demonymMentionMap.keys():
            mentions = demonymMentionMap[key]
            newCluster = self.__mentionToClusterMap[mentions[0]]
            headMention = newCluster.getHeadMention()
            for i in range(1, len(mentions)):
                cluster = self.__mentionToClusterMap[mentions[i]]
                if headMention != cluster.getHeadMention():
                    self.mergeClusters(newCluster, cluster)
        
        for mention in self.__mentions:
            left = mention[0]
            right = mention[1]
            string = text[left:right]
            acronym, acronymDotted = None, None
            if string not in acronymSet:
                acronym, acronymDotted = self.getAcronymOf(string)
            matchedAcronym = None
            if acronym in acronymSet:
                matchedAcronym = acronym
            elif acronymDotted in acronymSet:
                matchedAcronym = acronymDotted
            if not matchedAcronym is None:
                mentions = acronymMap[matchedAcronym]
                newCluster = self.__mentionToClusterMap[mentions[0]]
                headMention = newCluster.getHeadMention()
                for i in range(1, len(mentions)):
                    cluster = self.__mentionToClusterMap[mentions[i]]
                    if headMention != cluster.getHeadMention():
                        self.mergeClusters(newCluster, cluster)
                clusterOf_mention = self.__mentionToClusterMap[mention]
                self.mergeClusters(newCluster, clusterOf_mention)

