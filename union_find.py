#https://stackoverflow.com/questions/20154368/union-find-implementation-using-python
from collections import defaultdict
def indices_dict(L):
    d = defaultdict(list)
    for i,(a,b) in enumerate(L):
        d[a].append(i)
        d[b].append(i)
    return d

def disjoint_indices(L):
    d = indices_dict(L)
    sets = []
    while len(d):
        Q = set(d.popitem()[1])
        ind = set()
        while len(Q):
            ind |= Q 
            Q = set([y for i in Q
                         for x in L[i] 
                         for y in d.pop(x, [])]) - ind
        sets += [ind]
    return sets

def disjoint_sets(L):
    return [set([x for i in s for x in L[i]]) for s in disjoint_indices(L)]