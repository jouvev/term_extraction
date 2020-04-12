# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
import re
from document.corpus import Corpus
from document.document import Document
from Parser import Parser

class ParserSplit(Parser):
    """
    Objet qui permet de construire un corpus, les documents dans le fichier .txt
    sont délimités par "##END##"
    """
    def parse(self,path):
        """Methode qui permet de construire un corpus à partir d'un .txt.
        Ici le motif "##END##" doit être une ligne entre deux document dans le
        .txt. Si aucun motif "##END##" n'est présent alors le corpus sera composé
        d'un seul document de contenu tout le .txt.
        
        Parameters
        ----------
        path : str 
            Chemin du fichier à analyser
            
        Raises
        ------
        FileNotFoundError
            Si le chemin vers le fichier n'existe pas
        PermissionError
            Si les permissions du fichier ne permettent pas l'ouverture
        """
        corpusRes = Corpus()

        with open(path,'r',encoding='utf-8') as f :
            txt = f.read()
            
        listedoc = re.split('^##END##$',txt,flags=re.MULTILINE)
        
        for contenu in listedoc:
            corpusRes.addDocument(Document(contenu))
        
        return corpusRes
