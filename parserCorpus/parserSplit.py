# -*- coding: utf-8 -*-
import re
from document.corpus import Corpus
from document.document import Document
from parserCorpus.parserCorpus import ParserCorpus

class ParserSplit(ParserCorpus):
    """
    Objet qui permet de construire un corpus, les documents dans le fichier .txt
    doivent être séparés par "##END##"
    """
    def parse(self,path):
        """Methode qui permet de construire un corpus à partir d'un .txt.
        Ici le motif "##END##" doit être une ligne entre deux documents dans le
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

        Returns
        -------
        Corpus
            Le corpus extrait du fichier passé en argument
        """
        corpusRes = Corpus()

        with open(path,'r',encoding='utf-8') as f :
            txt = f.read()

        listedoc = re.split('^##END##$',txt,flags=re.MULTILINE)

        for contenu in listedoc:
            corpusRes.addDocument(Document(contenu))

        return corpusRes
