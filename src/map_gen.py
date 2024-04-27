import folium
from folium.plugins import AntPath
import pandas as pd

import geopandas as gpd
import folium.features

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
                                                 t_mag=df.loc[i, 'mag']),script = True, width='80%', height='80%')
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

def tornado_choropleth_map(geojson_path: str, geo_df: gpd.GeoDataFrame, year: int):
    map = folium.Map(
        location=[39.8283, -98.5795],
        tiles="cartodbpositronnolabels",
        zoom_start=5,
        max_bounds=True)
    custom_scale = (geo_df['count'].quantile((0,0.2,0.4,0.6,0.8,1))).tolist()
    folium.Choropleth(
                geo_data=geojson_path,
                data=geo_df,
                columns=['id', 'count'],
                key_on='feature.id',
                threshold_scale=custom_scale,
                fill_color='YlOrRd',
                nan_fill_color="White",
                fill_opacity=0.7,
                line_opacity=0.2,
                legend_name=f'Tornados in {year}',
                highlight=True,
                line_color='black').add_to(map) 

    # Add Customized Tooltips to the map
    folium.features.GeoJson(
                        data=geo_df,
                        name=f'Tornados in {year}',
                        smooth_factor=2,
                        style_function=lambda x: {'color':'black','fillColor':'transparent','weight':0.5},
                        tooltip=folium.features.GeoJsonTooltip(
                            fields=['name',
                                    'count',
                                ],
                            aliases=["State",
                                    'Tornado Count',
                                    ], 
                            localize=True,
                            sticky=False,
                            labels=True,
                            style="""
                                background-color: #F0EFEF;
                                border: 2px solid black;
                                border-radius: 3px;
                                box-shadow: 3px;
                            """,
                            max_width=800,),
                                highlight_function=lambda x: {'weight':3,'fillColor':'grey'},
                            ).add_to(map)   
    return map