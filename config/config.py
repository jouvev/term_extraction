# -*- coding: utf-8 -*-
from enum import Enum
import re
from distutils.util import strtobool

METHODES_EXTRACTION = Enum('METHODES_EXTRACTION', 'POSTAG NGRAMMES')
METHODES_SCORING = Enum('METHODES_SCORING', 'FREQUENCE TFIDF_STANDARD TFIDF_LOG OKAPI CVALUE')
FORMULES_AGREGATION = Enum('FORMULES_AGREGATION', 'MAX SUM MEAN')

PARAMS_OBLIGATOIRE = ['STEM','METHODEEXTRACTION','LONGUEURMIN','LONGUEURMAX',
                      'SEUILNBOCCMIN','METHODESCORING','FORMULEAGREGATION',
                      'CVALUE','CORPUSPATH','OUTPUTPATH']

class Config:
    """
    Objet de configuration des parametre de l'extraction et scoring de termes
    
    Attributes
    ----------
    stem : bool 
        Si True permet de remplacer les termes par leur stem. 
    
    methodeExtraction : METHODES_EXTRACTION
        Si POSTAG permet d'extraire les termes avec du POS tagging anisi avoir 
        des termes plus pertinent.
        Si NGRAMMES recupère les n-grammes de façon simple
    
    longueurMin : int
        Longueur minimale d'un termes en nombre de mots
        
    longueurMax : int
        Longueur maximale d'un termes en nombre de mots
        
    seuilNbOccMin : int
        Les termes ne sont pris en compte que s'ils sont présent plus de 
        seuilNbOccMin. Ce seuil s'applique sur les documents du corpus et non 
        sur le corpus.
    
    methodeScoring : METHODES_SCORING
        La façon dont laquelle ont attribut un score au termes. Soit juste la 
        FREQUENCE, soit avec un TFIDF_STANDARD c'est-à-dire la formule est : tf*idf 
        ou bien TFIDF_LOG formule : (1+log(tf))*idf, ou encore la methode OKAPI
        
    formuleAgregation : FORMULES_AGREGATION
        Quand il y a plusieurs documents dans le corpus on doit agréger le score
        des termes. Soit on prend le score max du terme parmi tout les document,
        soit on prend la sommme ou encore la moyenne.
    
    cValue : bool
        Si TRUE le score d'un terme sera la moyenne géometrique de la 
        methodeScoring  et la C-Value, qui a pour but de pénaliser les termes 
        qui sont imbriquer dans d'autre.
        
    corpusPath : str
        Chemin du fichier corpus
        
    outputPath  : str
        Chemin du fichier de sortie dans lequel on écrira le résultat
    """
    def __init__(self,path):
        """Constructeur de la classe Config 
        
        Intialise l'objet avec les valeurs du fichier de chemin path
        
        Parameters
        ----------
        path : str 
            Chemin du fichier de config
        """
        with open(path,'r',encoding='utf-8') as f:
            txt = f.read()
        self.recuperationParams(txt)
        
    def recuperationParams(self,txt):
        """
        Methode qui récupére les paramètres défini en attribut depuis txt
        
        Parameters
        ----------
        txt : str 
            Texte d'ensemble de lignes param = valeur, si la ligne commence 
            par # elle est ignoré
            
        Raises
        ------
        KeyError
            Cette erreur est levé quand une valeur de paramètre n'est pas valide
        ValueError
            Cette erreur est levé quand une valeur entiére ou booléen n'est pas
            valide ou quand un paramètre du fichier config n'est pas un paramètre
            légale, ou encore lorsque un paramètre n'est pas présent dans le fichier
            de config.
        """
        #On retire les commentaires et les lignes vides
        lignesParams = re.findall('^[^#\n].*$',txt,flags=re.MULTILINE)
                                     
        #Permet de verifié que tout les paramètres ont été entrés
        dictVerifParams = {param:False for param in PARAMS_OBLIGATOIRE}
        
        #On crée nos paramétres
        for ligne in lignesParams:
            param,valeur = ligne.split('=')
            param,valeur = param.strip().upper(),valeur.strip()
            
            if(param == 'STEM'):
                self.stem = bool(strtobool(valeur))
            elif(param == 'METHODEEXTRACTION'):
                self.methodeExtraction = METHODES_EXTRACTION[valeur.upper()]
            elif(param == 'LONGUEURMIN'):
                self.longueurMin = int(valeur)
            elif(param == 'LONGUEURMAX'):
                self.longueurMax = int(valeur)
            elif(param == 'SEUILNBOCCMIN'):
                self.seuilNbOccMin = int(valeur)
            elif(param == 'METHODESCORING'):
                self.methodeScoring = METHODES_SCORING[valeur.upper()]
            elif(param == 'FORMULEAGREGATION'):
                self.formuleAgregation = FORMULES_AGREGATION[valeur.upper()]
            elif(param == 'CVALUE'):
                self.cValue = bool(strtobool(valeur))
            elif(param == 'CORPUSPATH'):
                self.corpusPath = valeur
            elif(param == 'OUTPUTPATH'):
                self.outputPath = valeur
            else:
                raise ValueError(param+" n'est pas un paramètre")
            
            dictVerifParams[param] = True
            
        #On vérifie que tout les paramètres sont présent sinon on léve une exception 
        for param,present in dictVerifParams.items():
            if(not present):
                raise ValueError('Il manque au moins le paramètre suivant dans le fichier de config : '+param)
        
        if(self.longueurMin>self.longueurMax):
            raise ValueError('LONGUEURMAX doit être supérieur ou égale à LONGUEURMIN')
        
    def getStem(self):
        """Getter stem
        
        Returns
        -------
        bool
            stem
        """
        return self.stem
    
    def getMethodeExtraction(self):
        """Getter methodeExtraction
        
        Returns
        -------
        Enum METHODES_EXTRACTION
            POSTAG | NGRAMMES
        """
        return self.methodeExtraction
    
    def getLongueurMin(self):
        """Getter longueurMin
        
        Returns
        -------
        int
            Longueur minimale d'un terme en nombre de mots
        """
        return self.longueurMin
    
    def getLongueurMax(self):
        """Getter longueurMax
        
        Returns
        -------
        int
            Longueur maximale d'un terme en nombre de mots
        """
        return self.longueurMax
    
    def getSeuilNbOccMin(self):
        """Getter seuilNbOccMin
        
        Returns
        -------
        int
            Seuil minimale pour accepter un terme
        """
        return self.seuilNbOccMin
    
    def getMethodeScoring(self):
        """Getter methodeScoring
        
        Returns
        -------
        Enum METHODES_SCORING
            FREQUENCE | TFIDF_STANDARD | TFIDF_LOG | OKAPI
        """
        return self.methodeScoring
    
    def getFormuleAgregation(self):
        """Getter formuleAgregation
        
        Returns
        -------
        Enum FORMULES_AGREGATION
           MAX | SUM | MEAN
        """
        return self.formuleAgregation
        
    def getCValue(self):
        """Getter cValue
        
        Returns
        -------
        bool
            cValue
        """
        return self.cValue
    
    def getCorpusPath(self):
        """Getter corpusPath
        
        Returns
        -------
        str
            chemin du fichier corpus
        """
        return self.corpusPath
    
    def getOutputPath(self):
        """Getter outputpath
        
        Returns
        -------
        str
            chemin du fichier de sortie
        """
        return self.outputPath
    