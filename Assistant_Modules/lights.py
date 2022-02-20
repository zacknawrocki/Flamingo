import kasa
import asyncio
import time


class Lights:
    def __init__(self):
        # search for ips of kasa smart plugs
        self.normal_ips = list(asyncio.run(kasa.Discover.discover()).keys())

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

    def lights_on(self):
        asyncio.run(self.all_lights_on())

    def lights_off(self):
        asyncio.run(self.all_lights_off())


if __name__ == "__main__":
    lights = Lights()
    lights.flicker_lights(16, "on")
    lights.lights_off()
    lights.lights_on()
