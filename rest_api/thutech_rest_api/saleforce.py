import requests
import pprint

params = {
    "grant_type": "refresh_token", # authorization_code
    "client_id": "3MVG9G9pzCUSkzZt_wqRo655usHzMNgnb6IgOYf_s_gWd0OwGaLhKWjfZLHGACdqvq5tRif1tbgs5tZ9PHpzK", # Consumer Key
    "client_secret": "073F32B34AE9A146336BCB467097A4FCC3F384EB9748CD69E81D9F2650866D1A", # Consumer Secret
    "refresh_token": "5Aep861dlMxAL.LhVSZysdngEsNnXD79TtWycFKlwG0jKmKNywmOFrfFfk_lHvkLUec7kVQAB3kjBvSRP3vBGYC"
    #"username": "guest@thutechs.com", # The email you use to login
    #"password": "thutechs@2015sLEaKAhok5HS9GzmTQw8JL70" # Concat your password and your security token
}

try:
    r = requests.post("https://login.salesforce.com/services/oauth2/token", params=params)
    # print(r)
    print(r.json())
    access_token = r.json().get("access_token")
    instance_url = r.json().get("instance_url")
    print("Access Token:", access_token)
    # print("Instance URL", instance_url)
except Exception as e:
    print(e)

# refresh access token

headers = {
        'Content-type': 'application/json',
        'Accept-Encoding': 'gzip',
        'Authorization': 'Bearer %s' % access_token
    }

api_url = "https://thutechs-dev-ed.my.salesforce.com/services/apexrest/Products"

response = requests.get(api_url, headers=headers)
print(response)
# pprint.pprint(response.json())
products = response.json()
import unicodedata


for product in products:
    pid = product["Id"]
    # convert unicode to str
    pid_str = unicodedata.normalize('NFKD', pid).encode('ascii', 'ignore')
    print(pid_str)

