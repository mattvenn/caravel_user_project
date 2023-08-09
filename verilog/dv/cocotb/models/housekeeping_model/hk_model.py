import cocotb
from models.housekeeping_model.hk_monitor import HK_Monitor
from models.housekeeping_model.hk_coverage import SPI_Coverage
from models.housekeeping_model.hk_coverage import WB_Coverage
from models.housekeeping_model.hk_regs import HK_Registers
from cocotb.queue import Queue
from collections import namedtuple
import logging
from tabulate import tabulate


SPI_Operation = namedtuple("SPI_Operation", ["command", "address", "data_in", "data_out"])


class HK_Model():
    def __init__(self, caravelEnv) -> None:
        self.caravelEnv = caravelEnv
        spi_queue = Queue()
        wb_queue = Queue()
        HK_Monitor(self.caravelEnv, spi_queue, wb_queue)
        hk_regs = HK_Registers(caravelEnv)
        SPI_Model(spi_queue, hk_regs)
        WB_Model(wb_queue, hk_regs)


class AbstractModelHK():
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


class WB_Model(AbstractModelHK):
    def __init__(self, queue, hk_regs) -> None:
        self.configure_logger(logger_name="HK_WB_LOG", logger_file="hk_wb.log")
        super().__init__(queue)
        self.hk_regs = hk_regs

    async def _model(self, queue):
        wb_cov = WB_Coverage()
        while True:
            transaction = await self._get_transactions(queue)
            cocotb.log.debug(f"[{__class__.__name__}][_model] {transaction}")
            self.log_operation(transaction)
            wb_cov.wb_cov(transaction)
            if transaction.write == 1:
                self.hk_regs.cov_register_write(transaction.address, interface="wb")
            else:
                self.hk_regs.cov_register_read(transaction.address, interface="wb")

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


class SPI_Model(AbstractModelHK):
    def __init__(self, queue, hk_regs) -> None:
        self.configure_logger(logger_name="HK_SPI_LOG", logger_file="hk_spi.log")
        super().__init__(queue)
        self.hk_regs = hk_regs

    async def _model(self, queue):
        spi_cov = SPI_Coverage()
        bits_counter = -1
        command = address = data_write = data_read = ""
        data_in = []
        data_out = []
        while True:
            transaction = await self._get_transactions(queue)
            bits_counter += 1
            if transaction.cs == 1:
                bits_counter = -1
                command = address = data_write = data_read = ""
                data_in = []
                data_out = []
                continue
            elif bits_counter < 8:
                command += str(transaction.sdi)
                if bits_counter == 7:
                    command = spi_cov.command_to_text(command)
            elif bits_counter < 16:
                address += str(transaction.sdi)
                if bits_counter == 15 and "Pass-through" not in command:
                    address = hex(int(address, 2))
            else:
                if "read" in command:
                    data_read += str(transaction.sdo)
                if "write" in command:
                    data_write += str(transaction.sdi)
                if "Pass-through" in command:
                    if bits_counter < 40:
                        address += str(transaction.sdi)
                        if bits_counter == 39:
                            address = hex(int(address, 2))
                    else: 
                        data_read += str(transaction.sdo)
                        data_write += str(transaction.sdi)

                if (bits_counter - 15) % 8 == 0:  # if it's multiple of 8 bits
                    if "Pass-through" in command and bits_counter < 40:
                        continue
                    if data_write != "":
                        data_in.append(hex(int(data_write, 2)))
                    if data_read != "":
                        data_out.append(hex(int(data_read, 2)))
                    spi_operation = SPI_Operation(command=command, address=address, data_in=data_in, data_out=data_out)
                    spi_cov.spi_cov(spi_operation)
                    if "read" in command:
                        self.hk_regs.cov_register_read(int(address,16))
                    if "write" in command:
                        self.hk_regs.cov_register_write(int(address,16))
                    self.log_operation(spi_operation)
                    cocotb.log.debug(f"[{__class__.__name__}][_housekeeping] {spi_operation} ")

    # Function to log SPI operations
    def log_operation(self, transaction, header_logged=False):
        if header_logged:
            # Log the header
            header = tabulate([], headers=["Time", "Command", "Address", "Data In", "Data Out"], tablefmt="grid")
            self.spi_logger.info(header)
            # Mark that the header has been logged
        else:
            table_data = [(
                f"{cocotb.utils.get_sim_time(units='ns')} ns",
                transaction.command,
                transaction.address,
                transaction.data_in,
                transaction.data_out
            )]
            table = tabulate(table_data, tablefmt="grid")
            self.spi_logger.info(table)
