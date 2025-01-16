from fpdf import FPDF
import pandas as pd
import matplotlib.pyplot as plt
import os
from data_manager import AgriculturalDataManager

class AgriculturalReportGenerator:
    def __init__(self, data_manager):
        """Initialise le générateur de rapports avec le gestionnaire de données."""
        self.data_manager = data_manager

    def generate_parcelle_report(self, parcelle_id, output_file="rapport_parcelle.pdf"):
        """Génère un rapport PDF pour une parcelle donnée."""
        data = self.data_manager.prepare_features()
        parcelle_data = data[data['parcelle_id'] == parcelle_id]

        # Créer un PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Ajouter un titre
        pdf.cell(200, 10, txt=f"Rapport pour la parcelle {parcelle_id}", ln=True, align="C")

        # Ajouter des informations sur la parcelle
        pdf.cell(200, 10, txt="Informations sur la parcelle :", ln=True)
        pdf.cell(200, 10, txt=f"Culture : {parcelle_data['culture'].iloc[0]}", ln=True)
        pdf.cell(200, 10, txt=f"Rendement moyen : {parcelle_data['rendement'].mean():.2f} tonnes/ha", ln=True)

        # Ajouter un graphique (exemple : rendement au fil du temps)
        plt.figure()
        plt.plot(parcelle_data['date'], parcelle_data['rendement'], label="Rendement")
        plt.title(f"Rendement pour la parcelle {parcelle_id}")
        plt.xlabel("Date")
        plt.ylabel("Rendement (tonnes/ha)")
        plt.legend()
        plot_path = "rendement_plot.png"
        plt.savefig(plot_path)
        plt.close()

        # Ajouter le graphique au PDF
        pdf.image(plot_path, x=10, y=50, w=180)

        # Ajouter une carte (optionnel)
        if os.path.exists("carte_parcelles.png"):
            pdf.add_page()
            pdf.cell(200, 10, txt="Carte des parcelles :", ln=True)
            pdf.image("carte_parcelles.png", x=10, y=20, w=180)

        # Sauvegarder le PDF
        pdf.output(output_file)
        print(f"Rapport généré avec succès : {output_file}")

        # Nettoyer les fichiers temporaires
        if os.path.exists(plot_path):
            os.remove(plot_path)

            from data_manager import AgriculturalDataManager

# Initialisation du gestionnaire de données
data_manager = AgriculturalDataManager()
data_manager.load_data()

# Initialisation du générateur de rapports
report_generator = AgriculturalReportGenerator(data_manager)

# Générer un rapport pour une parcelle spécifique
parcelle_id = 'P001'  # Remplacez par l'ID d'une parcelle existante
report_generator.generate_parcelle_report(parcelle_id)

from selenium import webdriver
import time

def save_folium_map_as_image(map_object, output_file="carte_parcelles.png"):
    """Exporte une carte Folium en image."""
    map_object.save("map.html")  # Sauvegarder la carte en HTML
    
    # Utiliser Selenium pour capturer une image de la carte
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Exécuter en mode sans tête
    driver = webdriver.Chrome(options=options)
    driver.get(f"file://{os.path.abspath('map.html')}")
    time.sleep(5)  # Attendre que la carte se charge
    driver.save_screenshot(output_file)
    driver.quit()

    # Nettoyer le fichier HTML temporaire
    if os.path.exists("map.html"):
        os.remove("map.html")