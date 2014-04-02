class Cluster:
    """A cluster of mentions that correspond to the same entity"""
    
    def __init__(self, mention, headSpan):
        self.__informationCollection = {}
        self.__mentions = [headSpan]
        self.__headMention = mention
        self.__headSpan = headSpan
    
    def addInformation(self, informationKey, information):
        """Add an Information object to the Cluster object with its own key"""
        self.__informationCollection[informationKey] = information

    def getMentionsList(self):
        """Returns the mentions in the Cluster object as a set"""
        return self.__mentions
    
    def getHeadMention(self):
        """Returns the head mention"""
        return self.__headMention
    
    def getHeadSpan(self):
        """Returns start and end positions of the head mention"""
        return self.__headSpan

    def getInformationCollection(self):
        """Returns all the information contained in the Cluster object as a dictionary"""
        return self.__informationCollection

    def mergeCluster(self, cluster):
        """Merges two clusters"""

        self.__mentions = sorted(set(self.__mentions).union(set(cluster.getMentionsList())))
        clusterInfo = cluster.getInformationCollection()
        for k in clusterInfo.keys():
            if self.__informationCollection.has_key(k):
                self.__informationCollection[k].union(clusterInfo[k])
            else:
                self.__informationCollection[k] = clusterInfo[k]

