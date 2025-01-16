import folium
from folium.plugins import MarkerCluster
from data_manager import AgriculturalDataManager

class AgriculturalMap:
    def __init__(self, data_manager):
        """Initialise la carte avec le gestionnaire de données."""
        self.data_manager = data_manager
        self.map = folium.Map(location=[45.5236, -122.6750], zoom_start=13)

    def create_base_map(self):
        """Crée la carte de base avec les parcelles."""
        data = self.data_manager.prepare_features()

        # Ajouter des marqueurs pour chaque parcelle
        marker_cluster = MarkerCluster().add_to(self.map)
        for _, row in data.iterrows():
            folium.Marker(
                location=[row['latitude_x'], row['longitude_x']],
                popup=f"Parcelle {row['parcelle_id']}<br>NDVI: {row['ndvi']:.2f}<br>Rendement: {row['rendement']:.2f}",
            ).add_to(marker_cluster)

        return self.map

# Initialisation de la carte
data_manager = AgriculturalDataManager()
data_manager.load_data()
agricultural_map = AgriculturalMap(data_manager)
base_map = agricultural_map.create_base_map()

# Sauvegarder la carte dans un fichier HTML
base_map.save("carte_parcelles.html")