# -*- coding: utf-8 -*-
"""
Programme principale pour l'extraction de terme.
A appeler avec un fichier de config en argument
"""
import sys
import os.path
from config.config import Config,METHODES_EXTRACTION,METHODES_SCORING
from indexation.indexation import Indexation
from extracteur.extracteurSpacy import ExtracteurSpacy
from parserCorpus.parserArticle import ParserArticle
from parserCorpus.parserSplit import ParserSplit
from scoring.scoringTFIDF import ScoringTFIDF

PATH_CORPUSREF = 'ressources/corpus_ref.fr'

def recupIndRef(config):
    pathInd= 'ressources/indRef_'+str(config.getMethodeExtraction().value)+ \
            '_'+str(config.getStem())+'_'+str(config.getLongueurMin())+'_'+\
            str(config.getLongueurMax())+'.pkl'
    
    #si le fichier existe sinon on le créer
    if(os.path.exists(pathInd)):
        return Indexation.load(pathInd)
    else:
        #récupére le corpus de référence
        corpusRef = ParserArticle().parse(PATH_CORPUSREF)
        
        #on créer l'extracteur correspondant au fichier de config
        extracteur = recupExtracteur(config)
        
        #on extrait les termes du corpus de référence
        corpusRef.extraction(extracteur)
        #on créer l'indexation et on la sauvegarde pour ne pas recalculer la prochaine fois 
        indexation = Indexation(corpusRef)
        indexation.save(pathInd)
        
        return indexation
        
def recupExtracteur(config):
    #on créer l'extracteur correspondant au fichier de config
    if(config.getMethodeExtraction() == METHODES_EXTRACTION.POSTAG):
        return ExtracteurSpacy(config)
        
def recupScoring(config,indexCorpusRef):
    #on créer l'extracteur correspondant au fichier de config
    if(config.getMethodeScoring() == METHODES_SCORING.TFIDF_STANDARD or\
       config.getMethodeScoring() == METHODES_SCORING.TFIDF_LOG):
        return ScoringTFIDF(config,indexCorpusRef)
    
if __name__=='__main__':
    #récuperation du fichier de config et initialise l'objet Config  
    pathConfig = sys.argv[1]
    config = Config(pathConfig)
    
    #on récupére l'indexation de référence 
    indRef = recupIndRef(config) 
    
    #on récupére le corpus à traiter 
    pathCorpus = config.getCorpusPath()
    corpus = ParserSplit().parse(pathCorpus)
    
    #on extrait les termes du corpus
    extracteur = recupExtracteur(config)
    corpus.extraction(extracteur)


    indexCorpus = Indexation(corpus)
    
    scoring = recupScoring(config,indRef)
    
    listeTermesTrie = scoring.getScoreTrie(indexCorpus)
    
    listeTerme = [terme for terme,score in listeTermesTrie]
    if(config.getStem()):
        listeTerme = extracteur.stemToTerme(listeTerme)
    listeScore = [score for terme,score in listeTermesTrie]
    
    with open('res.txt','w',encoding='utf-8') as f:
        tmp=''
        for i,terme,score in zip(list(range(1,len(listeTerme)+1)),listeTerme,listeScore):
            tmp += str(i)+';'+' '.join(terme)+';'+str(score)+'\n'
        f.write(tmp)
    
