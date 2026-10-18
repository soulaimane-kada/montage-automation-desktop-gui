import requests, json


# READ CONFIGS
with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)


# Genius
CLIENT_ID = config["CLIENT_ID"]
CLIENT_SECRET = config["CLIENT_SECRET"]
CLIENT_ACCESS_TOKEN = config["CLIENT_ACCESS_TOKEN"]


def search(search_term):
    genius_search_url = f"http://api.genius.com/search?q={search_term}&access_token={CLIENT_ACCESS_TOKEN}"
    response = requests.get(genius_search_url)
    json_data = response.json()
    return json_data

def get_artist_info_by_id(artist_id):
    url = f"http://api.genius.com/artists/{artist_id}?access_token={CLIENT_ACCESS_TOKEN}"
    response = requests.get(url)
    print (response)
    artist_info = response.json()['response']['artist']
    return artist_info



json_data = get_artist_info_by_id(1177)
with open("results.json", "w") as json_file:
    json.dump(json_data, json_file)
print ("DONE")