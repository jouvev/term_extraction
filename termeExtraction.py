# -*- coding: utf-8 -*-
"""
Programme principale pour l'extraction de terme.
A appeler avec un fichier de config en argument
"""
import sys
import os
import csv
from config.config import Config,METHODES_EXTRACTION,METHODES_SCORING
from indexeur.indexeur import Indexeur
from extracteur.extracteurSpacy import ExtracteurSpacy
from extracteur.extracteurNGrammes import ExtracteurNGrammes
from parserCorpus.parserArticle import ParserArticle
from parserCorpus.parserSplit import ParserSplit
from classeur.classeurTFIDF import ClasseurTFIDF
from classeur.classeurFrequence import ClasseurFrequence
from classeur.classeurCValue import ClasseurCValue
from classeur.classeurOkapi import ClasseurOkapi

PATH_CORPUSREF = 'ressources/corpus_ref.fr'

def recupererIndexeurReference(config):
    """Permet de récupérer l'indexeur du corpus de référence correspondant à 
    la configuration.
    
    Comme le traitement est long si l'indexeur a déjà été créé il est chargé, 
    sinon il est calculé puis enregistré pour les prochaines fois.  
    
    Parameters
    ----------
    config : Config
        objet de configuration
        
    Returns
    -------
    Indexeur
        L'indexeur du corpus de référence correspondant à la configuration
    """
    pathInd= 'ressources/indRef_'+str(config.getMethodeExtraction().value)+ \
            '_'+str(config.getStem())+'_'+str(config.getLongueurMin())+'_'+\
            str(config.getLongueurMax())+'.pkl'
    
    #si le fichier existe sinon on le créer
    if(os.path.exists(pathInd)):
        return Indexeur.charger(pathInd)
    else:
        #récupére le corpus de référence
        corpusRef = ParserArticle().parse(PATH_CORPUSREF)
        
        #on crée l'extracteur correspondant au fichier de config
        extracteur = recupererExtracteur(config)
        
        #on extrait les termes du corpus de référence
        corpusRef.extraction(extracteur)
        #on créer l'indexation et on la sauvegarde pour ne pas recalculer la prochaine fois 
        indexation = Indexeur(corpusRef)
        indexation.sauvegarder(pathInd)
        
        return indexation
        
def recupererExtracteur(config):
    """Permet de récupérer l'extracteur correspondant à la configuration
    
    Parameters
    ----------
    config : Config
        objet de configuration
        
    Returns
    -------
    Extracteur
        L'extracteur correspondant à la configuration
    """
    #on crée l'extracteur correspondant au fichier de config
    if(config.getMethodeExtraction() == METHODES_EXTRACTION.POSTAG):
        return ExtracteurSpacy(config)
    
    if(config.getMethodeExtraction() == METHODES_EXTRACTION.NGRAMMES):
        return ExtracteurNGrammes(config)
        
def recupererClasseur(config,indexCorpusRef):
    """Permet de récupérer le classeur correspondant à la configuration
    
    Parameters
    ----------
    config : Config
        objet de configuration
    
    indexCorpusRef: Indexeur
        Certain classeur on besoin d'un corpus de référence
        
    Returns
    -------
    Classeur
        Classeur correspondant à la configuration
    """
    #on crée l'extracteur correspondant au fichier de config
    if(config.getMethodeScoring() == METHODES_SCORING.FREQUENCE):
        return ClasseurFrequence(config)
    
    elif(config.getMethodeScoring() == METHODES_SCORING.TFIDF_STANDARD or\
       config.getMethodeScoring() == METHODES_SCORING.TFIDF_LOG):
        return ClasseurTFIDF(config,indexCorpusRef)
    
    elif(config.getMethodeScoring() == METHODES_SCORING.CVALUE):
        return ClasseurCValue(config)
    
    elif(config.getMethodeScoring() == METHODES_SCORING.OKAPI):
        return ClasseurOkapi(config,indexCorpusRef)
    
def ecrireCSV(lignes,csvpath):
    """Ecris dans un fichier csv le classement des termes obtenu avant.
    Noms des champs du csv -> rang;terme;score.
    
    Parameters
    ----------
    lignes : zip[list[int],list[tuple(str*)],list[float]]
        Zip du rang, du termes, de son score. Ce qui va correspondre à une 
        ligne du csv rang;terme;score.
    """
    with open(csvpath,'w',encoding='utf-8',newline='') as fcsv:
        csvWriter = csv.writer(fcsv,delimiter=';')
        csvWriter.writerow(['Rang','Terme','Score'])
        for i,terme,score in lignes:
            strTerme = ' '.join(terme)
            csvWriter.writerow([str(i),strTerme,str(score)])
    
if __name__=='__main__':
    #on récupére le chemin d'où on appel le script
    cheminAppel = os.getcwd()+'/'
    #Pour la suite on se place dans le repértoire qui contient le script
    os.chdir(os.path.abspath(os.path.dirname( __file__)))
    
    #récuperation du fichier de config et initialise l'objet Config  
    pathConfig = sys.argv[1]
    config = Config(cheminAppel+pathConfig)
    
    #on récupére l'indexation de référence 
    indRef = recupererIndexeurReference(config) 
    
    #on récupére le corpus à traiter 
    pathCorpus = config.getCorpusPath()
    corpus = ParserSplit().parse(cheminAppel+pathCorpus)
    
    #on extrait les termes du corpus
    extracteur = recupererExtracteur(config)
    corpus.extraction(extracteur)

    #on index le corpus à traiter
    indexCorpus = Indexeur(corpus)
    
    #on récupére le classeur pour classer les termes du corpus
    classeur = recupererClasseur(config,indRef)
    #on récupére les termes classer avec leur score
    listeTermesTrie = classeur.classer(indexCorpus)
    
    #on découpe la liste des termes et scores
    listeTermes = [terme for terme,score in listeTermesTrie]
    listeScores = [score for terme,score in listeTermesTrie]
    
    #si stem = True alors on réécrit les stem en terme plus compréhensible 
    if(config.getStem()):
        listeTermes = extracteur.stemToTerme(listeTermes)
    
    #on écrit dans un csv le résultat
    lignes = zip(list(range(1,len(listeTermes)+1)),listeTermes,listeScores)
    ecrireCSV(lignes,cheminAppel+config.getOutputPath())