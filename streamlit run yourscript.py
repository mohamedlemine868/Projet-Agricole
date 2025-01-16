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