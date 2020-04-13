# -*- coding: utf-8 -*-
from nltk.stem import SnowballStemmer

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
        
        dictStemTerme : dict[tuple[str*],dict[tuple[str*],int]]
            Lorsque stem est à True dans la config ce dictionnaire permet de 
            retrouver la forme de surface la plus fréquente pour le stem
            
        stemmer : SnowballStemmer
            Objet permettant de faire du stemming
        """
        self.config = config
        
        if(self.config.getStem()):
            self.dictStemTerme = dict()
            self.stemmer = SnowballStemmer('french')

    def extraction(self,texte):
        """Méthode d'extraction des termes du texte.
        
        Parameters
        ----------
        texte : str 
             Texte duquel on veut extraire les termes
             
        Raises
        ------
        NotImplementedError
            Lève toujours cette erreur car cette classe est abstraite
        """
        raise NotImplementedError
        
    def termeToStem(self,listeTermes):
        """Méthode qui renvoie la liste des stem correspondant à la liste de 
        termes donné en paramètre. Met à jour le dictionnaire dictStemTerme. 
        Pour ensuite pouvoir faire appel à la méthode stemToTerme.
        
        Parameters
        ----------
        listeTermes : List[tuple[str*]]
             liste de termes extrait du texte
             
        Returns
        -------
        List[tuple[str*]]
            Liste de stem correspondant à la liste de termes donné en paramètre.
            
        Raises
        ------
        RuntimeError
            Si la configuration ne permet pas le stemming, cette méthode ne peut
            être appelé'
        """
        if(self.config.getStem()):
            RuntimeError('La configuration ne permet pas le stemming, cette méthode ne peut être appelé')
            
        listeStem = []
        for terme in listeTermes :
            stem = []
            for mot in terme:
                stem.append(self.stemmer.stem(mot))
            stem = tuple(stem)
            listeStem.append(stem)
            
            #mise à jour du dictionnaire
            if(stem not in self.dictStemTerme):
                self.dictStemTerme[stem] = {terme : 1}
            else:
                if(terme not in self.dictStemTerme[stem]):
                    self.dictStemTerme[stem][terme] = 1
                else :
                    self.dictStemTerme[stem][terme] += 1
                    
        return listeStem
    
    def stemToTerme(self,listeStem):
        """Méthode qui renvoie la liste des termes correspondant à la liste de 
        stem donné en paramètre. Le terme qui correspond au stem est celui qui 
        à le plus fréquement donné ce stem.
        
        Parameters
        ----------
        listeStem : List[tuple[str*]]
             liste de stem que l'on souhaite trnasformer en terme plus compréhensible
             
        Returns
        -------
        List[tuple[str*]]
            Liste de termes correspondant à la liste de stem donné en paramètre.
            
        Raises
        ------
        KeyError
            Si un stem de la liste n'a aucune correspondance en terme
        RuntimeError
            Si la configuration ne permet pas le stemming cette méthode ne peut
            être appelé'
        """
        if(self.config.getStem()):
            RuntimeError('La configuration ne permet pas le stemming, cette méthode ne peut être appelé')
            
        listeTermes = []
        for stem in listeStem:
            if (stem not in self.dictStemTerme):
                raise KeyError("Le stem : \""+' '.join(stem)+"\" n'a pas de terme associé dans le dictionnaire")
            
            #recupération de la forme la plus fréquente 
            occMax = -1
            for terme,occ in self.dictStemTerme[stem].items():
                if(occ>occMax):
                    occMax = occ 
                    termeMax = terme
            
            listeTermes.append(termeMax)
            
        return listeTermes