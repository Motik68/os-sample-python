import datetime

from definitions import *


def decodage_type_horaire(type_horaire):
	"""
	Décode un type_horaire pour le passer à calcul_horaire()
	
	:param type_horaire: type d'horaire
	:type type_horaire: dict
	:return: paramètres à passer à calcul_horaire()
	:rtype: dict
	"""
	
	return {
        'titre': type_horaire['titre'],
        'nTrains': type_horaire['nTrains'],
        'temps_entre_gares': datetime.timedelta(minutes=type_horaire['temps_entre_gares']),
        'terminus_gennevilliers': type_horaire['terminus_gennevilliers'],
        'terminus_epinay': type_horaire['terminus_epinay'],
        'temps_arret_terminus': datetime.timedelta(minutes=type_horaire['temps_arret_terminus']),
        'depart_limite_premier_train_depot': datetime.datetime(1970, 1, 1, type_horaire['depart_limite_premier_train_depot'].split(':')[0], type_horaire['depart_limite_premier_train_depot'].split(':')[1]),
        'temps_depot_ferme': datetime.timedelta(minutes=type_horaire['temps_depot_ferme']),
        'depart_T1_ferme': datetime.datetime(1970, 1, 1, type_horaire['depart_T1_ferme'].split(':')[0], type_horaire['depart_T1_ferme'].split(':')[1]),
        'temps_entre_trains': datetime.timedelta(minutes=type_horaire['temps_entre_trains']),
        'heure_limite_arrivee_ferme': datetime.datetime(1970, 1, 1, type_horaire['heure_limite_arrivee_ferme'].split(':')[0], type_horaire['heure_limite_arrivee_ferme'].split(':')[1]),
        'nNavettes': type_horaire['nNavettes'],
        'terminus_navettes': type_horaire['terminus_navettes']
	}

def calcul_horaire_partiel(train, parcours, heure_debut, temps_entre_gares, terminus, temps_arret_terminus, horaire):
    """
    Calcule une portion d'horaire d'un train

    :param train: numéro du train
    :type train: int
    :param parcours: liste des noms des gares de la portion de parcours à calculer
    :type parcours: list
    :param heure_debut: heure (avec date au 01/01/2000) de passage à la première gare du parcours
    :type heure_debut: datetime.datetime
    :param temps_entre_gares: temps entre deux gares
    :type temps_entre_gares: datetime.timedelta
    :param temps_arret_terminus: temps passé aux terminus
    :type temps_arret_terminus: datetime.timedelta
    :param horaire: horaire global
    :type horaire: dict
    :return: heure de passage à la première gare du parcours suivant
    :rtype: datetime.datetime
    """

    heure = heure_debut

    for i, gare in enumerate(parcours):
        if i + 1 < len(parcours):  # l'horaire de la dernière gare n'est pas ajouté, elle sert uniquement à retourner le bon temps de parcours
            horaire['train'][train].append({'heure': heure, 'lieu': gare})
            if temps_arret_terminus and gare in terminus:
                heure += temps_arret_terminus
                horaire['train'][train].append({'heure': heure, 'lieu': gare})
            heure += temps_entre_gares * abs(position_gare[parcours[i + 1]] - position_gare[gare])
        else:
            break
    return heure


