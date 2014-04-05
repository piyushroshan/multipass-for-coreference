from sieve import Sieve
from decorators import overrides

class StrictHeadMatchSieve(Sieve):
    """Pass 3 of the multi-sieve model.
    This sieve merges the mention and antecedent clusters if
    the head word of the mention lies in the set of head words of the antecedent.
    A few more constraints are conjuncted to this, the details of which can be found in the paper.
    
    """
    
    def __init__(self):
        self.__mentionToClusterMap = {}
        self.__mentionClusterList = []
        self.__mentions = set([])
        self.__toMerge = {}
        self.__docText = ""
        text = ""
        with open("Lists/english.stop") as f:
            text = f.read()
        stopWordsList = text.splitlines()
        self.__stopWordSet = set(stopWordsList)

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
        
    def checkAndUpdateOnWordInclusion(self):
        """Updates that a mention cluster and an antecedent cluster are not to be merged if
        non-stop words in mention cluster are not included in those of the antecedent cluster"""
        
        for clusterA, clusterB in self.__toMerge.keys():
            mentionTextsA = [self.__docText[mention[0]:mention[1]] for mention in clusterA.getMentionsList()]
            mentionTextsB = [self.__docText[mention[0]:mention[1]] for mention in clusterB.getMentionsList()]
            moreA = []
            moreB = []
            for mentionText in mentionTextsA:
                words = [word for word in mentionText.split() if word.swapcase() != word]
                moreA.extend(words)
            for mentionText in mentionTextsB:
                words = [word for word in mentionText.split() if word.swapcase() != word]
                moreB.extend(words)
            mentionTextsA.extend(moreA)
            mentionTextsB.extend(moreB)
            wordSetA = set(mentionTextsA).difference(self.__stopWordSet)
            wordSetB = set(mentionTextsB).difference(self.__stopWordSet)
            if wordSetA.intersection(wordSetB) != wordSetB:
                self.__toMerge[(clusterA, clusterB)] = False

    def checkAndUpdateOnCompatibleModifiers(self):
        """Updates that a mention cluster and an antecedent cluster are not to be merged if
        modifiers of the head mention of the cluster are not in the modifiers of the head word of the antecedent"""
        
        for clusterA, clusterB in self.__toMerge.keys():
            modifiersA = clusterA.getHeadMention().split()
            modifiersA.pop()
            modifiersB = clusterB.getHeadMention().split()
            modifiersB.pop()
            modifierSetA = set(modifiersA)
            modifierSetB = set(modifiersB)
            if modifierSetA.intersection(modifierSetB) != modifierSetB:
                self.__toMerge[(clusterA, clusterB)] = False

    def wordWithinWord(self, clusterA, clusterB):
        """Returns whether either of the mentions is within the other mention"""
    
        headSpanA = clusterA.getHeadSpan()
        headSpanB = clusterB.getHeadSpan()
        a = headSpanA
        b = headSpanB
        if b[0] < a[0]:
            a, b = b, a
        return a[1] >= b[1]
    
    @overrides(Sieve)
    def process(self, docObj, checkWordInclusion=True, checkCompatibleModifiers=True):
        """Merges clusters that pass all the relations of pass 3, modified by arguments passed to it"""
        
        self.__mentionToClusterMap = docObj.getMentionToClusterMap()
        self.__mentionClusterList = docObj.getMentionClustersList()
        self.__mentions = set(self.__mentionToClusterMap.keys())
        self.__docText = docObj.getText()
        
        headSpanList = []
        sortedClusterList = []
        clusterListLength = 0
        self.__toMerge = {}
        
        for cluster in self.__mentionClusterList:
            headSpanList.append(cluster.getHeadSpan())
        headSpanList.sort()

        for headSpan in headSpanList:
            sortedClusterList.append(self.__mentionToClusterMap[headSpan])

        self.__mentionClusterList = sortedClusterList
        docObj.setMentionClustersList(sortedClusterList)
    
        clusterListLength = len(sortedClusterList)
        for first in range(clusterListLength-1):
            clusterA = sortedClusterList[first]
            mentionTexts = [self.__docText[mention[0]:mention[1]] for mention in clusterA.getMentionsList()]
            wordSet = set(text.split()[-1] for text in mentionTexts)
            for second in range(first + 1, clusterListLength):
                clusterB = sortedClusterList[second]
                mention = clusterB.getHeadMention()
                headWord = mention.split()[-1]
                if headWord in wordSet:
                    self.__toMerge[(clusterA, clusterB)] = True
        
        if checkWordInclusion:
            self.checkAndUpdateOnWordInclusion()
            
        if checkCompatibleModifiers:
            self.checkAndUpdateOnCompatibleModifiers()

        for clusterA, clusterB in self.__toMerge.keys():
            if self.__toMerge[(clusterA, clusterB)] and not self.wordWithinWord(clusterA, clusterB):
                self.mergeClusters(clusterA, clusterB)
                    
        
