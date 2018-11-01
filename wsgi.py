# from flask import Flask
# application = Flask(__name__)

# @application.route("/")
# def hello():
    # return "Hello JF!"

# if __name__ == "__main__":
    # application.run()


	
from flask import Flask, render_template
from graph import build_graph
from definitions import *
from horaire import calcul_horaire
from marche import tableau_de_marche
 
application = Flask(__name__)
 
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
	horaire = calcul_horaire({
        'titre': 'Samedi (1 train)',
        'nTrains': 1,
        'temps_entre_gares': datetime.timedelta(minutes=8),
        'terminus_gennevilliers': 'Gennevilliers',
        'terminus_epinay': 'Les Mariniers',
        'temps_arret_terminus': datetime.timedelta(minutes=0),
        'depart_limite_premier_train_depot': datetime.datetime(1970, 1, 1, 14, 30),
        'temps_depot_ferme': datetime.timedelta(minutes=25),
        'depart_T1_ferme': datetime.datetime(1970, 1, 1, 15, 00),
        'temps_entre_trains': datetime.timedelta(minutes=32),
        'heure_limite_arrivee_ferme': datetime.datetime(1970, 1, 1, 19, 10),
        'nNavettes': 0,
        'terminus_navettes': 'La Ferme'
	})
	tableau_url = tableau_de_marche(horaire, horaire['titre'])
	return render_template('tableau_marche.html', tableau_marche=tableau_url)
 
if __name__ == '__main__':
    application.debug = True
    application.run()