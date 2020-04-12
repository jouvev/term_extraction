# -*- coding: utf-8 -*-

class Extracteur:
    """
    Objet permettant d'extraire des termes depuis du texte
    
    Attributes
    ----------
    config : Config 
        Objet qui contient tout les paramètres de la configuration de l'extraction.
    """
    
    def __init__(self, config):
        """Constructeur de la classe Extracteur
        
        Parameters
        ----------
        config : Config 
             Objet qui contient tout les paramètres de la configuration de 
             l'extraction.
        
        stemToTerme : dict[tuple[str*],tuple[str*]]
            Lorsque stem est à True dans la config ce dictionnaire permet de 
            retrouver la forme de surface la plus fréquente pour le stem
        """
        self.config = config
        self.dictStemToTerme = dict()

    def extraction(self,txt):
        """Méthode d'extraction des termes du texte txt.
        
        Parameters
        ----------
        txt : str 
             Texte duquel on veut extraire les termes
             
        Raises
        ------
        NotImplementedError
            Lève toujours cette erreur car cette classe est abstraite
        """
        raise NotImplementedError
        
    def termeToStem(self,listeTermes):
         """Méthode qui renvoie la liste des stem correspondant à la liste de 
         termes donné en paramètre. Sauvegarde en memoire quelle forme la
         plus fréquente
         
         
        
        Parameters
        ----------
        listeTermes : List[tuple[str*]]
             liste de termes extrait du texte
        """