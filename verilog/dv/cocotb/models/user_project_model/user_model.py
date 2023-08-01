from cocotb.queue import Queue
import cocotb
import logging
from tabulate import tabulate
from models.user_project_model.user_coverage import WB_Coverage
from models.user_project_model.user_coverage import LA_Coverage
from models.user_project_model.user_monitor import UserMonitor


class UserModel():
    def __init__(self, caravelEnv) -> None:
        self.caravelEnv = caravelEnv
        wb_queue = Queue()
        la_queue = Queue()
        la_number = 128
        UserMonitor(self.caravelEnv, wb_queue=wb_queue, la_queue=la_queue, la_number=la_number)
        WB_Model(wb_queue)
        LA_Model(la_queue, la_number=la_number)


class AbstractModelUser():
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


class WB_Model(AbstractModelUser):
    def __init__(self, queue) -> None:
        self.configure_logger(logger_name="User_WB_LOG", logger_file="user_wb.log")
        super().__init__(queue)

    async def _model(self, queue):
        wb_cov = WB_Coverage()
        while True:
            transaction = await self._get_transactions(queue)
            cocotb.log.debug(f"[{__class__.__name__}][_model] {transaction}")
            self.log_operation(transaction)
            wb_cov.wb_cov(transaction)

    def log_operation(self, transaction, header_logged=False):
        if header_logged:
            # Log the header
            header = tabulate([], headers=["Time", "Type", "Address", "Select", "Data"], tablefmt="grid")
            self.spi_logger.info(header)
            # Mark that the header has been logged
        else:
            table_data = [(
                f"{cocotb.utils.get_sim_time(units='ns')} ns",
                "read" if transaction.write == 0 else "write",
                hex(transaction.address),
                hex(transaction.select),
                hex(transaction.write_data) if transaction.write == 1 else hex(transaction.read_data)
            )]
            table = tabulate(table_data, tablefmt="grid")
            self.spi_logger.info(table)


class LA_Model(AbstractModelUser):
    def __init__(self, queue, la_number=128) -> None:
        self.configure_logger(logger_name="User_LA_LOG", logger_file="user_la.log")
        self.la_number = la_number
        super().__init__(queue)

    async def _model(self, queue):
        la_cov = LA_Coverage(self.la_number)
        while True:
            transaction = await self._get_transactions(queue)
            cocotb.log.debug(f"[{__class__.__name__}][_model] {transaction}")
            self.log_operation(transaction)
            la_cov.la_cov(transaction)

    def log_operation(self, transaction, header_logged=False):
        if header_logged:
            # Log the header
            header = tabulate([], headers=["Time", "direction", "la_bit", "changed to"], tablefmt="grid")
            self.spi_logger.info(header)
            # Mark that the header has been logged
        else:
            table_data = [(
                f"{cocotb.utils.get_sim_time(units='ns')} ns",
                transaction[2],
                transaction[0],
                transaction[1]
            )]
            table = tabulate(table_data, tablefmt="grid")
            self.spi_logger.info(table)
