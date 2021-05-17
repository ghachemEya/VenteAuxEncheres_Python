#Fonction Consulter avec return id et prix article disponible 
import os,sys

idArticle = 0 #id article avce de consulter le fichier 
prixArticle = 0 #prix article avce de consulter le fichier 

# 1) open file 
file = open('biens.txt', 'r') 

# 2) extaire l'id et le prix d'un article disponible (de départ)
for ligne in file :
    print(ligne)
    if 'Disponible ' in ligne :
       # convertir d'une chaine à une liste 
       a= ligne.split()
       idArticle = a[0]
       prixArticle = a[1]


print(idArticle)
print(prixArticle)



          
