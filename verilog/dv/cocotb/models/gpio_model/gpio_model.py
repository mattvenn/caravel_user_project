from cocotb.queue import Queue
import cocotb
import logging
from tabulate import tabulate
from models.gpio_model.gpio_monitor import GPIOs_Monitor


class GPIOs_Model():
    def __init__(self, caravelEnv) -> None:
        self.caravelEnv = caravelEnv
        config_queue = Queue()
        GPIOs_Monitor(self.caravelEnv, config_queue)
