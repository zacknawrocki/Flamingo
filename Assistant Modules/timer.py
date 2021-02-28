import time

class Timer:
    def __init__(self, minutes, seconds):
        self.minutes = minutes
        self.seconds = seconds
        self.begin_timer()

    def begin_timer(self):
        seconds = self.minutes * 60 + self.seconds

        # Countdown
        while seconds > 0:
            time.sleep(1)
            seconds -= 1
            # Notify how many minutes left
            if seconds % 60 == 0 and seconds > 0:
                if seconds == 60:
                    self.notify_user("One minute left.")
                else:
                    self.notify_user(f"{int(seconds / 60)} minutes left.")

        self.notify_user("Timer complete.")

    @staticmethod
    def notify_user(message):
        # For now, just print the response. Eventually, this will be sent to pi for TTS response
        print(message)

t = Timer(2, 30)
