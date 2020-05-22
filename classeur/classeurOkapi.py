# -*- coding: utf-8 -*-
from classeur.classeur import Classeur
from classeur.classeurCValue import ClasseurCValue
from classeur.outilsClasseur import normaliserIndex, inverserIndex

class ClasseurOkapi(Classeur):
    """Cette classe attribue comme score aux termes, leur score okapi
    d'après un corpus de référence et selon l'agrégation choisie dans la config.
    """
    def __init__(self,config,indexCorpusRef):
        """Constructeur de la classe ClasseurOkapi

        Parameters
        ----------
        config : Config
             Objet qui contient tous les paramètres de la configuration de
             l'extraction.

        indexCorpusRef : Indexeur
            L'index du corpus de référence qui permet de calculer l'idf pour okapi.
        """
        super().__init__(config)
        self.indexCorpusRef = indexCorpusRef
        self.k = 2.0
        self.b = 0.75

    def noter(self,indexCorpus):
        """Méthode qui attribue un score aux termes.
        Le score correspond à okapi selon le choix fait dans le fichier de
        config, normalisé par document puis pris selon l'agrégation choisie
        dans la config.
        """
        index = indexCorpus.getIndex()
        avgdl = self.indexCorpusRef.getCorpus().getNbMoyenMot()

        #on construit l'index mais avec comme valeur d'okapi depuis l'index du corpus
        okapiIndex = dict()
        for doc,dictTermeFreq in index.items():
            #dict[tuples[str*],float] -> dictionnaire du score okapi(en valeur) pour chaque terme(en clé) dans le doc
            tmp = dict()
            for term, freq in dictTermeFreq.items():
                idf = self.indexCorpusRef.getIDFOkapiTerme(term)
                dl = indexCorpus.getCorpus().getDocumentById(doc).getNbMot()
                okapi = (freq * (self.k + 1))/(freq + (self.k * (1-self.b+self.b*(dl/avgdl))))
                tmp[term] = idf*okapi
            okapiIndex[doc] = tmp

        #On normalise pour chaque document afin de préparer l'agrégation.
        #Pour comparer ce qui est comparable
        normaliserIndex(okapiIndex)

        #on calcule l'index inverse à partir de l'index
        okapiIndexInv = inverserIndex(okapiIndex)

        #Agrège les résultats
        dictTermesOkapi = self.agregerScore(indexCorpus.getCorpus().size(),okapiIndexInv)

        #Fait une normalisation sur le score final avant de le retourner
        self.normaliserScoreClassement(dictTermesOkapi)

        #Calcul avec ou sans c-value selon la config
        if(self.config.getCValue()):
            cValue = ClasseurCValue(self.config)
            dictTermesOkapi = cValue.scoreAvecCValue(indexCorpus,dictTermesOkapi)
            self.normaliserScoreClassement(dictTermesOkapi)

        return dictTermesOkapi
