import threading
import time
import math
from typing import Optional

from sense_hat import SenseHat
sense = SenseHat()

SAMPLE_PERIOD_SEC = 1

class Sampler:
    def __init__(self, period: int = SAMPLE_PERIOD_SEC):
        self.period = max(1, int(period))
        self._t: Optional[threading.Thread] = None
        self._stop = threading.Event()

    def start(self):
        if self._t and self._t.is_alive():
            return self

        self._stop.clear()
        self._t = threading.Thread(target=self._run, name="Sampler", daemon=True)
        self._t.start()
        return self

    def stop(self):
        self._stop.set()
        if self._t:
            self._t.join()
        return self

    def _run(self):
        while not self._stop.is_set():
            try:
                temp = sense.get_temperature()
                humidity = sense.get_humidity()
                pressure = sense.get_pressure()
                print(f"temp={temp:.2f}C humidity={humidity:.2f}% pressure={pressure:.2f}hPa")
            except Exception:
                print("sensor read error")
            slept = 0.0
            interval = 0.1
            while slept < self.period and not self._stop.is_set():
                time.sleep(interval)
                slept += interval