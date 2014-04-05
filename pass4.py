from sieve import Sieve
from pass3 import StrictHeadMatchSieve
from decorators import overrides

class StrictHeadMatchSieveVariant1(Sieve):
    """Pass 4 of the multi-sieve model.
    This is a variant of Pass 3 that drops the compatible modifiers constraint.
    
    """
    
    def __init__(self):
        pass
        
    @overrides(Sieve)
    def process(self, docObj):
        """Merges clusters that pass all the relations of pass 3, excluding compatible modifiers"""
        
        sieve = StrictHeadMatchSieve()
        sieve.process(docObj, checkCompatibleModifiers=False)
