from LOTlib.Eval import primitive
from LOTlib.DataAndObjects import FunctionData
import random
# # The data here has a form
def make_data(size=100):
    return [FunctionData(input=[],
                         #output={'g a k': size, 's a f': size, 'n a m':size, 'h a ng':size})]
                         #output={'f a ng': size, 's a ng': size, 's a k':size, 'h a ng':size})]
                         output=lotsa(10, size))]

def generate():
    unrestricted = ['k', 'g', 'm', 'n']
    onsets = ['f', 'h']
    codas = ['s', 'ng']
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
    return mydata




import LOTlib.Miscellaneous
from LOTlib.Grammar import Grammar
from LOTlib.Miscellaneous import q

from LOTlib.Eval import register_primitive
register_primitive(LOTlib.Miscellaneous.flatten2str)

# # # # # # # # # # # # # # # # # # # # # # # # # # # #

@primitive
def consT_(x,y):
    return (x,y)

@primitive
def cdrT_(x):
    try: return x[1:]
    except IndexError: return tuple()

@primitive
def carT_(x):
    try:    return x[0]
    except IndexError: return tuple()

@primitive
def listyset_(args):
    abba = []
    for a in args:
        abba.append(tuple(a))
    return set(tuple(abba))

TERMINAL_WEIGHT = 1.5

grammar = Grammar()

# flattern2str lives at the top, and it takes a cons, cdr, car structure and projects it to a string
grammar.add_rule('START', 'flatten2str', ['EXPR'], 1.0)

'''grammar.add_rule('BOOL', 'and_', ['BOOL', 'BOOL'], 1.)
grammar.add_rule('BOOL', 'or_', ['BOOL', 'BOOL'], 1.)
grammar.add_rule('BOOL', 'not_', ['BOOL'], 1.)'''

#grammar.add_rule('EXPR', 'if_', ['BOOL', 'EXPR', 'EXPR'], 1.)
#grammar.add_rule('BOOL', 'equal_', ['EXPR', 'EXPR'], 1.)

#grammar.add_rule('BOOL', 'flip_', [''], TERMINAL_WEIGHT)
grammar.add_rule('EXPR', 'sample_', ['SET'], 1.)
# List-building operators
grammar.add_rule('EXPR', 'consT_', ['EXPR', 'EXPR'], 1.)
grammar.add_rule('EXPR', 'cdrT_', ['EXPR'], 1.)
grammar.add_rule('EXPR', 'carT_', ['EXPR'], 1.)

grammar.add_rule('EXPR', '', ['TERMINAL'], 3. )


grammar.add_rule('SET', 'set_', ['EXPR'], 10.)
grammar.add_rule('SET', 'set_', ['TERMINAL'], 10.)
grammar.add_rule('SET', 'union_', ['SET', 'SET'], 14.)


#grammar.add_rule('TERMINAL', '', None, TERMINAL_WEIGHT)
grammar.add_rule('TERMINAL', q('g'), None, TERMINAL_WEIGHT)
grammar.add_rule('TERMINAL', q('a'), None, TERMINAL_WEIGHT)
grammar.add_rule('TERMINAL', q('k'), None, TERMINAL_WEIGHT)
grammar.add_rule('TERMINAL', q('s'), None, TERMINAL_WEIGHT)
grammar.add_rule('TERMINAL', q('f'), None, TERMINAL_WEIGHT)
grammar.add_rule('TERMINAL', q('n'), None, TERMINAL_WEIGHT)
grammar.add_rule('TERMINAL', q('m'), None, TERMINAL_WEIGHT)
grammar.add_rule('TERMINAL', q('h'), None, TERMINAL_WEIGHT)
grammar.add_rule('TERMINAL', q('ng'), None, TERMINAL_WEIGHT)

## Allow lambda abstraction
grammar.add_rule('EXPR', 'apply_', ['LAMBDAARG', 'LAMBDATHUNK'], 1)
grammar.add_rule('LAMBDAARG',   'lambda', ['EXPR'], 1., bv_type='EXPR', bv_args=[] )
grammar.add_rule('LAMBDATHUNK', 'lambda', ['EXPR'], 1., bv_type=None, bv_args=None ) # A thunk


from LOTlib.Hypotheses.Likelihoods.StochasticFunctionLikelihood import StochasticFunctionLikelihood
from LOTlib.Hypotheses.LOTHypothesis import LOTHypothesis

class MyHypothesis(StochasticFunctionLikelihood, LOTHypothesis):
    def __init__(self, grammar=None, **kwargs):
        LOTHypothesis.__init__(self, grammar, display='lambda : %s', **kwargs)

def make_hypothesis():
    return MyHypothesis(grammar)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":

    from LOTlib.Inference.Samplers.StandardSample import standard_sample

    standard_sample(make_hypothesis, make_data, show_skip=9, save_top=False)
