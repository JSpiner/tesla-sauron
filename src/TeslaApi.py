import json
import requests
import traceback

key_file = "./tesla_token.json"


class TeslaApi:
    def __init__(self) -> None:
        pass

    def getTokens(self):
        with open(key_file, 'r') as json_file:
            key_data = json.load(json_file)
            return key_data

    def saveTokens(self, tokens):
        with open(key_file, 'w') as json_file:
            json.dump(tokens, json_file)

    def refreshToken(self):
        tokens = self.getTokens()

        result = requests.post(
            "https://auth.tesla.com/oauth2/v3/token",
            data={
                "grant_type": "refresh_token",
                "client_id": "ownerapi",
                "refresh_token": tokens['refresh_token'],
                "scope": "openid email offline_access"
            }
        )
        print("refreshToken : " + str(result.status_code))
        print("refreshToken : " + str(result.text))

        newTokens = result.json()

        if 'refresh_token' in newTokens:
            self.saveTokens(newTokens)
        else:
            raise Exception("refresh fail")

    def apiGet(self, url, params = {}, isRetry=False):
        response = None
        try:
            response = requests.get(
                url,
                params=params,
                headers={"Authorization": "Bearer " + self.getTokens()['access_token']}
            )
            print(response.status_code)
            print(response.text)

            if response.status_code == 401:
                raise Exception("invalidate auth")
        except Exception as e:
            print("error occurs : " + str(e))
            traceback.print_exc()

            if isRetry:
                print("error, retry failed")
                raise e
            else:
                print("error, will retry")
                self.refreshToken()
                return self.apiGet(url, params, True)
        return response

    def apiPost(self, url, params = {}, data = {}, isRetry=False):
        response = None
        try:
            response = requests.post(
                url,
                params=params,
                json=data,
                headers={"Authorization": "Bearer " + self.getTokens()['access_token']}
            )
            print(response.status_code)
            print(response.text)

            if response.status_code == 401:
                raise Exception("invalidate auth")
        except Exception as e:
            print("error occurs : " + str(e))
            traceback.print_exc()

            if isRetry:
                print("error, retry failed")
                raise e
            else:
                print("error, will retry")
                self.refreshToken()
                return self.apiGet(url, params, True)
        return response
