import kasa
import asyncio
import time

class Lights:
    def __init__(self, normal_light_ips=None):
        self.normal_ips = normal_light_ips

    async def all_lights_on(self):
        for ip in self.normal_ips:
            plug = kasa.SmartPlug(ip)
            await plug.update()
            print(plug.alias)
            await plug.turn_on()

    async def all_lights_off(self):
        for ip in self.normal_ips:
            plug = kasa.SmartPlug(ip)
            await plug.update()
            print(plug.alias)
            await plug.turn_off()

    def flicker_lights(self, flashes, end):
        for flash in range(flashes):
            asyncio.run(self.all_lights_on())
            time.sleep(0.5)
            asyncio.run(self.all_lights_off())
            time.sleep(0.5)
        if end == "on":
            asyncio.run(self.all_lights_on())






if __name__ == "__main__":
    l = Lights(["192.168.1.22", "192.168.1.23"])
    l.flicker_lights(16, "on")
