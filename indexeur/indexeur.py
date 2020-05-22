# -*- coding: utf-8 -*-
import math
import pickle
from collections import Counter

class Indexeur:
    """
    Objet permettant l'indexation des termes d'un corpus et des fonctionnalités
    d'accés aux valeurs de l'index et de calcul (comme l'idf) d'un terme dans le corpus.

    Attributes
    ----------
    corpus : Corpus
        Corpus contenant les documents dont on a déjà extrait les termes

    index : dict[int,dict[tuple[str*],int]
        L'index des documents; la clé est l'id du document, la valeur est un dictionnaire
        contenant les termes du document en clé et leur fréquence en valeur.

    indexInv : dict[tuple[str*],dict[int,int]]
        Index inverse, la clé est un terme, la valeur est un dictionnaire contenant
        l'id des documents contenant le terme et en valeur la fréquence d'apparition
        du terme dans le document.
    """
    def __init__(self,corpusTraite):
        """Constructeur d'Indexation

        Construit un index du corpus passé en argument, corpus sur lequel on a
        déjà appelé la méthode extraction.

        Parameters
        ----------
        corpusTraite : Corpus
             Corpus sur lequel on a déjà appelé la méthode extraction et que
             l'on veut indexer.
        """
        self.corpus = corpusTraite
        self.calculIndex()

    def getIndex(self):
        """Getter d'index

        Returns
        -------
        dict[int,dict[tuple[str*],int]
            index
        """
        return self.index

    def getIndexInv(self):
        """Getter d'index inverse

        Returns
        -------
        dict[tuple[str*],dict[int,int]]
            index inverse
        """
        return self.indexInv

    def getCorpus(self):
        """Getter du corpus sur lequel on calcule l'index

        Returns
        -------
        Corpus
            corpus sur lequel on calcule l'index
        """
        return self.corpus

    def getNbDocTerme(self,terme):
        """Renvoie le nombre de documents contenants le terme passé en paramètre.

        Parameters
        ----------
        terme : tuple[str*]
            Un terme

        Returns
        -------
        int
            Nombre de documents contenants le terme
        """
        if (terme not in self.indexInv.keys()):
            return  0
        else:
            return len(self.indexInv[terme])

    def getIDFTerme(self,terme):
        """Calcule l'idf(inverse document frequency) du terme dans l'index

        fomrmule de l'idf log((1+N)/(1+n)), où N est le nombre de document
        du corpus et n est le nombre de documents dans lesquels apparaissent
        le terme passé en argument.

        Parameters
        ----------
        terme : tuple[str*]
            Le terme dont on veut l'idf.

        Returns
        -------
        int
            L'idf du terme
        """
        N = self.corpus.size()
        n = self.getNbDocTerme(terme)
        return math.log((1+N)/(1+n))

    def getIDFOkapiTerme(self,terme):
        """Calcule l'idf(inverse document frequency) pour okapi du terme dans l'index

        formule de l'idf log((0.5+N-n)/(0.5+n)), où N est le nombre de document
        du corpus et n est le nombre de documents dans lesquels apparait le terme
        passé en argument.

        Parameters
        ----------
        terme : tuple[str*]

        Returns
        -------
        int
            L'idf du terme pour okapi
        """
        N = self.corpus.size()
        n = self.getNbDocTerme(terme)
        return math.log((N-n+0.5)/(0.5+n))

    def calculIndex(self):
        """Calcule et initialise les attributs index et indexInv

        Appelée lors de la construction de l'objet
        """
        self.index = dict()
        self.indexInv = dict()

        #calcule de l'index
        for doc in self.corpus :
            termes = doc.getTermes()
            self.index[doc.getId()] = dict(Counter(termes))

        #calcule de l'index inverse à partir de l'index déjà calculé
        for doc, dictTermeFreq in self.index.items():
            for terme, freq in dictTermeFreq.items():
                if(terme not in self.indexInv):
                    self.indexInv[terme]={doc:freq}
                else:
                    self.indexInv[terme][doc] = freq

    def sauvegarder(self,path):
        """Sauvegarde l'objet dans un fichier pickle à l'emplacement path.

        Parameters
        ----------
        path : str
            Emplacement de sauvegarde
        """
        with open(path,'wb') as f:
            pickle.Pickler(f).dump(self)

    @classmethod
    def charger(self,path):
        """Charge un objet Indexation depuis un fichier pickle à l'emplacement path.

        Parameters
        ----------
        path : str
            Emplacement de la sauvegarde

        Returns
        -------
        Indexation
            L'objet Indexation chargé depuis le fichier à l'emplacement path.
        """
        with open(path,'rb') as f:
            return pickle.Unpickler(f).load()
