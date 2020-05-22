# -*- coding: utf-8 -*-
from classeur.classeur import Classeur

class ClasseurFrequence(Classeur):
    """Cette classe attribue comme score aux termes, leur fréquence selon l'agrégation
    dans la config.
    """
    def __init__(self,config):
        """Constructeur de la classe ClasseurFrequence

        Parameters
        ----------
        config : Config
            objet de configuration pour permettre de classer les termes en fonction
            da le configuration
        """
        super().__init__(config)

    def noter(self,indexCorpus):
        """Méthode qui attribue comme score aux termes, leur fréquence selon l'agrégation.

        Parameters
        ----------
        indexCorpus : Indexation
            L'index du corpus

        Returns
        -------
        dict[tuple[str*],float]
            Dictionnaire de terme en clé et score en valeur
        """
        indexInv = indexCorpus.getIndexInv()
        return {terme : self.formuleAgregation(dictDocFreq.values()) \
                for terme,dictDocFreq in indexInv.items()}
