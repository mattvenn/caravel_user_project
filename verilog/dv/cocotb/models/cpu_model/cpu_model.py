import cocotb
from models.cpu_model.cpu_monitor import CPU_Monitor
from cocotb.queue import Queue
from collections import namedtuple
import logging
from tabulate import tabulate


SPI_Operation = namedtuple("SPI_Operation", ["command", "address", "data_in", "data_out"])


class CPU_Model():
    def __init__(self, caravelEnv) -> None:
        self.caravelEnv = caravelEnv
        dbus_queue = Queue()
        ibus_queue = Queue()
        CPU_Monitor(self.caravelEnv, dbus_queue, ibus_queue)
        Dbus_Model(dbus_queue)
        Ibus_Model(ibus_queue)


class AbstractModelCPU():
    def __init__(self, queue) -> None:
        self._thread = cocotb.scheduler.add(self._model(queue))

    async def _model(self, queue):
        pass

    async def _get_transactions(self, queue):
        transaction = await queue.get()
        cocotb.log.debug(f"[{__class__.__name__}][_get_transactions] getting transaction {transaction} from monitor")
        return transaction

    def configure_logger(self, logger_name="logger", logger_file="log.txt"):
        self.model_logger = logging.getLogger(logger_name)

        # Configure the logger
        self.model_logger.setLevel(logging.INFO)

        # Create a FileHandler to log to a file
        file_handler = logging.FileHandler(logger_file)
        file_handler.setLevel(logging.INFO)

        # # Create a StreamHandler to log to the console (optional)
        # console_handler = logging.StreamHandler()
        # console_handler.setLevel(logging.DEBUG)

        # Add the handlers to the logger
        self.model_logger.addHandler(file_handler)
        # Create a NullHandler for the console to suppress output

        # self.model_logger.addHandler(console_handler)  # Optional: Log to console
        # Remove the console handler to avoid logging to console

        # log the header
        self.log_operation(None, header_logged=True)

    def log_operation(self, transaction, header_logged):
        pass


class Dbus_Model(AbstractModelCPU):
    def __init__(self, queue) -> None:
        self.configure_logger(logger_name="CPU_DBUS_LOG", logger_file="cpu_dbus.log")
        super().__init__(queue)

    async def _model(self, queue):
        while True:
            transaction = await self._get_transactions(queue)
            cocotb.log.debug(f"[{__class__.__name__}][_model] {transaction}")
            self.log_operation(transaction)

    def log_operation(self, transaction, header_logged=False):
        if header_logged:
            # Log the header
            header = tabulate([], headers=["Time", "Type", "Address", "Select", "Data"], tablefmt="grid")
            self.model_logger.info(header)
            # Mark that the header has been logged
        else:
            table_data = [(
                f"{cocotb.utils.get_sim_time(units='ns')} ns",
                "read" if transaction.write == 0 else "wrote",
                hex(transaction.address<<2),
                hex(transaction.select),
                transaction.data if "x" in transaction.data.binstr else hex(transaction.data.integer)
            )]
            table = tabulate(table_data, tablefmt="grid")
            self.model_logger.info(table)


class Ibus_Model(AbstractModelCPU):
    def __init__(self, queue) -> None:
        self.configure_logger(logger_name="CPU_IBUS_LOG", logger_file="cpu_ibus.log")
        super().__init__(queue)

    async def _model(self, queue):
        while True:
            transaction = await self._get_transactions(queue)
            cocotb.log.debug(f"[{__class__.__name__}][_model] {transaction}")
            self.log_operation(transaction)

    def log_operation(self, transaction, header_logged=False):
        if header_logged:
            # Log the header
            header = tabulate([], headers=["Time", "Type", "Address", "Select", "Data"], tablefmt="grid")
            self.model_logger.info(header)
            # Mark that the header has been logged
        else:
            table_data = [(
                f"{cocotb.utils.get_sim_time(units='ns')} ns",
                "read" if transaction.write == 0 else "wrote",
                hex(transaction.address<<2),
                hex(transaction.select),
                transaction.data if "x" in transaction.data.binstr else hex(transaction.data.integer)
            )]
            table = tabulate(table_data, tablefmt="grid")
            self.model_logger.info(table)
