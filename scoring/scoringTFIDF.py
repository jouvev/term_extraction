# -*- coding: utf-8 -*-
import math
from scoring.scoring import Scoring
from config.config import METHODES_SCORING

FORMULE_TFIDF = {METHODES_SCORING.TFIDF_STANDARD : lambda tf,idf : tf*idf,\
                 METHODES_SCORING.TFIDF_LOG : lambda tf,idf : (1+math.log(tf))*idf}

class ScoringTFIDF(Scoring):
    
    def __init__(self,config,indexCorpusRef):
        """
        
        """
        super().__init__(config)
        self.indexCorpusRef = indexCorpusRef
        if(config.getMethodeScoring() not in list(FORMULE_TFIDF.keys())):
            raise RuntimeError('Le fichier de configuration de correspond pas à une methode de scoring tfidf')
        self.formuleTFIDF = FORMULE_TFIDF[config.getMethodeScoring()]
        
    def score(self,indexCorpus):
        index = indexCorpus.getIndex()
        dictTermeScore = dict()
        
        tfidfindex = dict()
        for doc,term_occ in index.items():
            tmp = dict()
            for term, tf in term_occ.items():
                idf = self.indexCorpusRef.getIDFTerme(term)
                tfidf = self.formuleTFIDF(tf,idf)
                tmp[term]=tfidf
            tfidfindex[doc] = tmp
            
        normaliseIndex(tfidfindex)
        tfidfindexinv = inverseIndex(tfidfindex)
        for term,doc_tfidf in tfidfindexinv.items():
            dictTermeScore[term] = self.formuleAgregation(doc_tfidf.values())
        
        return dictTermeScore

def normaliseIndex(index):
    for doc,term_tfidf in index.items():
        scoremax = max(term_tfidf.values())#par rapport au doc
        scoremin = min(term_tfidf.values())#par rapport au doc
        for term in term_tfidf.keys():
            index[doc][term] = (index[doc][term]-scoremin) / (scoremax-scoremin)

def inverseIndex(index):
    res = dict()
    for doc,mots in index.items():
        for mot,occ in mots.items():
            if mot not in res:
                res[mot]={doc:occ}
            else:
                res[mot][doc] = occ
    return res
        
        

