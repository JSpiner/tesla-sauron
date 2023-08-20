from datetime import datetime
import time
import traceback
from TeslaApi import TeslaApi


class Cron:

    def __init__(self) -> None:
        self.vehicleId = None
        self.teslaApi = TeslaApi()

    def run(self):
        print("on cron : " + str(datetime.now()))

        for i in range(0, 30):
            try:
                result = self.teslaApi.apiPost(
                    "https://owner-api.teslamotors.com/api/1/vehicles/" + str(self.__getVehicleId()) + "/wake_up",
                ).json()
                print("try : " + str(i))
                print(result)

                if result['response']['state'] == "online":
                    print("car online")
                    return
                time.sleep(1)
            except:
                traceback.print_exc()

        print("wake up failed")

    def __getVehicleId(self):
        if self.vehicleId is None:
            response = self.teslaApi.apiGet(
                "https://owner-api.teslamotors.com/api/1/vehicles/"
            ).json()
            self.vehicleId = response['response'][0]['id']

        return self.vehicleId
