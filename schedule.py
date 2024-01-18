import matplotlib.pyplot as plt
import numpy as np
from creationGraphe import colorCoursesDict
from generationBDD import parameters

print(parameters['slotsNumber'])
if parameters['slotsNumber']%2 == 0:
    nbrDays = parameters['slotsNumber'] // 2
else: 
    nbrDays = (parameters['slotsNumber'] // 2) + 1
days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
weekDays = [" "]

for i in range(nbrDays):
    weekDays.append(days[i % 5])


fig, ax = plt.subplots()

ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
ax.set_frame_on(False)

cell_text = []
time = ["Matin", "Midi", "Après-midi"]
for i, row in enumerate(time):
    if i == 1:
        cell_text.append([row] + ["Repas"] * nbrDays)
    else:
        cell_text.append([row] + [""] * nbrDays)


table = ax.table(cellText=cell_text, rowLabels=None, colLabels=weekDays, loc='center', cellLoc='center',
                 colColours=["lightgray"] * (nbrDays + 1))  # Utiliser le même gris pour les jours et les horaires


table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)

for j in range(nbrDays + 1):
    cell = table[1, j]
    cell.set_height(0.2)

    cell = table[3, j]
    cell.set_height(0.2)

i, j = 1, 1
cnt = 0
colors = list(colorCoursesDict.keys())
while cnt < len(colors):
    cell = table[i, j]
    cell_text_obj = cell.get_text()
    cell_text_obj.set_text("\n".join(colorCoursesDict[colors[cnt]]))
    cell_text_obj.set_color(colors[cnt])  
    if i == 3:
        i = 1
        j += 1
    else:
        i += 2
    cnt += 1
    
ax.annotate(f"Emploi du temps avec {parameters['studentNumber']} élèves, {parameters['profsNumber']} professeurs, {parameters['courseNumber']} matières et {parameters['slotsNumber']} créneaux disponibles.", xy=(0.5, 0.96), xycoords='axes fraction', ha='center')
ax.annotate(f"Probabilité de {parameters['courseStudentProbability']} entre les élèves et les cours, et de {parameters['availabilityProbability']} sur la disponibilité des professeurs", xy=(0.5, 0.90), xycoords='axes fraction', ha='center')

plt.show()
