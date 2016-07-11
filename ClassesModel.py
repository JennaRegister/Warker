from LOTlib.Eval import primitive
from LOTlib.DataAndObjects import FunctionData
import random

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Data
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def make_data(size=100):
    mydata=lotsa(200,100)
    return [FunctionData(input=[],
                         #output={'g a k': size, 's a f': size, 'n a m':size, 'h a ng':size})]
                         #output={'f e ng': size, 's e ng': size, 's e k':size, 'h e ng':size})]
                         output = mydata)]
                         #output={'b i m': size, 'b o p': size})]



#can make output dictionaries of the stimuli

def generate():
    unrestricted = ['k', 'g', 'm', 'n']
    onsets = ['f', 'h']
    codas = ['s', 'N']
    vowels = ['e']

    onsets += (unrestricted)
    codas += (unrestricted)

    stim = ''
    stim+=random.choice(onsets)+' '+random.choice(vowels)+' '+random.choice(codas)
    return stim

def lotsa(n, size):
    mydata = {}
    for i in range(0,n):
        mydata.update({generate():size})
    print(mydata)
    return mydata





import LOTlib.Miscellaneous
from LOTlib.Grammar import Grammar
from LOTlib.Miscellaneous import q
from LOTlib.Eval import register_primitive
register_primitive(LOTlib.Miscellaneous.flatten2str)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Grammar
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Let's make the natural classes
@primitive
def bilabial_():
    return "pbmw"

@primitive
def frontvowels_():
    return "ie"

@primitive
def fricatives_():
    return "fvtszh"
@primitive
def alveolar_():
    return "tdsznlr"
@primitive
def glottal_():
    return "h"
@primitive
def palatal_():
    return "j"

@primitive
def velars_():
    return"kgN"



@primitive
def strintersection(s1, s2):
  out = ""
  for c in s1:
    if c in s2 and not c in out:
      out += c
  return out

@primitive

def strunion(s1, s2):
    out = s1
    for c in s2:
        if not c in out:
            out += c
    return out

@primitive
def strdifference(s1, s2):
  out = ""
  for c in s1:
    if c not in s2 and not c in out:
      out += c
  return out



TERMINAL_WEIGHT = 250

grammar = Grammar()

grammar.add_rule('START', 'flatten2str', ['EXPR'], 1.0)
grammar.add_rule('EXPR', 'sample_', ['SET'], 1.0)
grammar.add_rule('EXPR', 'cons_', ['EXPR', 'EXPR'], 1.0/2.0)

#clean string version
'''grammar.add_rule('SET', '"%s"', ['STRING'], 1.0)
grammar.add_rule('STRING', '%s%s', ['TERMINAL', 'STRING'], 1.0)
grammar.add_rule('STRING', '%s', ['TERMINAL'], 1.0)'''

#set operations
grammar.add_rule('SET', 'strunion', ['SET', 'SET'], 1.0/10.)
grammar.add_rule('SET', 'strintersection', ['SET', 'SET'], 1.0/10.)
grammar.add_rule('SET', 'strdifference', ['SET', 'SET'], 1.0/10.)

#sets go to the natural classes
grammar.add_rule('SET', 'bilabial_()', None, 1.0)
grammar.add_rule('SET', 'frontvowels_()', None, 1.0)
grammar.add_rule('SET', 'fricatives_()', None, 1.0)
grammar.add_rule('SET', 'alveolar_()', None, 1.0)
grammar.add_rule('SET', 'glottal_()', None, 1.0)
grammar.add_rule('SET', 'palatal_()', None, 1.0)
grammar.add_rule('SET', 'velars_()', None, 1.0)

