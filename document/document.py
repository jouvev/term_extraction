# -*- coding: utf-8 -*-
from nltk.tokenize import word_tokenize

class Document:
    """
    Objet Document qui stocke son id, son contenu, les termes extraits depuis
    son contenu et le nombre de mots qui le compose.

    Attributes
    ----------
    id : int
        L'id du document
    contenu : str
        Le contenu du document
    termes : list[tuple(str*)]
        Par défaut à None. Après appel de la méthode extraction contient la
        liste des termes extraits à partir du contenu.
    nbMot : int
        Nombre de mots dans le document
    """

    #cpt, variable de classe pour avoir un id unique à la création
    cpt = 0
    def __init__(self, contenu):
        """Constructeur de la classe Document

        Parameters
        ----------
        contenu : str
            Le contenu du document
        """
        self.id = Document.cpt
        Document.cpt+=1
        self.contenu = contenu
        self.termes = None
        self.nbMot = len(word_tokenize(self.contenu,'french'))

    def getId(self):
        """Getter d'attribut id

        Returns
        -------
        int
            L'id du document
        """
        return self.id

    def getContenu(self):
        """Getter d'attribut contenu

        Returns
        -------
        str
            Le contenu du document
        """
        return self.contenu

    def getTermes(self):
        """Getter d'attribut termes

        La variable termes correspond à la liste des termes extraits par l'extracteur
        lors de l'appel à la fonction extraction. Il faut donc impérativement
        faire appel à la méthode extraction avant de faire appel à ce getter.

        Returns
        -------
        list[tuple[str*]]
            Les termes extraits du document

        Raises
        ------
        RuntimeError
            Ce getter ne peut être appelé qu'après avoir appelé la méthode extraction
        """
        if(self.termes is None):
            RuntimeError("Ce getter ne peut être appelé qu'après avoir appelé la méthode extraction")
        return self.termes

    def getNbMot(self):
        """Getter d'attribut nbMot

        Returns
        -------
        int
            Le nombre de mots dans le document
        """
        return self.nbMot

    def extraction(self,extracteur):
        """Methode permetant d'extraire les termes du document selon le
        traitement fait par l'extracteur. Place le resultat dans l'attribut termes

        Parameters
        ----------
        extracteur : Extracteur
            Objet Extracteur traitant le contenu pour extraire les termes
        """
        self.termes = extracteur.extraire(self.contenu)
