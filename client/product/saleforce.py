import requests
import datetime


class Product:
    def __init__(self, client_id, client_secret, refresh_token):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.token_url = "https://login.salesforce.com/services/oauth2/token"
        self.api_url = "https://thutechs-dev-ed.my.salesforce.com/services/apexrest/Products/{}"

    def get_token(self):
        params = {
            "grant_type": "refresh_token",  # authorization_code
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token
        }
        response = requests.post(self.token_url, params=params)
        if response.ok:
            return response.json().get("access_token", None)
        else:
            raise Exception("token not found")

    def get_products(self, date):
        try:
            access_token = self.get_token()
            headers = {
                'Content-type': 'application/json',
                'Accept-Encoding': 'gzip',
                'Authorization': 'Bearer %s' % access_token
            }
            #date = datetime.date.today().strftime("%Y-%m-%d")
            url = self.api_url.format(date)
            response = requests.get(url, headers=headers)
            print("product response: ", response)
            print("text response: ", response.text)
            if response.ok:
                return response.json()
        except Exception as e:
            raise Exception(str(e))
