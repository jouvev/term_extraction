# -*- coding: utf-8 -*-
import string
from collections import Counter
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize

#Chemin vers un fichier qui contient un ensemble de mots vides, un mot par ligne
PATH_MOTSVIDES = 'ressources/stopwords.fr'

class Extracteur:
    """
    Objet permettant d'extraire des termes depuis un texte

    Attributes
    ----------
    config : Config
        Objet qui contient tous les paramètres de la configuration de l'extraction.

    dictStemTerme : dict[tuple[str*],dict[tuple[str*],int]]
        Lorsque stem est à True dans la config ce dictionnaire permet de
        retrouver la forme de surface la plus fréquente pour un stem.

    stemmer : SnowballStemmer
        Objet permettant de faire du stemming

    motsVides : set[str]
        Ensemble des mots vides
    """

    def __init__(self, config):
        """Constructeur de la classe Extracteur

        Parameters
        ----------
        config : Config
             Objet qui contient tous les paramètres de la configuration de
             l'extraction.
        """
        self.config = config

        if(self.config.getStem()):
            self.dictStemTerme = dict()
            self.stemmer = SnowballStemmer('french')

        #on charge l'ensemble de mots vides
        with open(PATH_MOTSVIDES,'r',encoding='utf-8') as f:
            self.motsVides = set(f.read().split('\n'))

    def extraire(self,texte):
        """Méthode d'extraction des termes du texte.

        Parameters
        ----------
        texte : str
             Texte duquel on veut extraire les termes

        Raises
        ------
        NotImplementedError
            Lève toujours cette erreur car cette classe est abstraite
        """
        raise NotImplementedError

    def termeToStem(self,listeTermes):
        """Méthode qui renvoie la liste des stems correspondants à la liste des
        termes donnée en paramètre. Met à jour le dictionnaire dictStemTerme.
        Pour ensuite pouvoir faire appel à la méthode stemToTerme.

        Parameters
        ----------
        listeTermes : List[tuple[str*]]
             liste de termes extraits du texte

        Returns
        -------
        List[tuple[str*]]
            Liste de stems correspondants à la liste de termes donnés en paramètre.

        Raises
        ------
        RuntimeError
            Si la configuration ne permet pas le stemming, cette méthode ne peut
            être appelée
        """
        if(self.config.getStem()):
            RuntimeError('La configuration ne permet pas le stemming, cette méthode ne peut être appelée')

        listeStem = []
        for terme in listeTermes :
            stem = []
            for mot in terme:
                stem.append(self.stemmer.stem(mot))
            stem = tuple(stem)
            listeStem.append(stem)

            #mise à jour du dictionnaire
            if(stem not in self.dictStemTerme):
                self.dictStemTerme[stem] = {terme : 1}
            else:
                if(terme not in self.dictStemTerme[stem]):
                    self.dictStemTerme[stem][terme] = 1
                else :
                    self.dictStemTerme[stem][terme] += 1

        return listeStem

    def stemToTerme(self,listeStem):
        """Méthode qui renvoie la liste des termes correspondants à la liste des
        stems donnée en paramètre. Le terme qui correspond au stem est celui qui
        a le plus fréquement donné ce stem.

        Parameters
        ----------
        listeStem : List[tuple[str*]]
             liste de stems que l'on souhaite trnasformer en termes plus compréhensibles

        Returns
        -------
        List[tuple[str*]]
            Liste de termes correspondants à la liste de stems donnée en paramètre.

        Raises
        ------
        KeyError
            Si un stem de la liste n'a aucune correspondance avec un terme
        RuntimeError
            Si la configuration ne permet pas le stemming cette méthode ne peut
            être appelée'
        """
        if(self.config.getStem()):
            RuntimeError('La configuration ne permet pas le stemming, cette méthode ne peut être appelée')

        listeTermes = []
        for stem in listeStem:
            if (stem not in self.dictStemTerme):
                raise KeyError("Le stem : \""+' '.join(stem)+"\" n'a pas de terme associé dans le dictionnaire")

            #récupération de la forme la plus fréquente
            occMax = -1
            for terme,occ in self.dictStemTerme[stem].items():
                if(occ>occMax):
                    occMax = occ
                    termeMax = terme

            listeTermes.append(termeMax)

        return listeTermes

    def retireTermePeuFrequent(self,listeTerme):
        """Cette méthode renvoie la liste des termes donnée en paramètre, privée
        des termes dont la fréquence dans cette liste est inférieure au seuil
        donné dans le fichier de config.

        Returns
        -------
        List[tuple[str*]]
            Liste des termes dont la fréquence est supérieure ou égale au seuil
            renseigné dans le fichier de configuration.
        """
        ensembleTermeSupSeuil = {terme for terme,freq in dict(Counter(listeTerme)).items() \
                                 if freq >= self.config.getSeuilNbOccMin()}

        return [terme for terme in listeTerme if terme in ensembleTermeSupSeuil]

    def nettoyerTerme(self, listeTermeTmp):
        """Nettoie une liste de termes temporaire.

        On retire les mots vides, la ponctuation en début et fin des termes de
        la liste listeTermeTmp. On tronque au niveau des parenthèses. On retire
        les termes qui n'ont pas de sens comme ceux avec un point au milieu
        ou ceux composés d'une lettre ou encore ceux qui ne sont que des chiffres.

        Parameters
        ----------
        listeTermeTmp : list[tuple[str*]]
            Liste des termes temporaires.

        Returns
        -------
        list[tuple[str*]]
            Liste des termes nettoyés
        """
        listeTermePropre = []
        for terme in listeTermeTmp:
            termetmp = terme
            
            #on retire les mots vides et la ponctuation en début de terme
            while(len(termetmp)>0 and (termetmp[0] in self.motsVides \
                  or termetmp[0] in string.punctuation+string.whitespace)):
                termetmp = termetmp[1:]
            #on retire les mots vides et la ponctuation en fin de terme
            while(len(termetmp)>0 and (termetmp[-1] in self.motsVides or \
                  termetmp[-1] in string.punctuation+string.whitespace)):
                termetmp = termetmp[:-1]
            
            #si le terme est vide on invalide 
            if(len(termetmp) <= 0):
                continue
            
            #Si le terme est composé d'un mot de une lettre => invalide
            if(len(termetmp) == 1 and len(termetmp[0])==1):
                continue

            #Si le terme est composé d'un mot et que c'est un nombre => invalide
            if(len(termetmp) == 1 and termetmp[0].isdigit()):
                continue

            #Les points, les virgules, les parenthèses, ...
            #dans les termes n'ont pas de sens on invalide le terme
            valide = True
            caractereNonSens = '.,;()[]!?:"{}'
            t=' '.join([mot for mot in termetmp])
            for l in t:
                if(l in caractereNonSens):
                    valide = False
                    break
            if(not valide):
                continue
                
            #si on est arrivé à cette ligne c'est que le terme a été validé
            #alors on l'ajoute à la liste des termes propres
            listeTermePropre.append(termetmp)

        return listeTermePropre

    def termeBonneLongueur(self,listeTerme):
        """Retire les termes de la liste qui ne sont pas comformes à la taille
        prévue par la configuration

        Parameters
        ----------
        listeTerme : list[tuple[str*]]
            Liste de termes de n'importe quelles tailles

        Returns
        -------
        list[tuple[str*]]
            Liste de termes de la taille prévue par la configuration

        """
        return [terme for terme in listeTerme if len(terme)>= self.config.getLongueurMin() and len(terme)<= self.config.getLongueurMax()]

    def finaliser(self,listeTermeTmp):
        """Prend une liste de termes temporaires et rend une liste des termes propres
        et conformes à la configuration.

        Parameters
        ----------
        listeTermeTmp : list[tuple[str*]]
            Liste de termes temporaires.

        Returns
        -------
        list[tuple[str*]]
            Liste de termes nettoyés et conformes à la configuration
        """
        listeTermeFinale = self.nettoyerTerme(listeTermeTmp)

        if(self.config.getStem()):
            listeTermeFinale = self.termeToStem(listeTermeFinale)

        if(self.config.getSeuilNbOccMin()>1):
            listeTermeFinale = self.retireTermePeuFrequent(listeTermeFinale)

        return self.termeBonneLongueur(listeTermeFinale)

    def segmenter(self,texte):
        """Sépare le texte en liste de mots.

        Parameters
        ----------
        texte : str
            Le texte qu'on souhaite segmenter.

        Returns
        -------
        list[str]
            Liste des mots du texte
        """
        #on sépare les mots
        txtSplit = word_tokenize(texte,'French')

        #on sépare les mots qui ont une aposthrophe car word_tokenize ne le fait pas
        txtSplitTmp = []
        for mot in txtSplit:
            if("'" not in mot):
                txtSplitTmp.append(mot)
            else:
                mots = mot.split("'")
                txtSplitTmp.append(mots[0]+"'")
                txtSplitTmp.append(mots[1])

        return txtSplitTmp
