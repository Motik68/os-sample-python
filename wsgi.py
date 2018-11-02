from flask import Flask, render_template, request
from graph import build_graph
from definitions import *
from horaire import decodage_type_horaire, calcul_horaire
from marche import tableau_de_marche
 
application = Flask(__name__)
 
@application.route("/")
def hello():
    return "Hello JF!"

@application.route('/graphs')
def graphs():
    #These coordinates could be stored in DB
    x1 = [0, 1, 2, 3, 4]
    y1 = [10, 30, 40, 5, 50]
    x2 = [0, 1, 2, 3, 4]
    y2 = [50, 30, 20, 10, 50]
    x3 = [0, 1, 2, 3, 4]
    y3 = [0, 30, 10, 5, 30]
 
    graph1_url = build_graph(x1,y1);
    graph2_url = build_graph(x2,y2);
    graph3_url = build_graph(x3,y3);
 
    return render_template('graphs.html',
    graph1=graph1_url,
    graph2=graph2_url,
    graph3=graph3_url)

@application.route('/cfc')
def horaireCFC():
	type_horaire = request.args.get('type', type=int)
	liste_types = [type['titre'] for type in TypeHoraire]
	parametres = {}
	
	if type_horaire == None:
		type_horaire = 0
		parametres['titre'] = request.args.get('titre', "")
		parametres['nTrains'] = request.args.get('nTrains', type=int)
		parametres['temps_entre_gares'] = request.args.get('temps_entre_gares', type=int)
		parametres['terminus_gennevilliers'] = request.args.get('terminus_gennevilliers')
		parametres['terminus_epinay'] = request.args.get('terminus_epinay')
		parametres['temps_arret_terminus'] = request.args.get('temps_arret_terminus', type=int)
		parametres['depart_limite_premier_train_depot'] = request.args.get('depart_limite_premier_train_depot')
		parametres['temps_depot_ferme'] = request.args.get('temps_depot_ferme', type=int)
		parametres['depart_T1_ferme'] = request.args.get('depart_T1_ferme')
		parametres['temps_entre_trains'] = request.args.get('temps_entre_trains', type=int)
		parametres['heure_limite_arrivee_ferme'] = request.args.get('heure_limite_arrivee_ferme')
		parametres['nNavettes'] = request.args.get('nNavettes', type=int)
		parametres['terminus_navettes'] = request.args.get('terminus_navettes')
	else:
		parametres = TypeHoraire[type_horaire].copy()

	horaire = calcul_horaire(decodage_type_horaire(parametres))
	tableau_url, pdf_url = tableau_de_marche(horaire, parametres['titre'])
	return render_template('tableau_marche.html', tableau_marche=tableau_url, tableau_marche_pdf=pdf_url, 
							types=liste_types, choix_type=type_horaire, parametres=parametres)
 
if __name__ == '__main__':
    application.debug = True
    application.run()