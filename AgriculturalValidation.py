import numpy as np
from sklearn.metrics import mean_squared_error

class AgriculturalValidation:
    def __init__(self, analyzer):
        """Initialise le système de validation avec l'analyseur."""
        self.analyzer = analyzer

    def validate_recommendations(self, parcelle_id, actual_yields):
        """Valide les recommandations en comparant les prédictions aux rendements réels."""
        predictions = self.analyzer.predict_yield(parcelle_id)
        mse = mean_squared_error(actual_yields, predictions)
        print(f"Erreur quadratique moyenne pour la parcelle {parcelle_id} : {mse:.2f}")
        return mse
    
    # Exemple de données réelles (à remplacer par vos données)
actual_yields = np.random.uniform(10, 20, size=10)  # Rendements réels

# Validation des recommandations
validation = AgriculturalValidation(analyzer)
mse = validation.validate_recommendations('P001', actual_yields)

class AgriculturalAnalyzer:
    def __init__(self, data_manager):
        """Initialise l'analyseur avec le gestionnaire de données."""
        self.data_manager = data_manager

    def calculate_risk_metrics(self, parcelle_id):
        """Calcule les métriques de risque pour une parcelle donnée."""
        data = self.data_manager.prepare_features()
        parcelle_data = data[data['parcelle_id'] == parcelle_id]

        # Exemple de métrique de risque : probabilité de stress hydrique élevé
        risk_metric = np.mean(parcelle_data['stress_hydrique'] > 0.15)  # Seuil arbitraire
        return risk_metric

    def identify_high_risk_parcelles(self, threshold=0.5):
        """Identifie les parcelles à haut risque."""
        data = self.data_manager.prepare_features()
        high_risk_parcelles = data[data['stress_hydrique'] > threshold]
        return high_risk_parcelles
    
    high_risk_parcelles = analyzer.identify_high_risk_parcelles()
print("Parcelles à haut risque :")
print(high_risk_parcelles[['parcelle_id', 'stress_hydrique']])

import requests

class WeatherAPI:
    def __init__(self, api_key):
        """Initialise l'API météorologique."""
        self.api_key = api_key

    def get_weather_data(self, latitude, longitude):
        """Obtient les données météorologiques pour une localisation donnée."""
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Erreur lors de la récupération des données météorologiques : {response.status_code}")
        
        # Exemple d'utilisation de l'API météorologique
api_key = "votre_clé_api"  # Remplacez par votre clé API OpenWeatherMap
weather_api = WeatherAPI(api_key)

# Coordonnées d'une parcelle
latitude = 45.5236
longitude = -122.6750

# Récupérer les données météorologiques
weather_data = weather_api.get_weather_data(latitude, longitude)
print("Données météorologiques :", weather_data)

from fpdf import FPDF
import matplotlib.pyplot as plt

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

        # Sauvegarder le PDF
        pdf.output(output_file)
        print(f"Rapport généré avec succès : {output_file}")

        # Nettoyer les fichiers temporaires
        if os.path.exists(plot_path):
            os.remove(plot_path)

            report_generator = AgriculturalReportGenerator(data_manager)
report_generator.generate_parcelle_report('P001')