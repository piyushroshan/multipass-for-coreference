#! /usr/bin/env python

from reader import Reader
from informationfiller import InformationFiller
from pass1 import ExactMatchSieve
from pass2 import PreciseConstructsSieve
from pass3 import StrictHeadMatchSieve
from pass4 import StrictHeadMatchSieveVariant1
from pass5 import StrictHeadMatchSieveVariant2
from pass6 import RelaxedHeadMatchSieve
from pass7 import PronounSieve

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

sieve = StrictHeadMatchSieve()
sieve.process(doc)
if verbose:
    print"\nAfter Pass 3:\n"
    printClusterDetails()

sieve = StrictHeadMatchSieveVariant1()
sieve.process(doc)
if verbose:
    print"\nAfter Pass 4:\n"
    printClusterDetails()

sieve = StrictHeadMatchSieveVariant2()
sieve.process(doc)
if verbose:
    print"\nAfter Pass 5:\n"
    printClusterDetails()
    
#sieve = RelaxedHeadMatchSieve()
#sieve.process(doc)
#if verbose:
#    print"\nAfter Pass 6:\n"
#    printClusterDetails()

#sieve = PronounSieve()
#sieve.process(doc)
#if verbose:
#    print"\nAfter Pass 7:\n"
#    printClusterDetails()

print "Coreference Resolution Pass 1 to 5 Complete!"