# -*- coding: utf-8 -*-
import math
from classeur.classeur import Classeur

class ClasseurCValue(Classeur):
    """Cette classe attribue comme score aux termes, leur cValue. Ici le 
    paramètre d'agrégation n'a pas d'influence. La C-value ce calcule seulement 
    sur un document. Donc ici on fusionne les documents avant le calcul.
    
    formule de la C-value : 
        -si le terme n'est pas imbriqué dans d'autre :
             
        -sinon
    """
    def __init__(self,config):
        """Constructeur de la classe ClasseurCValue
        
        Parameters
        ----------
        config : Config
            objet de configuration pour permettre de classer les termes en fonction
            da le configuration        
        """
        super().__init__(config)
        
    def noter(self,indexCorpus):
        """Méthode qui attribue comme score aux termes, leur C-value. 
        
        Parameters
        ----------
        indexCorpus : Indexation
            L'index du corpus
            
        Returns
        -------
        dict[tuple[str*],float]
            Dictionnaire de terme en clé et score en valeur
        """
        dictTermesFreq = {terme : sum(dictDocFreq.values()) \
                         for terme,dictDocFreq in indexCorpus.getIndexInv().items()}
        
        dictTermeScore = dict()
        termesImb = self.calculTermesImbriques(set(dictTermesFreq.keys()))
        
        for terme,ensSousTermes in termesImb.items():
            nbmot = len(terme)
            if(len(ensSousTermes)==0):
                score = dictTermesFreq[terme]
            else:
                somme=0
                for sousTerme in ensSousTermes:
                    somme += dictTermesFreq[sousTerme]
                score = (dictTermesFreq[terme] - (1/len(ensSousTermes)) * somme )
            score *=  math.log2(nbmot+1)#+1 pour les single-word
            dictTermeScore[terme] = score
            
        self.normaliserScoreClassement(dictTermeScore)
        return dictTermeScore
        
        
    def calculTermesImbriques(self,ensTermes):
        """Calcule des termes imbriquées à partir d'un ensemble de termes
        
        Returns
        -------
        dict[tuple[str*],set[tuple[str*]]]
            Dictionnaire avec en clé un terme et en valeur tout les termes qui
            sont imbriqué dans le terme en clé.
        """
        dictTermeImb = dict()
        for terme in ensTermes:
            if(terme not in dictTermeImb):
                dictTermeImb[terme] = set()
            nbmot = len(terme)
            #recherche de tout les sous-termes possible et de leur existance
            for taille in range(1,nbmot):
                for i in range(0,nbmot-taille+1):
                    sousterme = terme[i:i+taille]
                    if(sousterme in ensTermes):
                        if(sousterme not in dictTermeImb):
                            dictTermeImb[sousterme] = {terme}
                        else:
                            dictTermeImb[sousterme].add(terme)
        return dictTermeImb
    
    def scoreAvecCValue(self,indexCorpus,dictTermesScores):
        """Calcule la moyenne géométrique avec le score donné en paramètre et 
        la C-value.
        
        Parameters
        ----------
        dictTermesScores : dict[tuples[str*],float]
            Dictionnaire du score pour un terme
            
        Returns
        -------
        dict[tuple[str*],float]
            Dictionnaire de terme en clé et score en valeur
        """
        dictTermeScoreFinale = dict()
        cValue = self.noter(indexCorpus)
        for terme,score in dictTermesScores.items():
            scoreCValue = cValue[terme]
            dictTermeScoreFinale[terme] = (2*scoreCValue*score)/(scoreCValue+score)
        return dictTermeScoreFinale
