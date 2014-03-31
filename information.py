class Information:
    """Stores and retrieves information of an object"""
    
    def __init__(self):
        self.__valueSet = set()
        
    def addValues(self,*values):
        """Adds one or more unique values to the object"""
        for value in values:
            self.__valueSet.add(value)
        
    def getValues(self):
        """Retrieves set of all values stored in the object"""
        return self.__valueSet
        
    def clearValues(self):
        """Flush the set containing the information"""
        self.__valueSet = set()
        
    def union(self, information):
        """Perform union of this information object with another information object"""
        self.__valueSet = self.__valueSet.union(information.getValues())
