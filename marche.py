import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.dates import DateFormatter
from matplotlib.dates import HourLocator

# import mpld3

from definitions import *


def tableau_de_marche(horaire, titre):

    legende = []
    plt.close()
    axes = plt.subplot()

    nTrains = len(horaire['train'])
    nNavettes = len(horaire['navette'])

    for train in horaire['train']:
        xTrain = [arret['heure'] for arret in horaire['train'][train]]
        yTrain = [Ligne[iArret[arret['lieu']]]['position'] for arret in horaire['train'][train]]

        plt.plot(xTrain, yTrain)

        for xy in zip(xTrain, yTrain):
            axes.annotate('%s' % xy[0].strftime('%M'), xy=xy, textcoords='data')

        legende.append('T' + str(train))

    # Graphique navettes
    if nNavettes > 0:
        for navette in horaire['navette']:
            xNavette = [arret['heure'] for arret in horaire['navette'][navette]]
            yNavette = [Ligne[iArret[arret['lieu']]]['position'] for arret in horaire['navette'][navette]]

            plt.plot(xNavette, yNavette)

            # for xy in zip(xNavette, yNavette):
            #     axes.annotate('%s' % xy[0].strftime('%M'), xy=xy, textcoords='data')

            legende.append('Navette T' + str(navette))

    # Formatage général du tableau de marche
    figure = plt.gcf()
    figure.set_size_inches(11.69, 8.27)  # mise au format A4
    figure.canvas.set_window_title('Tableau de marche CFC - ' + titre)

    axes.xaxis.set_major_locator(HourLocator())
    axes.xaxis.set_major_formatter(DateFormatter('%H:%M'))
    axes.tick_params(labelbottom='on', labeltop='on')

    # plt.yticks(list(yGare.values()), list(yGare.keys()))
    plt.yticks([arret['position'] for arret in Ligne if arret['gare']], [arret['nom'] for arret in Ligne if arret['gare']])
    axes.set_yticks([Ligne[iArret['Dépôt']]['position']], minor=True)
    axes.yaxis.set_minor_formatter(ticker.FixedFormatter(['Dépôt']))

    plt.grid(which='major')
    plt.grid(which='minor', linestyle='--')
    if nTrains > 1 or nNavettes > 0:
        plt.legend(legende, loc='upper left')
    # with PdfPages('horaire.pdf') as pdf:
    #     pdf.savefig()
    figure.suptitle('Chemin de Fer des Chanteraines', fontsize=24, fontweight='bold')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
	# plt.show()
    # mpld3.show()

    # print(temps_demitourEpinay)
    # print(temps_demitourGennevilliers)

	plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)