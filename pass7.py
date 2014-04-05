from sieve import Sieve
from decorators import overrides
import infokeys

class PronounSieve(Sieve):
    """Pass 7 of the multi-sieve model.
    Matches pronoun mentions to antecedents
    
    """
    
    def __init__(self):
        self.__mentionToClusterMap = {}
        self.__mentionClusterList = []
        self.__mentions = set([])
        self.__toMerge = {}
        self.__docText = ""
        self.__NERMap = {}
        self.__NESet = set([])
        
    def mergeClusters(self, clusterA, clusterB):
        """Merges two clusters and updates mentionToClusterMap, mentionClusterList"""
        
        a, b = clusterA, clusterB
        firstA = a.getHeadSpan()
        firstB = b.getHeadSpan()
        if firstB[0] <= firstA[0] and firstB[1] >= firstB[1]:
            a, b = b, a
        if b in self.__mentionClusterList:
            a.mergeCluster(b)
            self.__mentionClusterList.remove(b)
            self.__mentionToClusterMap[b] = a
        
    @overrides(Sieve)
    def process(self, docObj):
        """Merges clusters that pass all the relations of pass 7"""
        
        self.__mentionToClusterMap = docObj.getMentionToClusterMap()
        self.__mentionClusterList = docObj.getMentionClustersList()
        self.__mentions = self.__mentionToClusterMap.keys()
        self.__docText = docObj.getText()
        self.__NERMap = docObj.getNERMap()
        self.__NESet = docObj.getNESet()
        
        headSpanList = []
        sortedClusterList = []
        for cluster in self.__mentionClusterList:
            headSpanList.append(cluster.getHeadSpan())
        headSpanList.sort()

        for headSpan in headSpanList:
            sortedClusterList.append(self.__mentionToClusterMap[headSpan])
        
        self.__mentionClusterList = sortedClusterList
        docObj.setMentionClustersList(sortedClusterList)
        
        l = len(sortedClusterList)
        i = 0
        
        while i < l - 1:
            clusterA = self.__mentionClusterList[i]
            infoCollectionA = clusterA.getInformationCollection()
            numberSetA = infoCollectionA[infokeys.number].getValues()
            genderSetA = infoCollectionA[infokeys.gender].getValues()
            animacySetA = infoCollectionA[infokeys.animacy].getValues()
            j = i + 1
            while j < l:
                clusterB = self.__mentionClusterList[j]
                infoCollectionB = clusterB.getInformationCollection()
                numberSetB = infoCollectionB[infokeys.number].getValues()
                genderSetB = infoCollectionB[infokeys.gender].getValues()
                animacySetB = infoCollectionB[infokeys.animacy].getValues()
                if len(animacySetB.intersection(animacySetA)) > 0 and \
                len(genderSetB.intersection(genderSetA)) > 0 and \
                len(numberSetB.intersection(numberSetA)) > 0:
                    self.mergeClusters(clusterA, clusterB)
                    j = j - 1
                    l = l - 1
                j = j + 1
            i = i + 1
