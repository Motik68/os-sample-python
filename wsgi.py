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
	type_horaire = request.args.get('type', 0, type=int)

	horaire = calcul_horaire(decodage_type_horaire(TypeHoraire[type_horaire]))
	tableau_url, pdf_url = tableau_de_marche(horaire, TypeHoraire[type_horaire]['titre'])
	return render_template('tableau_marche.html', tableau_marche=tableau_url, tableau_marche_pdf=pdf_url)
 
if __name__ == '__main__':
    application.debug = True
    application.run()