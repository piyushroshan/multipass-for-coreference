from sieve import Sieve
from decorators import override

class ExactMatchSieve(Sieve):
    """Pass 1 of this multi-sieve model.
    
    This sieve merges two clusters if the head mentions of both
    the clusters are exactly same, including all modifiers and determiners.
    
    """
    
    def __init__(self):
        pass
    
    @override(Sieve)
    def process(self, document):
        """Merges cluster pairs if their head mentions match exactly"""
        
        mentionClustersList = document.getMentionClustersList()
        headMentionMap = {}
        l = len(mentionClustersList)
        
        for mentionCluster in mentionClustersList:
            headMention = mentionCluster.getHeadMention()
            if headMentionMap.has_key(headMention):
                headMentionMap[headMention].append(mentionCluster)
            else:
                headMentionMap[headMention] = [mentionCluster]
        
        newList = []
        newMentionToClusterMap = {}
        
        for headMention in headMentionMap.keys():
            clusterList = headMentionMap[headMention]
            newCluster = clusterList[0]
            for i in range(1, len(clusterList)):
                newCluster.mergeCluster(clusterList[i])
            newList.append(newCluster)
        
        for cluster in newList:
            mentions = cluster.getMentionsList()
            for mention in mentions:
                newMentionToClusterMap[mention] = cluster
        
        document.setMentionClustersList(newList)
        document.setMentionToClusterMap(newMentionToClusterMap)
        
