import random
def generate():
    unrestricted = ['f', 's', 'm', 'n']
    onsetsa = ['g', 'h']
    codasa = ['k', 'ng']
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
        stim+=random.choice(onsetsa)+' '+v+' '+random.choice(codasa)
    else:
        stim+=random.choice(onsetsi)+' '+v+' '+random.choice(codasi)

    return stim

def lotsa(n, size):
    mydata = {}
    for i in range(0,n):
        mydata.update({generate():size})
    return mydata

d = lotsa(200,100)
print (d)
