from random import sample
from itertools import chain

from colour import Color
import numpy as np
from tqdm.auto import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_distances as pairwise_cos_dist


class avance():
    
    def __init__(self, liste_txt : list[str], NB_PIVOTS : int = 50) -> None:
        self.liste_txt = liste_txt
        self.NB_PIVOTS = NB_PIVOTS
        
        tqdm.write("\nDédoublonage avancé")
        
        with tqdm(total=2, desc = "Calcul des vecteurs BoW") as pbar:
            docspivots = sample(list(enumerate(liste_txt)), NB_PIVOTS)
            textespivots = {e for _, e in docspivots}
            #On crée les vecteurs pour les textes (coordonnée n = occurences du mot de position n dans la liste de vocabulaire)
            vocab = set(' '.join(textespivots).lower().split())
            vectorizer = TfidfVectorizer(stop_words = ("english"), vocabulary = vocab)
            pbar.update()
            tf = vectorizer.fit_transform(liste_txt)
            pbar.update()
            self.arrtf = tf.toarray()
            self.pivots = docspivots


    def process(self, taillegroupe : int = 1000, sensibilite : float = 0.00001) -> None:
        index_doublons , liste_doublons= [], []
        liste_txt = self.liste_txt
        self.taillegroupe = taillegroupe
        avg = np.mean([len(e) for e in liste_txt])
        tupliste = [(txt, i) for i, txt in enumerate(liste_txt)]
        tupliste = sorted(tupliste, key=lambda tupliste: len(tupliste))

        #On sépare les textes en groupes de même taille, en fonction de leur longueur    
        nbgroupes = 1 + (len(tupliste) // taillegroupe)
        groupes = [tupliste[i*taillegroupe:(i+1)*taillegroupe] for i in range(nbgroupes)]

        colors = [Color("blue")] +list(Color("blue").range_to(Color("green"),nbgroupes))
        
        manualpbar = tqdm(groupes, desc="Calcul des vecteurs seconds / supression")
        for i, groupe in enumerate(manualpbar):
            manualpbar.colour = colors[i].hex_l
            #Array de tous les vecteurs 2, un texte par ligne comparé a chaque pivot par colonne
            vect1_pivot = np.array([self.arrtf [i] * (avg / len(e)) for i, e in self.pivots], dtype = np.half)
            vect1_non_pivot = np.array([self.arrtf [i] * (avg / len(e)) for i, e in enumerate(groupe)], dtype = np.half)
            array_vecteurs = pairwise_cos_dist(vect1_non_pivot, vect1_pivot)
            del vect1_non_pivot, vect1_pivot

            #Matrice de la distance cosinus entre chaque texte du corpus, chaque intersection [x,y] donnant
            #la distance entre les textes de rang x et y
            matrice_cosine = pairwise_cos_dist(array_vecteurs)
            del array_vecteurs

            #Permet de faire abstraction de la distance nulle du texte n avec lui-même et ne pas le remonter comme doublon
            for i in range(np.shape(matrice_cosine)[0]): 
                matrice_cosine[i,i] = 1
            #Liste de toutes les distances faibles --> Doublons
            lst_doublons = np.transpose(np.nonzero(matrice_cosine < sensibilite)).tolist()

            del matrice_cosine

            for e in lst_doublons:
                lst_doublons.remove([e[1], e[0]])

            #Nous permet de supprimer directement les doublons par l'index vu que l'élement reste a sa place (seuls ceux qui suivent ont étés supprimés)
            doublons = sorted([e[1] for e in lst_doublons], reverse = True) 
            del lst_doublons

            for db in doublons:
                x = (groupe.pop(db))
                liste_doublons.append(x[0])
                index_doublons.append(x[1])

            del doublons

        self.liste_propre = list(chain.from_iterable(groupes))
        self.index_doublons = sorted(index_doublons)
        self.liste_doublons = sorted(liste_doublons, key=lambda liste_doublons: len(liste_doublons))
        tqdm.write(f"Dédoublonage avancé : Il reste désormais {len(liste_txt)} articles.")