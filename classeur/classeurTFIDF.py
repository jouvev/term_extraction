# -*- coding: utf-8 -*-
import math
from classeur.classeur import Classeur
from classeur.classeurCValue import ClasseurCValue
from config.config import METHODES_SCORING
from classeur.outilsClasseur import normaliserIndex, inverserIndex

FORMULE_TFIDF = {METHODES_SCORING.TFIDF_STANDARD : lambda tf,idf : tf*idf,\
                 METHODES_SCORING.TFIDF_LOG : lambda tf,idf : (1+math.log(tf))*idf}

class ClasseurTFIDF(Classeur):
    """Cette classe attribue comme score aux termes, leur tfidf d'après un
    corpus de référence et selon l'agrégation choisie dans la config.

    Il y a deux formules pour le tfidf, on peut choisir dans le fichier de config.
        - Standard -> tf*idf
        - Log -> (1+log(tf))*idf : accorde moins d'importance aux tf que dans
            la formule standard
    """
    def __init__(self,config,indexCorpusRef):
        """Constructeur de la classe ClasseurTFIDF

        Parameters
        ----------
        config : Config
             Objet qui contient tous les paramètres de la configuration de
             l'extraction.

        indexCorpusRef : Indexeur
            L'index du corpus de référence qui permet de calculer l'idf.
        """
        super().__init__(config)
        self.indexCorpusRef = indexCorpusRef
        if(config.getMethodeScoring() not in list(FORMULE_TFIDF.keys())):
            raise RuntimeError('Le fichier de configuration ne correspond pas à une methode de scoring tfidf')
        self.formuleTFIDF = FORMULE_TFIDF[config.getMethodeScoring()]

    def noter(self,indexCorpus):
        """Méthode qui attribue un score aux termes.
        Le score correspond au tfidf standard ou log selon le choix fait dans
        le fichier de config, normalisé par document puis pris selon l'agrégation
        choisie dans la config.
        """
        index = indexCorpus.getIndex()

        #on construit l'index mais avec comme valeur le tfidf depuis l'index du corpus
        tfidfIndex = dict()
        for doc,dictTermeFreq in index.items():
            #dict[tuples[str*],float] -> dictionnaire du score tfidf(en valeur) pour chaque terme(en clé) dans le doc
            tmp = dict()
            for term, tf in dictTermeFreq.items():
                idf = self.indexCorpusRef.getIDFTerme(term)
                tfidf = self.formuleTFIDF(tf,idf)
                tmp[term]=tfidf
            tfidfIndex[doc] = tmp

        #On normalise pour chaque document afin de préparer l'agrégation.
        #Pour comparer ce qui est comparable
        normaliserIndex(tfidfIndex)

        #on calcule l'index inverse du tfidf à partir de l'index tfidf
        tfidfIndexInv = inverserIndex(tfidfIndex)

        #Agrège les résultats
        dictTermesTFIDF = self.agregerScore(indexCorpus.getCorpus().size(),tfidfIndexInv)

        #Fait une normalisation sur le score final avant de le retourner
        self.normaliserScoreClassement(dictTermesTFIDF)

        #Calcul avec ou sans c-value selon la config
        if(self.config.getCValue()):
            cValue = ClasseurCValue(self.config)
            dictTermesTFIDF = cValue.scoreAvecCValue(indexCorpus,dictTermesTFIDF)
            self.normaliserScoreClassement(dictTermesTFIDF)

        return dictTermesTFIDF
