import infokeys
from information import Information

class InformationFiller:
    """Fills information of mentions in there respective clusters"""
    
    def __init__(self):
        self.__animateSet = set([])
        self.__inanimateSet = set([])
        self.__femaleSet = set([])
        self.__maleSet = set([])
        self.__neutralSet = set([])
        self.__pluralSet = set([])
        self.__singularSet = set([])
        self.__namegenderSet = set([])
        self.__namegenderDict = {}       
        with open("Lists/animate.unigrams.txt") as f_animate:
            self.__animateSet = set(self.lower(f_animate.read().splitlines()))
        
        with open("Lists/inanimate.unigrams.txt") as f_inanimate:
            self.__inanimateSet = set(self.lower(f_inanimate.read().splitlines()))
            
        with open("Lists/female.unigrams.txt") as f_female:
            self.__femaleSet = set(self.lower(f_female.read().splitlines()))
            
        with open("Lists/male.unigrams.txt") as f_male:
            self.__maleSet = set(self.lower(f_male.read().splitlines()))
            
        with open("Lists/neutral.unigrams.txt") as f_neutral:
            self.__neutralSet = set(self.lower(f_neutral.read().splitlines()))
            
        with open("Lists/plural.unigrams.txt") as f_plural:
            self.__pluralSet = set(self.lower(f_plural.read().splitlines()))

        with open("Lists/singular.unigrams.txt") as f_singular:
            self.__singularSet = set(self.lower(f_singular.read().splitlines()))

        with open("Lists/namegender.combine.txt") as f_namegender:
            text = self.lower(f_namegender.read().splitlines())
            for items in text:
                items = items.split()
                self.__namegenderDict[items[0].lower()] = items[1].lower()          
                self.__namegenderSet.add(items[0].lower())
                                
    def lower(self, ls):
        """Returns list contents in lowercase"""
        
        ls2 = []
        for x in ls:
            ls2.append(x.lower())
        return ls2
    
    def process(self,doc_obj):
        """Checks and fills information for each cluster in clusterlist of given document"""

        NESet = doc_obj.getNESet()
        NERMap = doc_obj.getNERMap()
        mentionPOSMap = doc_obj.getParserObject().getMentionPOSMap()
        for mentionCluster in doc_obj.getMentionClustersList():
            number = Information()
            gender = Information()
            animacy = Information()
            head = mentionCluster.getHeadMention().lower()
            headSpan = mentionCluster.getHeadSpan()
            singularByMap = None
            if headSpan in mentionPOSMap.keys() and mentionPOSMap[headSpan].startswith("NN"):
                if mentionPOSMap[headSpan].endswith("S"):
                    singularByMap = False
                else:
                    singularByMap = True
            if head in self.__maleSet:
                gender.addValues("male")
            headWords = head.split()
            for w in headWords:
                if w in self.__maleSet:
                    gender.addValues("male")
                if w in self.__femaleSet:
                    gender.addValues("female")
            if head in self.__femaleSet:
                gender.addValues("female")
            if head in self.__neutralSet:
                gender.addValues("neutral")
            if head in self.__animateSet or (headSpan in NESet and NERMap[headSpan] == 'PERSON'):
                animacy.addValues("animate")
            elif head in self.__inanimateSet or (headSpan in NESet and NERMap[headSpan] != 'PERSON'):
                animacy.addValues("inanimate")
            else:
                animacy.addValues("animate")
                animacy.addValues("inanimate")
            if head in self.__singularSet or headSpan in NESet or singularByMap == True:
                number.addValues("singular")
            if head in self.__pluralSet or singularByMap == False:
                number.addValues("plural")
            if head in self.__namegenderDict.keys():
                gender.addValues(self.__namegenderDict[head])                                         
            
            mentionCluster.addInformation(infokeys.gender,gender)
            mentionCluster.addInformation(infokeys.number,number)
            mentionCluster.addInformation(infokeys.animacy,animacy)
            
                        

