import random as rd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


parameters = {
    'studentNumber': 40, #int N: Nombre d'élèves dans l'école
    'courseNumber': 15, #int N: Nombre de cours disponibles
    'profsNumber': 20, #int N: Nombre de professeurs dans l'école. nbrProfs < nbrCours. Un prof enseigne forcément un cours mais les cours sont répartis de manière aléatoire
    'courseStudentProbability': 0.2, #float [0,1]: Probabilité de création d'un lien, entre un élève et un cours
    'availableDays': 15, #int N: Number of days available for the schedule
    'availabilityProbability': 1
}


def DocumentReader(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]
    

def ProfsAvailability(profsNumber, availableDays, availabilityProbability):
    """
    Function: (int, int, float) -> (array)
    Returns:
        Matrix of availability, professors as rows and days as columns, with 1 if the professors is available
    """
    availabilityMatrix = np.random.choice([0, 1], size=(profsNumber, availableDays), p=[1 - availabilityProbability, availabilityProbability])
    return availabilityMatrix


def StudentsCreation(studentNumber, studentsNames):
    """
    Function: (int) -> (list)
    Returns:
        List of nbrEleves unique random firstnames, given nbrEleves
    """
    cnt = 0
    students = []
    while cnt != studentNumber:
        firstname = rd.choice(studentsNames)
        if firstname not in students:
            students.append(firstname)
            cnt += 1
    return students


def ProfsCreation(profsNumber, profsNames):
    """
    Function: (int) -> (list)
    Returns:
        List of nbrProfs unique random lastnames, given nbrProfs
    """
    cnt = 0
    profs = []
    while cnt != profsNumber:
        name = rd.choice(profsNames).split(" ")[0]
        if name not in profs:
            profs.append(name)
            cnt += 1
    return profs


def CoursesCreation(courseNumber, subjectNames):
    """
    Function: (int) -> (list)
    Returns:
        List of nbrCours unique random subjects, given nbrCours
    """
    cnt = 0
    courses = []
    while cnt != courseNumber:
        subject = rd.choice(subjectNames)
        if subject not in courses:
            courses.append(subject)
            cnt += 1
    return courses


def EdgesCreation(students, profs, courses):
    """
    Function: (list, list, list) -> (list, list)
    Returns: 
        Both lists of edges courses/students and courses/professor given the lists of students, courses and professors
    
    """
    courseStudentEdges = []
    courseProfEdges = []
    for student in students:
        hasCourse = False
        for subject in courses:
            if rd.random() < parameters['courseStudentProbability']:
                courseStudentEdges.append((student, subject)) #On affecte un élève à un cours avec une probabilité de 'probaCoursEleves'
                hasCourse = True
        if not(hasCourse): #Si l'élève n'a pas été associé à un cours, on lui en associe un au hasard
            courseStudentEdges.append((student, rd.choice(courses)))
    for subject in courses:
        courseProfEdges.append((subject, rd.choice(profs))) #Pour chaque matière, on lui associe un professeur. Dans ces conditions, un professeur peut ne pas avoir de cours
    return courseStudentEdges, courseProfEdges


def Generation(parameters):
    """
    Global fonction
    """
    availabilityMatrix = ProfsAvailability(parameters['profsNumber'], parameters['availableDays'], parameters['availabilityProbability'])

    studentsNames = DocumentReader("Liste anonymisation/prenoms.txt")
    profsNames = DocumentReader("Liste anonymisation/noms.txt")
    subjectNames = DocumentReader("Liste anonymisation/matieres.txt")

    students = StudentsCreation(parameters['studentNumber'], studentsNames)
    profs = ProfsCreation(parameters['profsNumber'], profsNames)
    courses = CoursesCreation(parameters['courseNumber'], subjectNames)

    courseStudentEdges, courseProfEdges = EdgesCreation(students, profs, courses)

    return availabilityMatrix, students, profs, courses, courseStudentEdges, courseProfEdges


####################################################
#           Affichage du graphe                    #
####################################################

availabilityMatrix, students, profs, courses, courseStudentEdges, courseProfEdges = Generation(parameters)


G = nx.Graph()

G.add_nodes_from(students, bipartite=0, label='students')
G.add_nodes_from(courses, bipartite=1, label='subjects')
G.add_nodes_from(profs, bipartite=0, label='profs')

G.add_edges_from(courseStudentEdges)
G.add_edges_from(courseProfEdges)

pos = dict()
pos.update((node, (1, index / len(students))) for index, node in enumerate(students)) 
pos.update((node, (2, index / len(courses))) for index, node in enumerate(courses)) 
pos.update((node, (3, index / len(profs))) for index, node in enumerate(profs)) 

fig, ax = plt.subplots()
plt.figure(1)
nx.draw(G, pos, ax=ax, with_labels=True, font_color='black', node_color=['#77cad9' if G.nodes[node]['label'] == 'eleve' else '#64d16c' if G.nodes[node]['label'] == 'matiere' else '#f06573' for node in G.nodes], node_size=1000)
