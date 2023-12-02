import requests
import requests_cache
import json



requests_cache.install_cache('image_cache', backend='sqlite')

def get_image_url(search):
    url = "https://google-search72.p.rapidapi.com/search"

    querystring = {"q": search,"gl":"us","lr":"lang_en","num":"10","start":"0"}

    headers = {
	    "X-RapidAPI-Key": "abee8f758fmshe6e4f66562e5b3ep13fbeajsnc583a9839270",
	    "X-RapidAPI-Host": "google-search72.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()

    img_url = ""

    if item in data.keys():
        img_url = data[item][0]['originalImageUrl']

    return img_url

