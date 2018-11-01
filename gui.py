import wx
import wx.lib.masked as masked
import matplotlib.pyplot as plt

from definitions import *
from horaire import calcul_horaire
from marche import tableau_de_marche
import info_temps_reel

# TODO Horaire par train
# TODO horaire par gare
# TODO tableau de marche par train
# TODO affichage temps réel sur l'écran de la Ferme
# TODO horaire temps réel sur l'écran de la Ferme : connecter au site web (nombre de trains et position en temps réel)
# TODO un appui sur la touche "Entrée" lance le calcul
# TODO Importer les valeurs initiales d'un fichier JSON dans un dictionnaire
# TODO Impression directe du tableau de marche


class Fenetre(wx.Frame):
    def __init__(self, titre):
        self.titre = titre

        wx.Frame.__init__(self, None, title=titre, size=(1000, 700))
        self.CreateStatusBar()

        # Création du menu
        filemenu= wx.Menu()

        menuAPropos = filemenu.Append(wx.ID_ABOUT, "&A propos"," Informations sur ce programme")
        filemenu.AppendSeparator()
        menuQuitter = filemenu.Append(wx.ID_EXIT,"&Quitter"," Quitter le programme")

        # Création de la barre de menu
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&Fichier")  # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Evènements de menu
        self.Bind(wx.EVT_MENU, self.on_a_propos, menuAPropos)
        self.Bind(wx.EVT_MENU, self.on_sortir, menuQuitter)

        # Création du panneau et de ses composants
        self.panel = wx.Panel(self, wx.ID_ANY)

        label_type_horaire                  = wx.StaticText(self.panel, wx.ID_ANY, "Type d'horaire :")
        label_nTrains                       = wx.StaticText(self.panel, wx.ID_ANY, 'Nombre de trains :')
        label_temps_entre_gares             = wx.StaticText(self.panel, wx.ID_ANY, 'Temps entre gares (minutes) :')
        label_terminus                      = wx.StaticText(self.panel, wx.ID_ANY, 'Terminus :')
        label_temps_terminus                = wx.StaticText(self.panel, wx.ID_ANY, 'Temps aux terminus (minutes) :')
        label_limite_depart_depot           = wx.StaticText(self.panel, wx.ID_ANY, 'Départ du dépôt après :')
        label_temps_depot_ferme             = wx.StaticText(self.panel, wx.ID_ANY, 'Temps entre le dépôt et la Ferme (minutes) :')
        label_depart_ferme                  = wx.StaticText(self.panel, wx.ID_ANY, 'Départ T1 de la Ferme :')
        label_temps_entre_trains            = wx.StaticText(self.panel, wx.ID_ANY, 'Temps entre trains (minutes) :')
        label_limite_arrivee_ferme          = wx.StaticText(self.panel, wx.ID_ANY, 'Terminus à la Ferme avant :')
        label_nombre_navettes               = wx.StaticText(self.panel, wx.ID_ANY, 'Nombre de navettes :')
        label_terminus_navettes             = wx.StaticText(self.panel, wx.ID_ANY, 'Terminus des navettes :')

        self.input_type_horaire             = wx.ComboBox(self.panel, wx.ID_ANY, style=wx.CB_READONLY, choices=[TypeHoraire[i]['titre'] for i in range(len(TypeHoraire))])
        self.input_nTrains                  = wx.SpinCtrl(self.panel, wx.ID_ANY, min=1, max=9, size=(50, wx.DefaultSize.GetHeight()))
        self.input_temps_entre_gares        = wx.SpinCtrl(self.panel, wx.ID_ANY, min=1, max=20, size=(50, wx.DefaultSize.GetHeight()))
        self.input_terminus_gennevilliers   = wx.ComboBox(self.panel, wx.ID_ANY, style=wx.CB_READONLY, choices=liste_terminus_gennevilliers)
        self.input_terminus_epinay          = wx.ComboBox(self.panel, wx.ID_ANY, style=wx.CB_READONLY, choices=liste_terminus_epinay)
        self.input_temps_terminus           = wx.SpinCtrl(self.panel, wx.ID_ANY, min=0, max=20, size=(50, wx.DefaultSize.GetHeight()))
        self.input_limite_depart_depot      = masked.TimeCtrl(self.panel, format='24HHMM', spinButton=None)
        self.input_temps_depot_ferme        = wx.SpinCtrl(self.panel, wx.ID_ANY, min=1, max=60, size=(50, wx.DefaultSize.GetHeight()))
        self.input_depart_ferme             = masked.TimeCtrl(self.panel, format='24HHMM')
        self.input_temps_entre_trains       = wx.SpinCtrl(self.panel, wx.ID_ANY, min=1, max=60, size=(50, wx.DefaultSize.GetHeight()))
        self.input_limite_arrivee_ferme     = masked.TimeCtrl(self.panel, format='24HHMM')
        self.input_nombre_navettes          = wx.SpinCtrl(self.panel, wx.ID_ANY, min=0, max=9, size=(50, wx.DefaultSize.GetHeight()))
        self.input_terminus_navettes        = wx.ComboBox(self.panel, wx.ID_ANY, style=wx.CB_READONLY, choices=liste_terminus_navettes)

        self.input_type_horaire.SetSelection(0)
        self.Bind(wx.EVT_COMBOBOX, self.on_type_horaire, self.input_type_horaire)

        bouton_marche = wx.Button(self.panel, wx.ID_ANY, 'Tableau de marche')
        bouton_marche.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.on_marche, bouton_marche)

        bouton_position = wx.Button(self.panel, wx.ID_ANY, 'Position des trains')
        self.Bind(wx.EVT_BUTTON, self.on_position, bouton_position)

        bouton_fermer = wx.Button(self.panel, wx.ID_ANY, 'Fermer')
        self.Bind(wx.EVT_BUTTON, self.on_fermer, bouton_fermer)

        sizerGrille = wx.FlexGridSizer(2)
        sizer_boutons = wx.BoxSizer(wx.HORIZONTAL)

        sizerGrille.Add(label_type_horaire, 0, wx.TOP|wx.LEFT, 5)
        sizerGrille.Add(self.input_type_horaire, 1, wx.TOP|wx.RIGHT, 5)

        sizerGrille.Add(label_nTrains, 0, wx.TOP|wx.LEFT, 5)
        sizerGrille.Add(self.input_nTrains, 1, wx.TOP|wx.RIGHT, 5)

        sizerGrille.Add(label_temps_entre_gares, 0, wx.TOP|wx.LEFT, 5)
        sizerGrille.Add(self.input_temps_entre_gares, 1, wx.TOP|wx.RIGHT, 5)

        sizerGrille.Add(label_terminus, 0, wx.TOP|wx.LEFT, 5)
        sizerGrille.Add(self.input_terminus_gennevilliers, 1, wx.TOP|wx.RIGHT, 5)
        sizerGrille.Add(wx.StaticText(self.panel, -1, ''), 0, wx.TOP|wx.LEFT, 5)
        sizerGrille.Add(self.input_terminus_epinay, 1, wx.TOP|wx.RIGHT, 5)

        sizerGrille.Add(label_temps_terminus, 0, wx.TOP|wx.LEFT, 5)
        sizerGrille.Add(self.input_temps_terminus, 1, wx.TOP|wx.RIGHT, 5)

        sizerGrille.Add(label_limite_depart_depot, 0, wx.TOP|wx.LEFT, 5)
        sizerGrille.Add(self.input_limite_depart_depot, 1, wx.TOP|wx.RIGHT, 5)

        sizerGrille.Add(label_temps_depot_ferme, 0, wx.TOP|wx.LEFT, 5)
        sizerGrille.Add(self.input_temps_depot_ferme, 1, wx.TOP|wx.RIGHT, 5)

        sizerGrille.Add(label_depart_ferme, 0, wx.TOP|wx.LEFT, 5)
        sizerGrille.Add(self.input_depart_ferme, 1, wx.TOP|wx.RIGHT, 5)

        sizerGrille.Add(label_temps_entre_trains, 0, wx.TOP|wx.LEFT, 5)
        sizerGrille.Add(self.input_temps_entre_trains, 1, wx.TOP|wx.RIGHT, 5)

        sizerGrille.Add(label_limite_arrivee_ferme, 0, wx.TOP|wx.LEFT, 5)
        sizerGrille.Add(self.input_limite_arrivee_ferme, 1, wx.TOP|wx.RIGHT, 5)

        sizerGrille.Add(label_nombre_navettes, 0, wx.TOP|wx.LEFT, 5)
        sizerGrille.Add(self.input_nombre_navettes, 1, wx.TOP|wx.RIGHT, 5)

        sizerGrille.Add(label_terminus_navettes, 0, wx.TOP|wx.LEFT, 5)
        sizerGrille.Add(self.input_terminus_navettes, 1, wx.TOP|wx.RIGHT, 5)

        sizer_boutons.Add(bouton_marche, 0, wx.ALL, 5)
        sizer_boutons.Add(bouton_position, 0, wx.ALL, 5)
        sizer_boutons.Add(bouton_fermer, 0, wx.ALL, 5)
        sizerGrille.Add(sizer_boutons, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.panel.SetSizer(sizerGrille)
        sizerGrille.Fit(self)

        self.remplissage_formulaire()
        self.Show(True)

    def remplissage_formulaire(self):
        i = self.input_type_horaire.GetSelection()

        self.input_nTrains.SetValue(TypeHoraire[i]['nTrains'])
        self.input_temps_entre_gares.SetValue(TypeHoraire[i]['temps_entre_gares'])
        self.input_terminus_gennevilliers.SetSelection(self.input_terminus_gennevilliers.FindString(TypeHoraire[i]['terminus_gennevilliers']))
        self.input_terminus_epinay.SetSelection(self.input_terminus_epinay.FindString(TypeHoraire[i]['terminus_epinay']))
        self.input_temps_terminus.SetValue(TypeHoraire[i]['temps_arret_terminus'])
        self.input_limite_depart_depot.SetValue(TypeHoraire[i]['depart_limite_premier_train_depot'])
        self.input_temps_depot_ferme.SetValue(TypeHoraire[i]['temps_depot_ferme'])
        self.input_depart_ferme.SetValue(TypeHoraire[i]['depart_T1_ferme'])
        self.input_temps_entre_trains.SetValue(TypeHoraire[i]['temps_entre_trains'])
        self.input_limite_arrivee_ferme.SetValue(TypeHoraire[i]['heure_limite_arrivee_ferme'])
        self.input_nombre_navettes.SetValue(TypeHoraire[i]['nNavettes'])
        self.input_terminus_navettes.SetSelection(self.input_terminus_navettes.FindString(TypeHoraire[i]['terminus_navettes']))
    
    def lecture_formulaire(self):
        parametres = {
            'titre': frame.input_type_horaire.GetValue(),
            'nTrains': frame.input_nTrains.GetValue(),
            'temps_entre_gares': datetime.timedelta(minutes=frame.input_temps_entre_gares.GetValue()),
            'terminus_gennevilliers': frame.input_terminus_gennevilliers.GetStringSelection(),
            'terminus_epinay': frame.input_terminus_epinay.GetStringSelection(),
            'temps_arret_terminus': datetime.timedelta(minutes=frame.input_temps_terminus.GetValue()),
            'depart_limite_premier_train_depot': datetime.datetime(
                1970, 1, 1, frame.input_limite_depart_depot.GetWxDateTime().GetHour(),
                frame.input_limite_depart_depot.GetWxDateTime().GetMinute()),  # Date bidon pour permettre l'addition avec timedelta
            'temps_depot_ferme': datetime.timedelta(minutes=frame.input_temps_depot_ferme.GetValue()),
            'depart_T1_ferme': datetime.datetime(
                1970, 1, 1, frame.input_depart_ferme.GetWxDateTime().GetHour(),
                frame.input_depart_ferme.GetWxDateTime().GetMinute()),  # Date bidon pour permettre l'addition avec timedelta
            'temps_entre_trains': datetime.timedelta(minutes=frame.input_temps_entre_trains.GetValue()),
            'heure_limite_arrivee_ferme': datetime.datetime(
                1970, 1, 1, frame.input_limite_arrivee_ferme.GetWxDateTime().GetHour(),
                frame.input_limite_arrivee_ferme.GetWxDateTime().GetMinute()),  # Date bidon pour permettre l'addition avec timedelta
            'nNavettes': frame.input_nombre_navettes.GetValue(),
            'terminus_navettes': frame.input_terminus_navettes.GetStringSelection()
        }

        return parametres


    def on_type_horaire(self, e):
        self.remplissage_formulaire()

    def on_a_propos(self, e):
        dlg = wx.MessageDialog( self, "Calcul des horaires du CFC", "A propos")
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def on_sortir(self, e):
        plt.close()
        self.Close(True)  # Close the frame.

    def on_marche(self, event):
        horaire = calcul_horaire(self.lecture_formulaire())
        tableau_de_marche(horaire, self.titre)

    def on_position(self, event):
        horaire = calcul_horaire(self.lecture_formulaire())
        info_temps_reel.position(horaire)

    def on_fermer(self, event):
        self.on_sortir(event)


app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
frame = Fenetre('Horaire CFC')
app.MainLoop()