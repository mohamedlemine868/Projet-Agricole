import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from scipy import stats
from statsmodels.tsa.seasonal import seasonal_decompose
from data_manager import AgriculturalDataManager

class AgriculturalAnalyzer:
    def __init__(self, data_manager):
        """Initialise l'analyseur avec le gestionnaire de données."""
        self.data_manager = data_manager
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)

    def analyze_yield_factors(self, parcelle_id):
        """Analyse les facteurs influençant les rendements pour une parcelle donnée."""
        data = self.data_manager.prepare_features()
        parcelle_data = data[data['parcelle_id'] == parcelle_id]

        # Sélectionnez uniquement les colonnes numériques
        numeric_data = parcelle_data.select_dtypes(include=[np.number])

        # Vérifiez que la colonne 'rendement' existe
        if 'rendement' not in numeric_data.columns:
            raise KeyError("La colonne 'rendement' est manquante dans les données.")

        # Calcul des corrélations entre les rendements et les autres variables
        correlations = numeric_data.corr()['rendement'].drop('rendement')
        return correlations

    def analyze_yield_trends(self, parcelle_id):
        """Analyse les tendances des rendements pour une parcelle donnée."""
        parcelle_data = self.data_manager.yield_history[self.data_manager.yield_history['parcelle_id'] == parcelle_id]

        # Vérifiez que la colonne 'rendement' existe
        if 'rendement' not in parcelle_data.columns:
            raise KeyError("La colonne 'rendement' est manquante dans les données.")

        # Décomposition des séries temporelles
        decomposition = seasonal_decompose(parcelle_data['rendement'], model='additive', period=12)
        trend = decomposition.trend
        seasonal = decomposition.seasonal
        residual = decomposition.resid

        return trend, seasonal, residual

    def calculate_risk_metrics(self, parcelle_id):
        """Calcule les métriques de risque pour une parcelle donnée."""
        data = self.data_manager.prepare_features()
        parcelle_data = data[data['parcelle_id'] == parcelle_id]

        # Exemple de métrique de risque : probabilité de stress hydrique élevé
        risk_metric = np.mean(parcelle_data['stress_hydrique'] > 0.15)  # Seuil arbitraire
        return risk_metric

    def predict_yield(self, parcelle_id):
        """Prédit les rendements futurs pour une parcelle donnée."""
        data = self.data_manager.prepare_features()
        parcelle_data = data[data['parcelle_id'] == parcelle_id]

        # Vérifiez que la colonne 'rendement' existe
        if 'rendement' not in parcelle_data.columns:
            raise KeyError("La colonne 'rendement' est manquante dans les données.")

        # Séparation des caractéristiques et de la cible
        X = parcelle_data.select_dtypes(include=[np.number]).drop(columns=['rendement'])
        y = parcelle_data['rendement']

        # Entraînement du modèle
        self.model.fit(X, y)

        # Prédiction
        predictions = self.model.predict(X)
        return predictions

# Test de la classe AgriculturalAnalyzer
if __name__ == "__main__":
    # Initialisation du gestionnaire de données
    data_manager = AgriculturalDataManager()
    data_manager.load_data()

    # Initialisation de l'analyseur
    analyzer = AgriculturalAnalyzer(data_manager)

    # Analyse des facteurs influençant les rendements pour une parcelle
    parcelle_id = 'P001'  # Remplacez par l'ID d'une parcelle existante dans vos données
    try:
        correlations = analyzer.analyze_yield_factors(parcelle_id)
        print(f"Corrélations pour la parcelle {parcelle_id} :")
        print(correlations)
    except KeyError as e:
        print(f"Erreur : {e}")

    # Analyse des tendances des rendements
    try:
        trend, seasonal, residual = analyzer.analyze_yield_trends(parcelle_id)
        print(f"Tendance des rendements pour la parcelle {parcelle_id} :")
        print(trend.head())
    except KeyError as e:
        print(f"Erreur : {e}")

    # Calcul des métriques de risque
    risk_metric = analyzer.calculate_risk_metrics(parcelle_id)
    print(f"Métrique de risque pour la parcelle {parcelle_id} : {risk_metric:.2f}")

    # Prédiction des rendements
    try:
        predictions = analyzer.predict_yield(parcelle_id)
        print(f"Prédictions des rendements pour la parcelle {parcelle_id} :")
        print(predictions[:5])  # Affiche les 5 premières prédictions
    except KeyError as e:
        print(f"Erreur : {e}")