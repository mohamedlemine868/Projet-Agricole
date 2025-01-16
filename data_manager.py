import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

class AgriculturalDataManager:
    def __init__(self):
        """Initialise le gestionnaire de données."""
        self.monitoring_data = None  # Données de suivi des cultures
        self.weather_data = None     # Données météorologiques
        self.soil_data = None        # Données des sols
        self.yield_history = None    # Historique des rendements
        self.scaler = StandardScaler()  # Pour normaliser les données

    def load_data(self):
        """Charge les données depuis les fichiers CSV."""
        try:
            # Chargement des données de suivi des cultures
            self.monitoring_data = pd.read_csv('data/monitoring_cultures.csv', parse_dates=['date'])
            print("Données de monitoring chargées avec succès.")

            # Chargement des données météorologiques
            self.weather_data = pd.read_csv('data/meteo_detaillee.csv', parse_dates=['date'])
            print("Données météorologiques chargées avec succès.")

            # Chargement des données des sols
            self.soil_data = pd.read_csv('data/sols.csv')
            print("Données des sols chargées avec succès.")

            # Chargement de l'historique des rendements
            self.yield_history = pd.read_csv('data/historique_rendements.csv', parse_dates=['date'])
            print("Historique des rendements chargé avec succès.")

            # Générer une colonne 'rendement' fictive si elle n'existe pas
            if 'rendement' not in self.monitoring_data.columns:
                self.monitoring_data['rendement'] = np.random.uniform(10, 20, size=len(self.monitoring_data))
                print("Colonne 'rendement' fictive générée avec succès.")

        except Exception as e:
            print(f"Erreur lors du chargement des données : {e}")

    def prepare_features(self):
        """Prépare les caractéristiques pour l'analyse en fusionnant les données."""
        if self.monitoring_data is None or self.weather_data is None or self.soil_data is None:
            raise ValueError("Les données n'ont pas été chargées. Utilisez load_data() d'abord.")

        # Fusion des données de monitoring et météo
        merged_data = pd.merge_asof(
            self.monitoring_data.sort_values('date'),
            self.weather_data.sort_values('date'),
            on='date'
        )

        # Fusion avec les données du sol
        merged_data = pd.merge(merged_data, self.soil_data, on='parcelle_id')

        # Normalisation des données
        numeric_cols = merged_data.select_dtypes(include=[np.number]).columns
        merged_data[numeric_cols] = self.scaler.fit_transform(merged_data[numeric_cols])

        return merged_data