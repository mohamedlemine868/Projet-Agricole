from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool

class AgriculturalDashboard:
    def __init__(self, data_manager):
        """Initialise le tableau de bord avec le gestionnaire de données."""
        self.data_manager = data_manager
        self.source = ColumnDataSource(data=dict())
        self.hist_source = ColumnDataSource(data=dict())
        self.selected_parcelle = None
        self.create_data_sources()

    def create_data_sources(self):
        """Prépare les sources de données pour Bokeh."""
        data = self.data_manager.prepare_features()
        self.source.data = data.to_dict(orient='list')

        # Exemple : Historique des rendements pour une parcelle
        parcelle_id = 'P001'  # Parcelle par défaut
        parcelle_data = data[data['parcelle_id'] == parcelle_id]
        self.hist_source.data = parcelle_data.to_dict(orient='list')

    def create_yield_history_plot(self):
        """Crée un graphique montrant l'historique des rendements."""
        p = figure(title="Historique des Rendements", x_axis_type='datetime', height=400)
        p.line('date', 'rendement', source=self.hist_source, line_width=2, legend_label="Rendement")
        p.xaxis.axis_label = "Date"
        p.yaxis.axis_label = "Rendement (tonnes/ha)"
        p.add_tools(HoverTool(tooltips=[("Date", "@date{%F}"), ("Rendement", "@rendement{0.2f}")],
                              formatters={'@date': 'datetime'}))
        return p

    def create_ndvi_temporal_plot(self):
        """Crée un graphique montrant l'évolution du NDVI."""
        p = figure(title="Évolution du NDVI", x_axis_type='datetime', height=400)
        p.line('date', 'ndvi', source=self.hist_source, line_width=2, color="green", legend_label="NDVI")
        p.xaxis.axis_label = "Date"
        p.yaxis.axis_label = "NDVI"
        p.add_tools(HoverTool(tooltips=[("Date", "@date{%F}"), ("NDVI", "@ndvi{0.2f}")],
                              formatters={'@date': 'datetime'}))
        return p