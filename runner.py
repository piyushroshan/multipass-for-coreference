from reader import Reader
from informationfiller import InformationFiller
from pass1 import ExactMatchSieve
from pass2 import PreciseConstructsSieve

def printClusterDetails():
    """Prints head mention and mentions list for each cluster"""
    
    for i in doc.getMentionClustersList():
        print i.getHeadMention()
        print "|",
        for mention in i.getMentionsList():
            left = mention[0]
            right = mention[1]
            print docText[left:right] + str(mention), "|",
        print "\n"
    raw_input("==========================<Press enter to continue>==========================")

verbose = True  # True: prints the details of the clusters after each pass; False: no such printing

filename = raw_input("Enter name of input file: ")
mentionfile = raw_input("Enter name of mentions file: ")

reader  = Reader("input/")
filler = InformationFiller()
doc = reader.read(filename, mentionfile)
docText = doc.getText()
filler.process(doc)
if verbose:
    print "\nInitially:\n"
    printClusterDetails()

sieve = ExactMatchSieve()
sieve.process(doc)
if verbose:
    print "\nAfter Pass 1:\n"
    printClusterDetails()

sieve = PreciseConstructsSieve()
sieve.process(doc)
if verbose:
    print "\nAfter Pass 2:\n"
    printClusterDetails()
