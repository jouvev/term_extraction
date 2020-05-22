# -*- coding: utf-8 -*-
import string
from extracteur.extracteur import Extracteur


class ExtracteurNGrammes(Extracteur):
    """
    Objet permettant d'extraire des termes depuis du texte.

    Cet objet extrait les ngrammes d'un document. Un ngramme est extrait seulement
    s'il est entouré de mots vides ou de ponctuations. On fait l'hypothèse que si
    un mot est directement à coté d'un autre mot, alors ces mots auraient du sens
    ensemble.
    """

    def __init__(self,config):
        """Constructeur de la classe ExtracteurNGrammes

        Parameters
        ----------
        config : Config
             Objet qui contient tous les paramètres de la configuration de
             l'extraction.
        """
        super().__init__(config)

    def extraire(self,texte):
        """Méthode d'extraction des termes du texte.

        Parameters
        ----------
        texte : str
             Texte duquel on veut extraire les termes

        Returns
        -------
        list[tuple[str*]]
            liste de termes correspondants à la configuration.
        """
        #on met tout en miniscule
        txt = texte.lower()

        #on sépare les mots
        txtSplit = self.segmenter(txt)

        termes = []
        for n in range(self.config.getLongueurMin(),self.config.getLongueurMax()):
            termes += self.nGrammes(txtSplit, n)

        return self.finaliser(termes)

    def nGrammes(self,listeMots,n):
        """On récupére les ngrammes à partir d'une liste de mot.
        Un ngramme est valide s'il est entouré de mots vides ou de ponctuation.

        Parameters
        ----------
        listeMots : list[str]

        Return
        ------
        list[tuple[str*]]
            liste de ngrammes
        """
        listeTermes = []

        for i in range(len(listeMots)-n+1):
            #on forme un terme potentiel qu'on valide ou pas par la suite
            termePotentiel = listeMots[i:i+n]

            #on valide le terme potentiel s'il est entouré de mots vides ou ponctuation
            if(i>0 and listeMots[i-1] not in string.punctuation and \
               listeMots[i-1] not in self.motsVides ):
                #le terme n'est pas valide
                continue
            if(i+n<len(listeMots) and listeMots[i+n] not in string.punctuation and \
               listeMots[i+n] not in self.motsVides ):
                #le terme n'est pas valide
                continue
            if(termePotentiel[0] in self.motsVides or termePotentiel[-1] in self.motsVides):
                #si le terme commence ou termine par un mot vide, il n'est pas valide
                #car les mots vides avant et après sont retiré et donc il ne sera
                #plus un terme de longueur n passé en argument
                continue

            listeTermes.append(tuple(termePotentiel))

        return listeTermes
