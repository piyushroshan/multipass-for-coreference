from sieve import Sieve
from pass3 import StrictHeadMatchSieve
from decorators import overrides

class StrictHeadMatchSieveVariant2(Sieve):
    """Pass 5 of the multi-sieve model.
    This is a variant of Pass 3 that drops the word inclusion constraint.
    
    """
    
    def __init__(self):
        pass
        
    @overrides(Sieve)
    def process(self, docObj):
        """Merges clusters that pass all the relations of pass 3, excluding word inclusion"""
        
        sieve = StrictHeadMatchSieve()
        sieve.process(docObj, checkWordInclusion=False)
