import folium
from folium.plugins import AntPath
import pandas as pd

def state_tornado_path_map(state: str, year: int, data: pd.DataFrame, geojson_path: str, capital_locations: dict):

    map = folium.Map(location=capital_locations[state], tiles="cartodbpositronnolabels", zoom_start=5, max_bounds=True)

    df = data[(data["yr"]==year) & (data['st'] == state)]

    fg = folium.FeatureGroup(name="Tornados", show=True).add_to(map)

    for i in df.index: # loop through the plots
        html = \
        """
        <h3>
            Date: {date} Start: {t_start} End: {t_end} Mag: {t_mag}
        </h3>
        <br>
        """
        start = df.loc[i, 'sgeo']
        end = df.loc[i, 'egeo']

        popup_contents = folium.Html(html.format(date=df.loc[i, 'date'],
                                                 t_start=start, 
                                                 t_end=end, 
                                                 t_mag=df.loc[i, 'mag']),script = True)
        popup = folium.Popup(popup_contents, max_width=1500)
        if ((end != [0.0,0.0]) & (end != start)):
            folium.Marker(location=start,
                          popup=popup,
                          icon=folium.Icon(icon='tornado', prefix='fa')).add_to(fg)
            
            AntPath(locations=[start, end],
                    delay=400, 
                    weight=3, 
                    color='red', 
                    dash_array=[30,15]).add_to(fg)

    borderStyle = {
        'color' : 'blue',
        'weight': 1,
        'fillColor': 'blue',
        'fillOpacity': 0.1
    }

    folium.GeoJson(data=geojson_path, style_function=lambda x: borderStyle, control=False).add_to(map)
    folium.map.CustomPane("labels").add_to(map)
    folium.TileLayer("cartodbpositrononlylabels", pane="labels").add_to(map)
    folium.LayerControl().add_to(map)

    return map