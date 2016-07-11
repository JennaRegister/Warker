import random
def generate(bool):

    unrestricted = ['f', 's', 'm', 'n']
    onsetsa = ['g', 'h']
    codasa = ['k', 'N']
    onsetsi = ['k','h']
    codasi = ['g','N']
    vowels = ['a','i']

    onsetsa += (unrestricted)
    codasa += (unrestricted)
    onsetsi += (unrestricted)
    codasi+= (unrestricted)

    stim = ''
    v = random.choice(vowels)

    if v == 'a':
        if bool:
            stim+=random.choice(onsetsa)+' '+v+' '+random.choice(codasa)
        else:
            stim+=random.choice(codasa)+' '+v+' '+random.choice(onsetsa)
    else:
        if bool:
            stim+=random.choice(onsetsi)+' '+v+' '+random.choice(codasi)
        else:
            stim+=random.choice(codasi)+' '+v+' '+random.choice(onsetsi)

    return stim

def lotsa(n, size,bool):
    mydata = {}
    for i in range(0,n):
        mydata.update({generate(bool):size})
    return mydata

d = lotsa(200,100,False)
listy = []
for k,v in d.items():
    if 'N' in k or 'k' in k or 'g' in k or 'h' in k:
        listy.append(k)
print (listy)
