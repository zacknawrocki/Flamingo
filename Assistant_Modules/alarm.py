import time
import math
from lights import Lights
from pathlib import Path
from playsound import playsound
from datetime import datetime
from datetime import timedelta


class Alarm:
    def __init__(self):
        # Locate mp3 file
        current_path = str(Path.cwd().parent)
        self.alarm_file = "zachary_default_alarm.m4a"
        self.alarm_sound = f"{current_path}/files/audio/alarm/{self.alarm_file}"

    def set_alarm_sound(self, alarm_sound):
        self.alarm_sound = alarm_sound
        # send_response: setting alarm to ...

    def set_alarm(self, alarm_time):
        # An alarm set for a time that already occurred today implies that it is referring to tomorrow
        current_time = datetime.now()
        hour, minute = alarm_time.split(":")
        alarm_time = datetime.now().replace(hour=int(hour), minute=int(minute), second=0)
            # Therefore, if time already occurred today, push alarm to tomorrow's date
        if (alarm_time - current_time).total_seconds() < 0:
           alarm_time = alarm_time + timedelta(days=1)

        # Loop occurs until alarm goes off (for now)
        while True:
            current_time = datetime.now()
            # Gradually increase sleep precision as you get closer to alarm
            # If not within hour of waking up
            if math.ceil((alarm_time - current_time).total_seconds() / 60) > 60:
                # Sleep for an hour
                time.sleep(3600)
            # If not within 30 minutes of waking up
            elif math.ceil((alarm_time - current_time).total_seconds() / 60) > 30:
                # Sleep for 30 minutes
                time.sleep(1800)
            # If not within 15 minutes of waking up
            elif math.ceil((alarm_time - current_time).total_seconds() / 60) > 15:
                # Sleep for 15 minutes
                time.sleep(900)
            # If not within 5 minutes of waking up
            elif math.ceil((alarm_time - current_time).total_seconds() / 60) > 5:
                # Sleep for 5 minutes
                time.sleep(300)
            # If not within 1 minute of waking up
            elif math.ceil((alarm_time - current_time).total_seconds() / 60) > 1:
                # Sleep for 1 minute
                time.sleep(60)
            # If less than 1 minute remaining
            elif math.ceil((alarm_time - current_time).total_seconds() / 60) > 0:
                # Sleep for 1 second
                time.sleep(1)
            # Time for alarm to go off
            else:
                # This alarm compliments my alarm phone app
                # I have found it looks way cooler for the phone to go off,
                # then the lights, followed by the message from Flamingo
                time.sleep(2)
                self.activate_alert()
                break

    def activate_alert(self):
        # Turn on lights
        # Play alert
        playsound(self.alarm_sound, block=False)
        all_lights = Lights()
        all_lights.flicker_lights(16, "on")
        # Flicker lights in between alert
        # Do this as a loop until turned off


if __name__ == "__main__":
    a = Alarm()
    a.set_alarm("17:00")
