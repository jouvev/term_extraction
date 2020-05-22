# -*- coding: utf-8 -*-
from statistics import mean

class Corpus:
    """
    Objet Corpus qui stocke une collection de documents.

    Attributes
    ----------
    collection : dict[int,Document]
        Dictionnaire avec en clé l'id du document et en valeur l'objet Document
    nbMoyenMot : float
        Nombre moyen de mots dans les documents du corpus
    """
    def __init__(self):
        """Constructeur de la classe Document

        Construit un corpus vide
        """
        self.collection = dict()
        self.nbMoyenMot = None #calculer lors de l'appel au getter

    def __iter__(self):
        """Permet d'itérer sur les documents dans les boucles for
        ex: for doc in corpus
        """
        return self.collection.values().__iter__()

    def addDocument(self,doc):
        """Ajouter un document au corpus

        Parameters
        ----------
        doc : Document
            Document à ajouter au corpus

        Raises
        ------
        KeyError
            Si l'id du doc est déjà dans le corpus
        """
        iddoc = doc.getId()
        if(iddoc in self.collection):
            raise KeyError("Le corpus contient déjà un document avec le même id : "+str(iddoc))
        self.nbMoyenMot = None #invalide le nombre de mots moyen qui change
        self.collection[iddoc]=doc

    def getDocumentById(self, iddoc):
        """Getter de document avec l'id

        Parameters
        ----------
        iddoc : int
            L'id du document que l'on veut récupérer

        Returns
        -------
        Document
            Le document d'id iddoc

        Raises
        ------
        KeyError
            Si l'iddoc ne correspond à aucun document du corpus
        """
        if(iddoc not in self.collection):
            raise KeyError("iddoc "+str(iddoc)+" n'est pas présent dans le corpus")
        return self.collection[iddoc]

    def size(self):
        """
        Returns
        -------
        int
            Le nombre de documents dans le corpus
        """
        return len(self.collection)

    def getNbMoyenMot(self):
        """Getter de nbMoyenMot

        Returns
        -------
        float
            Le nombre de mots moyen par document du corpus
        """
        if(self.nbMoyenMot is None):
            self.nbMoyenMot = mean([doc.getNbMot() for doc in self])
        return self.nbMoyenMot

    def extraction(self,extracteur):
        """Méthode appelant la méthode extraction de chaque document.

        Parameters
        ----------
        extracteur : Extracteur
            Objet Extracteur traitant le contenu pour extraire les termes
        """
        for doc in self:
            doc.extraction(extracteur)

    def getCollection(self):
        """Getter de la collection de document

        Returns
        -------
        dict[int,Document]
            La collection de document du corpus
        """
        return self.collection
