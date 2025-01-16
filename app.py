import streamlit as st
from data_manager import AgriculturalDataManager
from dashboard import AgriculturalDashboard
from map_visualization import AgriculturalMap

# Titre de l'application
st.title("Tableau de Bord Agricole Interactif")

# Chargement des données
data_manager = AgriculturalDataManager()
data_manager.load_data()
prepared_data = data_manager.prepare_features()

# Initialisation du tableau de bord
dashboard = AgriculturalDashboard(data_manager)

# Afficher les visualisations Bokeh
st.write("### Historique des Rendements")
yield_plot = dashboard.create_yield_history_plot()
st.bokeh_chart(yield_plot)

st.write("### Évolution du NDVI")
ndvi_plot = dashboard.create_ndvi_temporal_plot()
st.bokeh_chart(ndvi_plot)

# Afficher la carte Folium
st.write("### Carte des Parcelles")
agricultural_map = AgriculturalMap(data_manager)
base_map = agricultural_map.create_base_map()
st.folium_static(base_map)