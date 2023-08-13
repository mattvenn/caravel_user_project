from cocotb.queue import Queue
import cocotb
import logging
from tabulate import tabulate
from models.gpio_model.gpio_monitor import GPIOs_Monitor
from models.gpio_model.gpio_coverage import GPIOs_Coverage


class GPIOs_Model():
    def __init__(self, caravelEnv) -> None:
        self.caravelEnv = caravelEnv
        config_queue = Queue()
        io_queue = Queue()
        GPIOs_Monitor(self.caravelEnv, config_queue, io_queue)
        gpios_cov = GPIOs_Coverage()
        ConfigModel(config_queue, gpios_cov)
        IO_Model(io_queue, gpios_cov)

class AbstractModelGPIO():
    def __init__(self, queue) -> None:
        self._thread = cocotb.scheduler.add(self._model(queue))

    async def _model(self, queue):
        pass

    async def _get_transactions(self, queue):
        transaction = await queue.get()
        cocotb.log.debug(f"[{__class__.__name__}][_get_transactions] getting transaction {transaction} from monitor")
        return transaction

    def configure_logger(self, logger_name="logger", logger_file="log.txt"):
        self.spi_logger = logging.getLogger(logger_name)

        # Configure the logger
        self.spi_logger.setLevel(logging.INFO)

        # Create a FileHandler to log to a file
        file_handler = logging.FileHandler(logger_file)
        file_handler.setLevel(logging.INFO)

        # # Create a StreamHandler to log to the console (optional)
        # console_handler = logging.StreamHandler()
        # console_handler.setLevel(logging.DEBUG)

        # Add the handlers to the logger
        self.spi_logger.addHandler(file_handler)
        # Create a NullHandler for the console to suppress output

        # self.spi_logger.addHandler(console_handler)  # Optional: Log to console
        # Remove the console handler to avoid logging to console

        # log the header
        self.log_operation(None, header_logged=True)

    def log_operation(self, transaction, header_logged):
        pass


class ConfigModel(AbstractModelGPIO):
    def __init__(self, queue, gpios_cov) -> None:
        self.configure_logger(logger_name="GPIO_config_LOG", logger_file="gpio_config.log")
        self.gpios_cov = gpios_cov
        super().__init__(queue)

    async def _model(self, queue):
        while True:
            transaction = await self._get_transactions(queue)
            cocotb.log.debug(f"[{__class__.__name__}][_model] {transaction}")
            self.log_operation(transaction)
            self.gpios_cov.gpio_cov(transaction)

    def log_operation(self, transaction, header_logged=False):
        if header_logged:
            # Log the header
            header = tabulate([], headers=["Time", "GPIO","config Type", "controlled by", "in/out", "dm"], tablefmt="grid")
            self.spi_logger.info(header)
            # Mark that the header has been logged
        else:
            table_data = [(
                f"{cocotb.utils.get_sim_time(units='ns')} ns",
                f"GPIO{transaction.gpio_number}",
                transaction.config_type,
                "Managment" if transaction.mgmt_en == 1 else "User",
                "bi-directional" if transaction.inenb == 0 and transaction.outenb == 0 else "output" if transaction.outenb == 0 else "input" if transaction.inenb == 0 else "unknown",
                "no_pull" if transaction.dm == 0x1 else "pull up" if transaction.dm == 0x2 else "pull down" if transaction.dm == 0x3 else "float" if transaction.dm == 0x6 else "analog" if transaction.dm == 0x0 else transaction.dm
            )]
            table = tabulate(table_data, tablefmt="grid")
            self.spi_logger.info(table)


class IO_Model(AbstractModelGPIO):
    def __init__(self, queue, gpios_cov) -> None:
        self.gpios_cov = gpios_cov
        super().__init__(queue)

    async def _model(self, queue):
        while True:
            transaction = await self._get_transactions(queue)
            cocotb.log.debug(f"[{__class__.__name__}][_model] {transaction}")
            self.gpios_cov.io_cov(transaction)
