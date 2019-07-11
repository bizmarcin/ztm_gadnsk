import folium
from folium.plugins import MarkerCluster
import requests
import json
from datetime import datetime

def map():
    start_time = datetime.now()
    ztm_map = folium.Map(location=[54.34632, 18.649246])
    ztm_cluster = MarkerCluster()

    def get_line_number(bus_id, data):
        for row in data['Vehicles']:
            if row['VehicleId']==bus_id:
                return row['Line']
        return None

    def get_json_data_from_web(url):
        r = requests.get(url)
        data = r.json()
        r.close()
        return data

    def get_icon_color(delay):
        if delay is None:
            return 'gray'

        if delay < 60:
            return 'green'

        if delay < 120:
            return 'orange'

        return 'red'

    def get_delay_time(delay_in_sec):
        delay = ""
        min_delay = delay_in_sec // 60
        if min_delay > 0:
            delay += f"{min_delay}min"

        sec_delay = delay_in_sec % 60
        if sec_delay >= 0:
            if delay.__len__() > 1:
                delay += f" {sec_delay}sec"
            else:
                delay += f"{sec_delay}sec"
        return delay

    def get_delays(stop_id, data):
        delays_list = []
        message = None
        for stop_delay in data[str(stop_id)]['delay']:
            try:
                message = f"delay: {get_delay_time(stop_delay['delayInSeconds'])}, estimatedTime: {stop_delay['estimatedTime']}, headsign: {stop_delay['headsign']}, vehicleId: {stop_delay['vehicleId']}, line: {get_line_number(stop_delay['vehicleId'],ztm_rider)}"
            except:
                pass
            delays_list.append(message)
        return delays_list

    # Data source: https://ckan.multimediagdansk.pl/dataset/tristar
    ztm_rider = get_json_data_from_web('http://ckan2.multimediagdansk.pl/gpsPositions')
    stops_reader = get_json_data_from_web('https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/4c4025f0-01bf-41f7-a39f-d156d201b82b/download/stops.json')
    delays_rider = get_json_data_from_web('http://ckan2.multimediagdansk.pl/delays')

    max_bus_delay = 0
    max_bus_speed = 0

    for ztm_row in ztm_rider['Vehicles']:
        latitude = float(ztm_row['Lat'])
        longitude = float(ztm_row['Lon'])
        coordinates = [latitude, longitude]
        if get_delay_time(ztm_row['Delay'])=="0sec":
            bus_info = f"""Line: {ztm_row['Line']},<br> VehicleId: {ztm_row['VehicleId']},<br> Speed: {ztm_row[
                'Speed']}"""
        else:
            bus_info = f"""Line: {ztm_row['Line']},<br> VehicleId: {ztm_row['VehicleId']},<br> Speed: {ztm_row['Speed']},
                <br> Delay: {get_delay_time(ztm_row['Delay'])}"""

        if abs(int(ztm_row['Delay'])) > max_bus_delay:
            max_bus_delay = abs(int(ztm_row['Delay']))

        if abs(int(ztm_row['Speed'])) > max_bus_speed:
            max_bus_speed = abs(int(ztm_row['Speed']))

        bus_popup = folium.Popup(bus_info, max_width=300)
        bus_icon = folium.Icon(icon='bus', prefix='fa', color=get_icon_color(ztm_row['Delay']))

        ztm_marker = folium.Marker(location=coordinates, popup=bus_popup, icon=bus_icon)

        ztm_cluster.add_child(ztm_marker)

    today = f'{datetime.now().year}-'
    if datetime.now().month < 10:
        today = today + f'0{datetime.now().month}-'
    else:
        today = today + str(datetime.now().month) + '-'

    if datetime.now().day < 10:
        today = today + f'0{datetime.now().day}'
    else:
        today = today + str(datetime.now().day)

    for stops_row in stops_reader[today]['stops']:
        latitude = float(stops_row['stopLat'])
        longitude = float(stops_row['stopLon'])
        coordinates = [latitude, longitude]


        stops_info = f"""stopId: {stops_row['stopId']} <br>
                        stopName: {stops_row['stopName']} <br>
                        stopDesc: {stops_row['stopDesc']} <br>"""

        try:
            delays_on_stop = get_delays(stops_row['stopId'],delays_rider)
            for delay in delays_on_stop:
                stops_info = stops_info + delay + "<br>"
        except:
            pass

        stops_popup = folium.Popup(stops_info, max_width=500)
        stops_icon = folium.Icon(color='blue')

        ztm_marker = folium.Marker(location=coordinates, popup=stops_popup, icon=stops_icon)
        ztm_cluster.add_child(ztm_marker)

    print(f"Max delay: {get_delay_time(max_bus_delay)}")
    print(f"Max speed: {max_bus_speed}")

    ztm_map.add_child(ztm_cluster)
    ztm_map.save('templates\ztm_map.html')
    stop_time = datetime.now()

    print(f"Start time: {start_time}")
    print(f"Stop time: {stop_time}")

    return ztm_map

map()