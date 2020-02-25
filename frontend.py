from flask import Flask, render_template, request
import twitter
import folium
from geopy.geocoders import Nominatim

keys = {
    "consumer_key" : "sphwjr534OVIynyBnaT6PsKdi",
    "consumer_secret" : "Yw6T6JNySGpfXfIiMikoxXqg8Ahjas7IOWcQR2og4QNr2gG7w8",
    "access_token" : "2924865400-gx2ARK9JpJN0vjYerDyqVApJpLB8l7jJjuYMdkV",
    "access_token_secret" : "JUvuRGfLvwNlnkdn1v0ywyziMnKiWGRwiw2ONSS3LimW7"}


locator = Nominatim(user_agent="Markers")


def get_location_name(name, keys):
    """
    Returns a list of following users and their locations
    of a given user
    :param name:str
    :param keys:dict
    :return:list
    """
    api = twitter.Api(consumer_key=keys["consumer_key"],
                      consumer_secret=keys["consumer_secret"],
                      access_token_key=keys["access_token"],
                      access_token_secret=keys["access_token_secret"])
    user_list = api.GetFriends(screen_name=name)
    return [(user.location, user.screen_name) for user in user_list
             if len(user.location)>=1]


def make_map(users):
    """
    Makes an map with users from users and saves it
    :param users: list
    :return: None
    """
    m = folium.Map(location=[49.8326046, 23.8721529], zoom_start=3)
    markers = folium.FeatureGroup(name="Locations")
    dct_locations = {}
    for user in users:
        try:
            location = locator.geocode(user[0])
            lat, lon = (location.latitude, location.longitude)
            dct_locations[(lat, lon)] = dct_locations.get((lat, lon), []) + [user[1]]
        except:
            continue
    for location in dct_locations:
        markers.add_child(folium.Marker(location=[location[0], location[1]],
                                        popup=", ".join(dct_locations[location]),
                                        icon=folium.Icon(icon='cloud',
                                                         icon_color='red')))
    m.add_child(markers)
    m.save("map.html")
    lines = []
    with open("map.html") as f:
        for line in f:
            lines.append(line)
    with open("templates/map.html", 'w') as f:
        for i in lines:
            f.write(i)


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        username = request.form['username']
        users = get_location_name(username, keys)
        make_map(users)
    return render_template("map.html")


app.run(debug=True)