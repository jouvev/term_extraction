# -*- coding: utf-8 -*-
class Parser:
    """
    Objet qui permet d'analyser un fichier .txt pour fabriquer un corpus
    """
    def parse(self,path):
        """Methode qui analyse un fichier .txt est renvoie un corpus
        
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
