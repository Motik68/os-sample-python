import datetime

N_PREMIERE_NAVETTE = 4

temps_depot_gennevilliers = datetime.timedelta(minutes=15)
temps_ferme_depot = datetime.timedelta(minutes=4)
temps_navette_depot_ferme = datetime.timedelta(minutes=5)
temps_navette_ferme_avant_train = datetime.timedelta(minutes=1)
temps_navette_ferme_apres_train = datetime.timedelta(minutes=1)

Ligne = [
    {
        'nom': 'Gennevilliers',
        'position': 0,
        'gare': True
    },
    {
        'nom': "L'Etang",
        'position': 1,
        'gare': True
    },
    {
        'nom': 'Verdure',
        'position': 2,
        'gare': True
    },
    {
        'nom': 'Dépôt',
        'position': 2.5,
        'gare': False
    },
    {
        'nom': 'La Ferme',
        'position': 3,
        'gare': True
    },
    {
        'nom': 'Les Fiancés',
        'position': 4,
        'gare': True
    },
    {
        'nom': 'Les Mariniers',
        'position': 6,
        'gare': True
    }
]
iArret = {arret['nom']: i for i, arret in enumerate(Ligne)} # Indice dans Ligne à partir du nom de l'arrêt
Gares = [arret for arret in Ligne if arret['gare']] # Les gares seulement (pas le dépôt)
iGare = {gare['nom']: i for i, gare in enumerate(Gares)} # Indice dans Gares à partir du nom de l'arrêt
position_gare = {gare['nom']: gare['position'] for gare in Gares}

liste_terminus_gennevilliers = ['Gennevilliers', "L'Etang", 'Verdure']
liste_terminus_epinay = ['La Ferme', 'Les Fiancés', 'Les Mariniers']
liste_terminus_navettes = ['La Ferme', 'Les Fiancés']

TypeHoraire = [
    {
        'titre': 'Samedi (1 train)',
        'nTrains': 1,
        'temps_entre_gares': 8,
        'terminus_gennevilliers': 'Gennevilliers',
        'terminus_epinay': 'Les Mariniers',
        'temps_arret_terminus': 0,
        'depart_limite_premier_train_depot': '14:30:00',
        'temps_depot_ferme': 25,
        'depart_T1_ferme': '15:00:00',
        'temps_entre_trains': 32,
        'heure_limite_arrivee_ferme': '19:10:00',
        'nNavettes': 0,
        'terminus_navettes': 'La Ferme'
    },
    {
        'titre': 'Dimanche (2 trains)',
        'nTrains': 2,
        'temps_entre_gares': 8,
        'terminus_gennevilliers': 'Gennevilliers',
        'terminus_epinay': 'Les Mariniers',
        'temps_arret_terminus': 0,
        'depart_limite_premier_train_depot': '14:30:00',
        'temps_depot_ferme': 25,
        'depart_T1_ferme': '15:00:00',
        'temps_entre_trains': 32,
        'heure_limite_arrivee_ferme': '19:10:00',
        'nNavettes': 0,
        'terminus_navettes': 'La Ferme'
    },
    {
        'titre': 'JPO (3 trains)',
        'nTrains': 3,
        'temps_entre_gares': 8,
        'terminus_gennevilliers': 'Gennevilliers',
        'terminus_epinay': 'Les Mariniers',
        'temps_arret_terminus': 0,
        'depart_limite_premier_train_depot': '14:00:00',
        'temps_depot_ferme': 8,
        'depart_T1_ferme': '15:00:00',
        'temps_entre_trains': 32,
        'heure_limite_arrivee_ferme': '19:10:00',
        'nNavettes': 2,
        'terminus_navettes': 'La Ferme'
    },
    {
        'titre': 'JPAT 2017 (2 trains + CFC mini)',
        'nTrains': 2,
        'temps_entre_gares': 8,
        'terminus_gennevilliers': 'Gennevilliers',
        'terminus_epinay': 'Les Mariniers',
        'temps_arret_terminus': 0,
        'depart_limite_premier_train_depot': '14:00:00',
        'temps_depot_ferme': 8,
        'depart_T1_ferme': '14:28:00',
        'temps_entre_trains': 32,
        'heure_limite_arrivee_ferme': '19:10:00',
        'nNavettes': 2,
        'terminus_navettes': 'Les Fiancés'
    }
]