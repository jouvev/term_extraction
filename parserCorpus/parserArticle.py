# -*- coding: utf-8 -*-
import re
from document.corpus import Corpus
from document.document import Document
from parserCorpus.parserCorpus import ParserCorpus

class ParserArticle(ParserCorpus):
    """
    Objet principalement fait pour pouvoir analyser le corpus de réference
    (corpus_ref.fr)
    """
    def parse(self,path):
        """Méthode qui analyse un fichier .txt est renvoie un corpus

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
        with open(path, "r", encoding="utf-8") as file :
            txt = file.read()

        regex=r'<article title=\".*?\">\n(.*?)</article>'
        contenus = re.findall(regex, txt, re.DOTALL)

        for content in contenus:
            corpusRes.addDocument(Document(content))

        return corpusRes
