----------- Allows to delete duplicates froml a list -----------

You have to pass a list, it will process "pivots", texts from the list that'll be used as reference texts in order to process the similarity.

The syntax is the following, it'll process a few things when initialized : 

instance = avance.Avance(list_to_process,  NB_PIVOTS : int = 50)




You'll then be able to process the duplicates with the method "process"

The syntax is the following, you can explicit a few parameters:

instance.process(taillegroupe = 50, sensibilite  = .0004)

"taillegroupe" is the size of each group, the smallest, the fastest to process. But a small group means that the texts are only compared to a limited sample.

"sensibilite" is the minimal similarity required between two texts in order to flag them as dulpicates --> the sensivity of the process


There's a example notebook called "test.ipynb" alongside a list so you can try the script !