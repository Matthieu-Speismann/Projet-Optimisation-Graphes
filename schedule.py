import matplotlib.pyplot as plt
import numpy as np
from creationGraphe import colorCoursesDict

# Créer les données pour le tableau
jours_semaine = ["", "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
creneaux_horaires = ["8h-9h", "9h-10h", "10h-11h", "11h-12h", "12h-13h", "13h-14h", "14h-15h", "15h-16h", "16h-17h"]

# Créer la figure et les axes
fig, ax = plt.subplots()

# Cacher les axes
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
ax.set_frame_on(False)

# Ajouter les cellules au tableau
cell_text = []
for i, row in enumerate(creneaux_horaires):
    if i == 4:  # Ligne 5 (index 4) correspondant à 12h-13h
        cell_text.append([row] + ["Repas"] * 5)
    else:
        cell_text.append([row] + [""] * 5)  # Remplacer "Repas" par une chaîne vide pour les autres lignes

# Créer le tableau
table = ax.table(cellText=cell_text, rowLabels=None, colLabels=jours_semaine, loc='center', cellLoc='center', colColours=["lightgray"] * 6)  # Utiliser le même gris pour les jours et les horaires

# Ajuster le style du tableau
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)

i, j = 1, 1
cnt = 0
colors = list(colorCoursesDict.keys())
while cnt != len(colors):
    cell = table[i, j]
    cell_text_obj = cell.get_text()
    cell_text_obj.set_text("\n".join(colorCoursesDict[colors[cnt]]))
    cell_text_obj.set_color(colors[cnt])  
    if i == 4: #Repas
        i += 2
    elif i == 9:
        i = 1
        j += 1
    else:
        i += 1
    cnt += 1


# print(colorCoursesDict)
# Afficher le tableau
plt.show()