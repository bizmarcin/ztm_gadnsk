import folium
from folium.plugins import MarkerCluster
import requests
import json

ztm_map = folium.Map(location=[54.34632, 18.649246])
ztm_cluster = MarkerCluster()

r = requests.get('http://ckan2.multimediagdansk.pl/gpsPositions')
ztm_rider = r.json()

def get_icon_color(delay):
    if delay is None:
        return 'gray'

    if delay < 60:
        return 'green'

    if delay < 120:
        return 'orange'

    return 'red'

for ztm_row in ztm_rider['Vehicles']:
    latitude = float(ztm_row['Lat'])
    longitude = float(ztm_row['Lon'])
    coordinates = [latitude, longitude]

    bus_info = f"Line: {ztm_row['Line']},<br> VehicleId: {ztm_row['VehicleId']},<br> Speed: {ztm_row['Speed']},<br> Delay: {ztm_row['Delay']} sec,<br> Lat: {ztm_row['Lat']},<br> Lon: {ztm_row['Lon']},<br> GPSQuality: {ztm_row['GPSQuality']}"
    bus_icon = folium.Icon(icon='bus', prefix='fa', color=get_icon_color(ztm_row['Delay']))

    ztm_marker = folium.Marker(location=coordinates, popup=bus_info, icon=bus_icon)
    ztm_cluster.add_child(ztm_marker)

ztm_map.add_child(ztm_cluster)
ztm_map.save('ztm_map.html')