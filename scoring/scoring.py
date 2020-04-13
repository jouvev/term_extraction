# -*- coding: utf-8 -*-
from statistics import mean
from config.config import FORMULES_AGREGATION

FONCTION_AGREGATION = {FORMULES_AGREGATION.MAX : lambda iter : max(iter), \
                       FORMULES_AGREGATION.SUM : lambda iter : sum(iter), \
                       FORMULES_AGREGATION.MEAN : lambda iter : mean(iter)}

class Scoring:
    """Cette classe permet d'attribuer un score pour les termes d'un corpus
    
    """
    def __init__(self,config):
        """Constructeur de la classe Scoring
        
        Parameters
        ----------
        config : Config
            objet de configuration pour permettre de faire le scoring en fonction
            da le configuration        
        """
        self.config=config
        self.formuleAgregation = FONCTION_AGREGATION[config.getFormuleAgregation()]
    
    def score(self,indexCorpus):
        """Méthode qui attribut un score à chacun des termes du corpus
        
        Parameters
        ----------
        indexCorpus : Indexation
            L'index du corpus
            
        Returns
        -------
        dict[tuple[str*],float]
            Dictionnaire de terme en clé et score en valeur
            
        Raises
        ------
        NotImplementedError
            Lève toujours cette erreur car cette classe est abstraite
        """
        raise NotImplementedError

    def getScoreTrie(self,indexCorpus):
        """Attribut un score aux tremes du corpus puis les trie en fonction du
        score
        
        Parameters
        ----------
        indexCorpus : Indexation
            L'index du corpus
            
        Returns
        -------
        List[tuple[tuple[str*],float]]
            Liste trié par ordre décroissant des scores des termes 
        """
        dictTerme = self.score(indexCorpus)
        return sorted(dictTerme.items(), key=lambda t: t[1], reverse=True)
