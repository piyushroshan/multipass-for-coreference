from subprocess import PIPE, call, Popen

class NER:
    """Use Stanford-NER to get name-entity relationship"""
    
    def __init__(self):
        self.__nerDict = {}
                
    def process(self, textFilePath):
        """Process the text file to find name-entity relationships"""

        nerDict = {}
        tupleStart = 0
        tupleEnd = 0
        tupleLength = 0
        nerRelation = ""
        prevRelation = ""
        nextRelation = ""
        start = -1
        end = -1
        
        with open(textFilePath) as f:
            text = f.read()
        
        p = Popen(["bash", "stanford-ner-2012-11-11/ner.sh", textFilePath], stdout=PIPE, stderr=PIPE)
        nerText = p.communicate()[0]
        entityRelationsList = nerText.split()
        for relation in entityRelationsList:
            idx2 = relation.find('/')
            if idx2 != -1:
                tupleLength = idx2
                tupleEnd = tupleStart + tupleLength
                nextRelation = relation[idx2+1:]
                if nextRelation != 'O':
                    if prevRelation == nextRelation:
                        end = tupleEnd
                    else:
                        if start != -1 and end != -1:
                            self.__nerDict[start,end] = nextRelation
                        start = tupleStart
                        end = tupleEnd
                    self.__nerDict[tupleStart, tupleEnd] = nextRelation #remove this if needed for merged only
                else:
                    if prevRelation != 'O' and prevRelation != "" and start != -1 and end != -1:
                        self.__nerDict[start,end] = prevRelation
                    start = -1
                    end = -1
                    
                if text[tupleEnd:tupleEnd + 1] == ' ':
                    tupleStart = tupleEnd + 1
                else:
                    tupleStart = tupleEnd
                prevRelation = nextRelation

    def getNERRelations(self):
        """Returns name-entity relations for all but OTHERS"""
        return self.__nerDict
