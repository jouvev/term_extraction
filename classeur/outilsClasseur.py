# -*- coding: utf-8 -*-
"""
Dans ce module on trouve des fonctions outils pour les classes Classeur
"""
def normaliserIndex(index):
    """Normalise l'index passé en argument.

    Recentre le score entre 0 et 1, pour chaque document.

    Parameters
    ----------
    index : dict[int,dict[tuple[str*],float]]
        Dictionnaire du score tfidf pour un terme par document
    """
    
    for iddoc,dictTermesTfidf in index.items():
        scoremax = max(dictTermesTfidf.values())
        scoremin = min(dictTermesTfidf.values())
        for terme in dictTermesTfidf.keys():
            if(scoremax-scoremin == 0):
                #cas particulier où tous les termes on le même score. on lui donne docn le score max càd 1
                index[iddoc][terme] = 1
            else:
                index[iddoc][terme] = (index[iddoc][terme]-scoremin) / (scoremax-scoremin)

def inverserIndex(index):
    """Renvoie l'index inverse de l'index passé en argument.

    Parameters
    ----------
    index : dict[int,dict[tuple[str*],float]]
        Dictionnaire du score tfidf pour un terme par document

    Returns
    -------
    dict[tuple[str*],dict[int,float]]
        Dictionnaire du score tfidf par un document pour un terme
    """
    indexInv = dict()
    for iddoc,dictTermesTfidf in index.items():
        for terme,tfidf in dictTermesTfidf.items():
            if terme not in indexInv:
                indexInv[terme]={iddoc:tfidf}
            else:
                indexInv[terme][iddoc] = tfidf
    return indexInv
