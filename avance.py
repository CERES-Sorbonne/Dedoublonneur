from random import sample
from itertools import chain

from colour import Color
import numpy as np
from tqdm.auto import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_distances as pairwise_cos_dist


class avance():
    
    def __init__(self, liste_txt : List[str], taillegroupe : int = 1000, NB_PIVOTS : int = 50) -> None:
        self.liste_txt = liste_txt
        self.taillegroupe = taillegroupe
        self.NB_PIVOTS = NB_PIVOTS
        
        tqdm.write("\nDédoublonage avancé")
        
        with tqdm(total=2, desc = "Calcul des vecteurs BoW") as pbar:
            avg = np.mean([len(e) for e in liste_txt])
            docspivots = sample(liste_txt, NB_PIVOTS)

            #On crée les vecteurs pour les textes (coordonnée n = occurences du mot de position n dans la liste de vocabulaire)
            vocab = set(' '.join(docspivots).lower().split())
            vectorizer = TfidfVectorizer(stop_words = ("english"), vocabulary = vocab)
            pbar.update()
            tf = vectorizer.fit_transform(liste_txt)
            pbar.update()
            arrtf = tf.toarray()

            #On sépare les textes en groupes de même taille, en fonction de leur longueur
            liste_txt = sorted(liste_txt, key=lambda liste_txt: len(liste_txt))
            nbgroupes = 1 + (len(liste_txt) // taillegroupe)
            groupes = [liste_txt[i*taillegroupe:(i+1)*taillegroupe] for i in range(nbgroupes)]

        colors = list(Color("blue").range_to(Color("green"),nbgroupes))
        
        manualpbar = tqdm(groupes, desc="Calcul des vecteurs seconds / supression")
        doublons_tot = {}
        cquoilesdoublons = {}
        for i, groupe in enumerate(manualpbar):
            manualpbar.colour = colors[i].hex_l
            #Array de tous les vecteurs 2, un texte par ligne comparé a chaque pivot par colonne
            vect1_pivot = np.array([arrtf[i] * (avg / len(e["texte"])) for i, e in enumerate(docspivots)], dtype = np.half)
            vect1_non_pivot = np.array([arrtf[i] * (avg / len(e["texte"])) for i, e in enumerate(groupe)], dtype = np.half)
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
            lst_doublons = np.transpose(np.nonzero(matrice_cosine < 0.00001)).tolist()

            del matrice_cosine

            for e in lst_doublons:
                lst_doublons.remove([e[1], e[0]])

            #Nous permet de supprimer directement les doublons par l'index vu que l'élement reste a sa place (seuls ceux qui suivent ont étés supprimés)
            doublons = sorted([e[1] for e in lst_doublons], reverse = True) 
            del lst_doublons

            for db in doublons:
                doublons_tot.add((taillegroupe * i) + db)
                cquoilesdoublons.add(groupe.pop(db))

            del doublons

        self.liste_propre = list(chain.from_iterable(groupes))
        self.index_doublons = doublons_tot
        self.doublons = cquoilesdoublons
        tqdm.write(f"Dédoublonage avancé : Il reste désormais {len(liste_txt)} articles.")