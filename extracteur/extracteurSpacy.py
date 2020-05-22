# -*- coding: utf-8 -*-
import spacy
from extracteur.extracteur import Extracteur


class ExtracteurSpacy(Extracteur):
    """
    Objet permettant d'extraire des termes depuis du texte grace au POS tagging

    Attributes
    ----------
    nlp : spacy
        Objet permettant de faire le POS tagging
    """

    def __init__(self,config):
        """Constructeur de la classe ExtracteurSpacy

        Parameters
        ----------
        config : Config
             Objet qui contient tous les paramètres de la configuration de
             l'extraction.
        """
        super().__init__(config)
        self.nlp = spacy.load("fr_core_news_sm")

    def extraire(self,texte):
        """Méthode d'extraction des termes du texte.

        Parameters
        ----------
        texte : str
             Texte duquel on veut extraire les termes

        Returns
        -------
        list[tuple[str*]]
            liste de termes correspondant à la configuration.
        """
        #on met tout en miniscule et on remplace les sauts de lignes qui posent des problèmes à spacy
        txt = texte.replace('\n',' ').lower()

        if(self.nlp.max_length < len(txt)):
            #Le texte est trop grand, spacy nous met en garde et peut lever allocationError.
            #Une solution pourrait être de le couper en plusieurs blocs qu'on analyserait
            #bloc par bloc de taille plus raisonnable.
            self.nlp.max_length = len(txt)

        txtTag = self.nlp(txt)

        #On recupère l'ensemble des noms dans le texte qui donneront les termes par la suite.
        #On fait une première sélection en retirant les noms dépendants d'autres noms
        #sauf si c'est lui même ce qui signifie qu'il serait la racine.
        noms = set([t for t in txtTag if t.pos_=='NOUN' and  (t.head==t or t.head.pos_!='NOUN')])

        #Deuxieme selection
        #On retire les noms qui sont dans un terme plus grand.
        noms2 = noms.copy()
        for nom in noms2:
            terme = list(nom.subtree)
            #On recupère les noms du terme autre que la racine.
            nomsSousTerme = [t for t in terme if t.pos_=='NOUN' and t!=nom]
            #Puis on les supprime s'il existe dans la liste des noms que l'on
            #garde pour composer nos termes.
            for n in nomsSousTerme:
                if n in noms:
                    noms.remove(n)
        
        #on forme la liste des termes
        listeTerme = [tuple([mot.text for mot in nom.subtree]) for nom in noms]
        
        #On tronque tout ce qu'il y a derrière une parenthèse
        for iterme in range(0,len(listeTerme)):
            termetmp = listeTerme[iterme]
            if('(' in termetmp):
                listeTerme[iterme] = termetmp[:termetmp.index('(')]

        #on compose nos termes finaux qu'on renvoie
        return self.finaliser(listeTerme)
