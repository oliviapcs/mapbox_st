import streamlit as st
import pandas as pd
import numpy as np
import pandas as pd
#import geoplot as gplt
#import geoplot.crs as gcrs
#import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox
import geojson
import pydeck as pdk
import time

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
)

st.title("Explore your world")



default = 'São José dos Campos'

address = st.text_input(label="Address", value=default, placeholder="City, street, address")

#Tags per theme
FB = {"amenity": ["bar",
                      "biergarten",
                      "cafe",
                      "fast_food",
                      "food_court",
                      "pub",
                      "ice_cream",
                      "restaurant"],
        }

education = {"amenity": ["college",
                      "kindergarten",
                      "library",
                      "research_institute",
                      "training",
                      "music_school",
                      "school",
                      "university"],
        }

healthcare = {"amenity": ["clinic",
                      "dentist",
                      "doctors",
                      "hospital",
                      "nursing_home",
                      "pharmacy",
                      "social_facility",
                      "veterinary"],
        }

civic = {"amenity": ["courthouse",
                      "fire_station",
                      "bank",
                      "police",
                      "post_office",
                      "townhall"]
        }

entertainment = {"amenity": ["arts_centre",
                      "casino",
                      "cinema",
                      "community_centre",
                      "conference_centre",
                      "events_venue",
                      "music_venue",
                      "nightclub",
                      "social_centre",
                      "theatre"]
        }

tags = entertainment
tags2 = civic
tags3 = FB
tags4 = education
tags5 = healthcare

#Tags per category
places = ox.features_from_place(address,tags)
places2 = ox.features_from_place(address,tags2)
places3 = ox.features_from_place(address,tags3)
places4 = ox.features_from_place(address,tags4)
places5 = ox.features_from_place(address,tags5)

#pls = [places, places2, places3, places4, places5]

#get x and
places['centroid'] = places.centroid
places["x"]=places['centroid'].x
places["y"]=places["centroid"].y

places2['centroid'] = places2.centroid
places2["x"]=places2['centroid'].x
places2["y"]=places2["centroid"].y

places3['centroid'] = places3.centroid
places3["x"]=places3['centroid'].x
places3["y"]=places3["centroid"].y

places4['centroid'] = places4.centroid
places4["x"]=places4['centroid'].x
places4["y"]=places4["centroid"].y

places5['centroid'] = places5.centroid
places5["x"]=places5['centroid'].x
places5["y"]=places5["centroid"].y

#Filter out centroids and key info

pls1 = places[["amenity","centroid","x","y"]]
pls1["geometry"]=pls1["centroid"]
pls1['tag'] = 'Entertainment'

pls2 = places2[["amenity","centroid","x","y"]]
pls2["geometry"]=pls2["centroid"]
pls2['tag'] = 'Civic'

pls3 = places3[["amenity","centroid","x","y"]]
pls3["geometry"]=pls3["centroid"]
pls3['tag'] = 'F&B'

pls4 = places4[["amenity","centroid","x","y"]]
pls4["geometry"]=pls4["centroid"]
pls4['tag'] = 'Education'


pls5 = places5[["amenity","centroid","x","y"]]
pls5["geometry"]=pls5["centroid"]
pls5['tag'] = 'Healthcare'


#path = 'data\sanja_centroides.geojson'
#with open(path, encoding="utf8") as f:
#    gj = geojson.load(f)

#coordinates = []

#for i in range(len(gj['features'])):
#  coordinates.append(gj['features'][i]['geometry']['coordinates'])

#sanja_centroide = pd.DataFrame(coordinates).rename(columns = {0:'x', 1: 'y'})
#sanja_centroide['tag'] = 'Centroide Sanja'

pls = pd.concat([pls1, pls2, pls3, pls4, pls5])

options_amenities = st.multiselect(
    'Amenities',
    ['Entertainment', 'Civic', 'F&B', 'Education', 'Healthcare'],
    ['F&B']
    )

#st.write('You selected:', options_amenities)

pls = pls[pls['tag'].isin(options_amenities)]
#pls = [['x', 'y']]  


#st.write(pls)


chart_data = pls[['x', 'y']]

options_layer = st.multiselect(
    'Layer',
    ['Hexagon', 'Heatmap', 'Scatter', 'GridLayer'],
    ['Hexagon']
    )


Hexagon = pdk.Layer(
     'HexagonLayer',
     data=chart_data,
     get_position='[x, y]',
     radius=200,
     elevation_scale=4,
     elevation_range=[0, 1000],
     pickable=True,
     extruded=True,
         )

GridLayer = pdk.Layer(
    "GridLayer",
    data=chart_data,
    pickable=True,
    extruded=True,
    cell_size=200,
    elevation_scale=4,
    get_position='[x, y]',
)

Heatmap = pdk.Layer(
    "HeatmapLayer",
    data=chart_data,
    opacity=0.25,
    get_position='[x, y]',
    aggregation=pdk.types.String('MEAN'),
)
Scatter =  pdk.Layer(
             'ScatterplotLayer',
             data=chart_data,
             get_position='[x, y]',
             get_color='[200, 30, 0, 160]',
             get_radius=200,
         ),

options_layer_dict = {
   'Hexagon': Hexagon,
   'Heatmap': Heatmap,
   'Scatter': Scatter,
   'GridLayer':GridLayer
   }

layers = [options_layer_dict.get(key) for key in list(options_layer)]

print(pls['x'].mean().round(2),)

progress_text = "Operation in progress. Please wait."
my_bar = st.progress(0, text=progress_text)

for percent_complete in range(100):
    time.sleep(0.01)
    my_bar.progress(percent_complete + 1, text=progress_text)
time.sleep(1)
my_bar.empty()


st.pydeck_chart(pdk.Deck(
    map_style=None,
    tooltip={
        'html': '<b>Elevation Value:</b> {elevationValue}',
        'style': {
            'color': 'white'
        }},
    initial_view_state=pdk.ViewState(
        latitude=pls['y'].mean().round(2),
        longitude=pls['x'].mean().round(2),
        zoom=11,
        pitch=50,
    ),
    layers=
       layers                   
    
))


#Usar esse exemplo de organização para selecionar a visualização
#Criar botões laterais para selecionar a visualização