# my terminal sounds
grammar.add_rule('TERMINAL', 'g', None, TERMINAL_WEIGHT)
grammar.add_rule('TERMINAL', 'e', None, TERMINAL_WEIGHT)
grammar.add_rule('TERMINAL', 'k', None, TERMINAL_WEIGHT)
grammar.add_rule('TERMINAL', 's', None, TERMINAL_WEIGHT)
grammar.add_rule('TERMINAL', 'f', None, TERMINAL_WEIGHT)
grammar.add_rule('TERMINAL', 'n', None, TERMINAL_WEIGHT)
grammar.add_rule('TERMINAL', 'm', None, TERMINAL_WEIGHT)
grammar.add_rule('TERMINAL', 'h', None, TERMINAL_WEIGHT)
grammar.add_rule('TERMINAL', 'N', None, TERMINAL_WEIGHT)


'''grammar.add_rule('TERMINAL', 'b', None, TERMINAL_WEIGHT)
grammar.add_rule('TERMINAL', 'm', None, TERMINAL_WEIGHT)
grammar.add_rule('TERMINAL', 'p', None, TERMINAL_WEIGHT)
grammar.add_rule('TERMINAL', 'i', None, TERMINAL_WEIGHT)
grammar.add_rule('TERMINAL', 'o', None, TERMINAL_WEIGHT)'''



from LOTlib.Hypotheses.Likelihoods.StochasticFunctionLikelihood import StochasticFunctionLikelihood
from LOTlib.Hypotheses.LOTHypothesis import LOTHypothesis
#from LOTlib.Hypotheses.Likelihoods.LevenshteinLikelihood import StochasticLevenshteinLikelihood
from LOTlib.Hypotheses.Proposers import insert_delete_proposal, ProposalFailedException, regeneration_proposal
import numpy

from LOTlib.Miscellaneous import logsumexp
#from Levenshtein import distance
from math import log

class MyHypothesis(StochasticFunctionLikelihood, LOTHypothesis):
#Levenshtein distance allows us to accept a bit of noise when calculating our likelihood for our proposals
#class MyHypothesis(StochasticLevenshteinLikelihood, LOTHypothesis):
    def __init__(self, grammar=None, **kwargs):
        LOTHypothesis.__init__(self, grammar, display='lambda : %s', **kwargs)


    # we can get stuck pretty easily without this insert/delete ability.
    # This will allow an insertion/deletion in the generated FunctionNodes

    #overwrite propose
    def propose(self, **kwargs):
        ret_value, fb = None, None
        while True: # keep trying to propose
            try:
                ret_value, fb = numpy.random.choice([insert_delete_proposal,regeneration_proposal])(self.grammar, self.value, **kwargs)
                break
            except ProposalFailedException:
                pass

        ret = self.__copy__(value=ret_value)

        return ret, fb

    #overwrite compute_single_likelihood to alter distance factor
    '''def compute_single_likelihood(self, datum, distance_factor=1000.0):
        assert isinstance(datum.output, dict), "Data supplied must be a dict (function outputs to counts)"
        llcounts = self.make_ll_counts(datum.input)
        lo = sum(llcounts.values()) # normalizing constant
        # We are going to compute a pseudo-likelihood, counting close strings as being close
        return sum([datum.output[k]*logsumexp([log(llcounts[r])-log(lo) - distance_factor*distance(r, k) for r in llcounts.keys()]) for k in datum.output.keys()])'''

def make_hypothesis():
    return MyHypothesis(grammar)

def runme(x):
    print "Start: " + str(x)
    return standard_sample(make_hypothesis, make_data, show=False, save_top= "top.pkl", steps=10000)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":

    from LOTlib.Inference.Samplers.StandardSample import standard_sample
    from LOTlib.Primitives.Functional import cons_
    standard_sample(make_hypothesis, make_data, show_skip=9, save_top=False)
    #for _ in range(40):
        #print flatten2str(cons_(cons_(sample_(strdifference(strunion(alveolar_(), strunion(strunion(strunion(alveolar_(), velars_()), fricatives_()), bilabial_())), frontvowels_())), sample_(frontvowels_())), sample_(velars_())))