def calcul_horaire(parametres):
    """
    Calcule l'horaire complet d'une journée

    :param parametres: paramètres de l'horaire à calculer
    :type dict
    :return: horaire global
    :rtype dict[str, dict[int, list[dict[datetime, str]]]]
    """

    horaire = {
        'train': {},
        'navette': {}
    }

    # Lecture des paramètres
    nTrains = parametres['nTrains']
    temps_entre_gares = parametres['temps_entre_gares']
    terminus_gennevilliers = parametres['terminus_gennevilliers']
    terminus_epinay = parametres['terminus_epinay']
    temps_arret_terminus = parametres['temps_arret_terminus']
    depart_limite_premier_train_depot = parametres['depart_limite_premier_train_depot']
    temps_depot_ferme = parametres['temps_depot_ferme']
    depart_T1_ferme = parametres['depart_T1_ferme']
    temps_entre_trains = parametres['temps_entre_trains']
    heure_limite_arrivee_ferme = parametres['heure_limite_arrivee_ferme']
    nNavettes = parametres['nNavettes']
    terminus_navettes = parametres['terminus_navettes']

    terminus = (terminus_gennevilliers, terminus_epinay)

    # Segmentation de la ligne
    temps_demitourEpinay = 2 * temps_entre_gares * (Ligne[iArret[terminus_epinay]]['position'] - Ligne[iArret['La Ferme']]['position'])
    demitourEpinay = []
    for gare in Gares[iGare['La Ferme']:iGare[terminus_epinay]]:
        demitourEpinay.append(gare['nom'])
    for gare in Gares[iGare[terminus_epinay]:iGare['La Ferme'] - 1:-1]:
        demitourEpinay.append(gare['nom'])

    temps_gennevilliers_ferme = temps_entre_gares * (Ligne[iArret['La Ferme']]['position'] - Ligne[iArret[terminus_gennevilliers]]['position'])
    temps_demitourGennevilliers = 2 * temps_gennevilliers_ferme
    demiTourGennevilliers = []
    quartdetourGennevilliersFerme = []
    for gare in Gares[iGare['La Ferme']:iGare[terminus_gennevilliers]:-1]:
        demiTourGennevilliers.append(gare['nom'])
    for gare in Gares[iGare[terminus_gennevilliers]:iGare['La Ferme'] + 1]:
        demiTourGennevilliers.append(gare['nom'])
        quartdetourGennevilliersFerme.append(gare['nom'])

    # Calcul des trains
    for train in range(1, nTrains + 1):
        horaire['train'][train] = []
        heure = depart_T1_ferme + (train - 1) * temps_entre_trains
        if heure - temps_demitourGennevilliers - temps_demitourEpinay - temps_depot_ferme >= depart_limite_premier_train_depot:
            # on a le temps de faire un tour complet avant le départ de la ferme
            heure = heure - temps_demitourGennevilliers - temps_demitourEpinay
            horaire['train'][train].append({'heure': heure - temps_depot_ferme, 'lieu': 'Dépôt'})
        elif heure - temps_demitourGennevilliers - temps_depot_ferme >= depart_limite_premier_train_depot:
            # on a le temps de faire un demi-tour à Gennevilliers avant le départ de la ferme
            horaire['train'][train].append({'heure': heure - temps_demitourGennevilliers - temps_depot_ferme, 'lieu': 'Dépôt'})
            heure = calcul_horaire_partiel(train, demiTourGennevilliers, heure - temps_demitourGennevilliers, temps_entre_gares, terminus, temps_arret_terminus, horaire)
        elif heure - temps_depot_gennevilliers - temps_gennevilliers_ferme >= depart_limite_premier_train_depot:
            # on a le temps de partir de Gennevilliers avant le départ de la ferme
            horaire['train'][train].append({'heure': heure - temps_gennevilliers_ferme - temps_depot_gennevilliers, 'lieu': 'Dépôt'})
            heure = calcul_horaire_partiel(train, quartdetourGennevilliersFerme, heure - temps_gennevilliers_ferme, temps_entre_gares, terminus, temps_arret_terminus, horaire)
        else:
            horaire['train'][train].append({'heure': heure - temps_depot_ferme, 'lieu': 'Dépôt'}) # On part directement à la ferme

        while True: # calcul itératif de l'horaire : demi-tour Epinay puis demi-tour Gennevilliers.
                    # Arrêt quand le demi-tour suivant dépasserait l'heure limite d'arrivée à la ferme
            heure = calcul_horaire_partiel(train, demitourEpinay, heure, temps_entre_gares, terminus, temps_arret_terminus, horaire)
            if heure + temps_demitourGennevilliers > heure_limite_arrivee_ferme:
                break

            heure = calcul_horaire_partiel(train, demiTourGennevilliers, heure, temps_entre_gares, terminus, temps_arret_terminus, horaire)
            if heure + temps_demitourEpinay > heure_limite_arrivee_ferme:
                break

        horaire['train'][train].append({'heure': heure, 'lieu': 'La Ferme'})
        horaire['train'][train].append({'heure': heure + temps_ferme_depot, 'lieu': 'Dépôt'})

    # Correction de l'heure de départ du dépôt pour tous les trains allant à la Ferme sauf le premier à partir
    for heure, train in sorted([(horaire['train'][train][0]['heure'], train) for train in range(1, nTrains + 1) if horaire['train'][train][1]['lieu'] == 'La Ferme'])[1:]:
        horaire['train'][train][0] = {'heure': heure + temps_depot_ferme - temps_entre_gares, 'lieu': 'Dépôt'}

    # Calcul des navettes
    if nNavettes > 0:
        passagesFerme = sorted([arret['heure'] for train in range(1, nTrains + 1) for arret in horaire['train'][train] if arret['lieu'] == 'La Ferme'])
        passagesFerme = passagesFerme[:-nTrains] # Pas de navette pour les derniers retours à la Ferme

        if nTrains < N_PREMIERE_NAVETTE:
            nPremiereNavette = N_PREMIERE_NAVETTE
        else:
            nPremiereNavette = nTrains + 1

        for navette in range(nPremiereNavette, nPremiereNavette + nNavettes):
            horaire['navette'][navette] = []
        navette = nPremiereNavette

        for trajet in range(len(passagesFerme)): # Une navette à chaque fois qu'un train passe à la Ferme
            if len(horaire['navette'][navette]) > 0 and horaire['navette'][navette][-1]['heure'] >= passagesFerme[trajet] - temps_navette_ferme_avant_train - temps_navette_depot_ferme:
                continue # Si la navette n'est pas encore revenue, on essaie de la faire partir au tour suivant
            else:
                horaire['navette'][navette].append(
                    {'heure': passagesFerme[trajet] - temps_navette_ferme_avant_train - temps_navette_depot_ferme, 'lieu': 'Dépôt'})
                horaire['navette'][navette].append(
                    {'heure': passagesFerme[trajet] - temps_navette_ferme_avant_train, 'lieu': 'La Ferme'})

                if terminus_navettes == 'Les Fiancés':
                    horaire['navette'][navette].append(
                        {'heure': passagesFerme[trajet] - temps_navette_ferme_avant_train + temps_entre_gares, 'lieu': 'Les Fiancés'})
                    horaire['navette'][navette].append(
                        {'heure': passagesFerme[trajet] + temps_navette_ferme_apres_train + temps_entre_gares, 'lieu': 'Les Fiancés'})
                    horaire['navette'][navette].append(
                        {'heure': passagesFerme[trajet] + temps_navette_ferme_apres_train + 2 * temps_entre_gares, 'lieu': 'La Ferme'})
                    horaire['navette'][navette].append(
                        {'heure': passagesFerme[trajet] + temps_navette_ferme_apres_train + temps_navette_depot_ferme + 2 * temps_entre_gares, 'lieu': 'Dépôt'})

                else: # Terminus des navettes à la Ferrme
                    horaire['navette'][navette].append(
                        {'heure': passagesFerme[trajet] + temps_navette_ferme_apres_train, 'lieu': 'La Ferme'})
                    horaire['navette'][navette].append(
                        {'heure': passagesFerme[trajet] + temps_navette_ferme_apres_train + temps_navette_depot_ferme, 'lieu': 'Dépôt'})
            navette += 1
            if navette >= nPremiereNavette + nNavettes:
                navette = nPremiereNavette

    # Affichage dans la console
    for train in horaire['train']:
        print('\nT' + str(train))
        for arret in horaire['train'][train]:
            print(arret['heure'].strftime('%H:%M'), arret['lieu'])
    if nNavettes > 0:
        for navette in horaire['navette']:
            print('\nNavette T' + str(navette))
            for arret in horaire['navette'][navette]:
                print(arret['heure'].strftime('%H:%M'), arret['lieu'])

    return horaire
