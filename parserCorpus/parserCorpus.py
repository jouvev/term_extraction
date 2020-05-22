# -*- coding: utf-8 -*-
class ParserCorpus:
    """
    Objet qui permet d'analyser un fichier .txt pour fabriquer un corpus
    """
    def parse(self,path):
        """Méthode qui analyse un fichier .txt est renvoie un corpus

        Parameters
        ----------
        path : str
            Chemin du fichier à analyser

        Raises
        ------
        NotImplementedError
            Lève toujours cette erreur car cette classe est abstraite
        """
        raise NotImplementedError
