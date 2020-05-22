# -*- coding: utf-8 -*-
from statistics import mean
from config.config import FORMULES_AGREGATION

FONCTION_AGREGATION = {FORMULES_AGREGATION.MAX : max, \
                       FORMULES_AGREGATION.SUM : sum, \
                       FORMULES_AGREGATION.MEAN : mean}

class Classeur:
    """Cette classe permet d'attribuer un score aux termes d'un corpus"""
    def __init__(self,config):
        """Constructeur de la classe Classeur

        Parameters
        ----------
        config : Config
            objet de configuration pour permettre la classification des termes en fonction
            de la configuration
        """
        self.config=config
        self.formuleAgregation = FONCTION_AGREGATION[config.getFormuleAgregation()]

    def noter(self,indexCorpus):
        """Méthode qui attribue un score à chacun des termes du corpus

        Parameters
        ----------
        indexCorpus : Indexation
            L'index du corpus

        Returns
        -------
        dict[tuple[str*],float]
            Dictionnaire avec les termes en clé et les scores en valeur

        Raises
        ------
        NotImplementedError
            Lève toujours cette erreur car cette classe est abstraite
        """
        raise NotImplementedError

    def classer(self,indexCorpus):
        """Attribue un score aux termes du corpus puis les trie en fonction du
        score, puis par ordre alphabétique si égalité sur le score

        Parameters
        ----------
        indexCorpus : Indexation
            L'index du corpus

        Returns
        -------
        List[tuple[tuple[str*],float]]
            Liste triée par ordre décroissant des scores des termes
        """
        #on récupère le dictionnaire terme/score
        dictTerme = self.noter(indexCorpus)
        #D'abord le tri par ordre alphabétique
        tmp = sorted(dictTerme.items(), key=lambda t: ' '.join(t[0]))
        #Puis le tri par score
        return sorted(tmp, key=lambda t: t[1], reverse=True)

    def normaliserScoreClassement(self,dictTermesScores):
        """Normalise en place le score des termes du dictionnaire passé en paramètre.

        Recentre entre 0 et 1 le score des termes.

        Parameters
        ----------
        dictTermesScores : dict[tuples[str*],float]
            Dictionnaire du score pour un terme
        """
        scoremax = max(dictTermesScores.values())
        scoremin = min(dictTermesScores.values())
        for terme in dictTermesScores.keys():
            dictTermesScores[terme] = (dictTermesScores[terme]-scoremin) / (scoremax-scoremin)
            
    def agregerScore(self,nbdoc,indexInvScore):
        """Renvoie un dictionnaire de scores pour les termes du dictionnaire passé en argument, 
        agréger selon la config.
        
        Parameters
        ----------
        nbdoc : int 
            nombre de document dans le corpus. Important pour la moyenne.
            
        indexInvScore : dict[tuple[str*],dict[int,float]] 
            Score d'un terme dans les documents
            
        Returns
        -------
        dict[tuple[str*],float]
            Dictionnaire de score agrégé pour un terme
        """
        if(self.config.getFormuleAgregation() == FORMULES_AGREGATION.MEAN):
            #on ajoute autant de zéros qu'il y a de document où le terme n'apparait pas
            return {terme : self.formuleAgregation(list(dictDocScore.values())+[0]*(nbdoc-len(dictDocScore)))  \
                 for terme,dictDocScore in indexInvScore.items()}
                 
        return {terme : self.formuleAgregation(dictDocScore.values())  \
                 for terme,dictDocScore in indexInvScore.items()}
        