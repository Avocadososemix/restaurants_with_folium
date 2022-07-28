""" flast_folium
    Required packages:
    - flask
    - folium
    - pandas
    Usage:
    Start the flask server by running:
        $ python flast_folium.py
    Visit http://127.0.0.1:5000/
    
    restaurant list with:
    curl -X GET "https://open-api.myhelsinki.fi/v2/places/?tags_search=restaurants" -H "accept: application/json"
    https://open-api.myhelsinki.fi/v2/places/?tags_search=restaurants
"""

from flask import Flask

import folium
from folium.plugins import MiniMap
from folium.plugins import MarkerCluster
import pandas as pd

app = Flask(__name__)

restaurant_list = pd.read_csv('restaurants.csv')
restaurant_list['point'] = restaurant_list[['location.lat', 'location.lon']].values.tolist()


@app.route('/')
def index():
    start_coords = (60.1699, 24.9384)
    folium_map = folium.Map(location=start_coords, tiles='Stamen Terrain', zoom_start=14)
    marker_cluster = MarkerCluster().add_to(folium_map)
    for index, row in restaurant_list.iterrows():
        popup_text = """<b>{}</b><br><a href="{}">{}</a>"""
        folium.Marker(location=row["point"], popup=popup_text.format(row["name.fi"],
                               row["info_url"], row["info_url"])).add_to(marker_cluster)
    minimap = MiniMap( position='topright')
    folium_map.add_child(minimap)
    return folium_map._repr_html_()

if __name__ == '__main__':
    app.run(debug=False)