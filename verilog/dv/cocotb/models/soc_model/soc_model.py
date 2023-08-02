import cocotb
from cocotb.queue import Queue
from models.soc_model.soc_monitor import SOC_Monitor
from models.soc_model.soc_coverage import UART_Coverage
from models.soc_model.soc_coverage import MSPI_Coverage
from models.soc_model.soc_coverage import Debug_Coverage
from models.soc_model.soc_coverage import IRQ_Coverage
import logging
from collections import namedtuple
from tabulate import tabulate

MSPI_Operation = namedtuple("MSPI_Operation", ["data_write", "data_read"])

class SOC_Model():
    def __init__(self, caravelEnv) -> None:
        self.caravelEnv = caravelEnv
        uart_queue = Queue()
        mspi_queue = Queue()
        debug_queue = Queue()
        irq_queue = Queue()
        SOC_Monitor(self.caravelEnv, spi_queue=mspi_queue, uart_queue=uart_queue, debug_queue=debug_queue, irq_queue=irq_queue)
        UART_Model(uart_queue)
        MSPI_Model(mspi_queue)
        Debug_Model(debug_queue)
        IRQ_Model(irq_queue)

class AbstractModelSOC():
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


class UART_Model(AbstractModelSOC):
    def __init__(self, queue) -> None:
        self.configure_logger(logger_name="SOC_UART_LOG", logger_file="soc_uart.log")
        super().__init__(queue)

    async def _model(self, queue):
        uart_cov = UART_Coverage()
        while True:
            transaction = await self._get_transactions(queue)
            self.log_operation(transaction)
            uart_cov.uart_cov(transaction)

    def log_operation(self, transaction, header_logged=False):
        if header_logged:
            # Log the header
            header = tabulate([], headers=["Time","Type", "character"], tablefmt="grid")
            self.spi_logger.info(header)
            # Mark that the header has been logged
        else:
            table_data = [(
                f"{cocotb.utils.get_sim_time(units='ns')} ns",
                transaction.type,
                transaction.char
            )]
            table = tabulate(table_data, tablefmt="grid")
            self.spi_logger.info(table)


class MSPI_Model(AbstractModelSOC):
    def __init__(self, queue) -> None:
        self.configure_logger(logger_name="SOC_SPI_LOG", logger_file="soc_spi.log")
        super().__init__(queue)

    async def _model(self, queue):
        spi_cov = MSPI_Coverage()
        bits_counter = -1
        data_write = data_read = ""
        while True:
            transaction = await self._get_transactions(queue)
            bits_counter += 1
            if transaction.cs == 1:
                bits_counter = -1
                data_write = data_read = ""
                continue
            else:
                data_write += str(transaction.sdo)
                data_read += str(transaction.sdi)
            if bits_counter == 7:
                command = MSPI_Operation(data_write, data_read)
                bits_counter = -1
                data_write = data_read = ""
                self.log_operation(command)
                spi_cov.spi_cov(command)

    def log_operation(self, transaction, header_logged=False):
        cocotb.log.debug(f"[{__class__.__name__}][log_operation] {transaction}")
        if header_logged:
            # Log the header
            header = tabulate([], headers=["Time", "data_write", "data_read"], tablefmt="grid")
            self.spi_logger.info(header)
            # Mark that the header has been logged
        else:
            table_data = [(
                f"{cocotb.utils.get_sim_time(units='ns')} ns",
                hex(int(transaction.data_write, 2)),
                hex(int(transaction.data_read, 2))
            )]
            table = tabulate(table_data, tablefmt="grid")
            self.spi_logger.info(table)


class Debug_Model(AbstractModelSOC):
    def __init__(self, queue) -> None:
        self.configure_logger(logger_name="SOC_DEBUG_IF_LOG", logger_file="soc_debug_if.log")
        super().__init__(queue)

    async def _model(self, queue):
        debug_cov = Debug_Coverage()
        while True:
            transaction = await self._get_transactions(queue)
            self.log_operation(transaction)
            debug_cov.debug_cov(transaction)

    def log_operation(self, transaction, header_logged=False):
        if header_logged:
            # Log the header
            header = tabulate([], headers=["Time","Type", "character"], tablefmt="grid")
            self.spi_logger.info(header)
            # Mark that the header has been logged
        else:
            table_data = [(
                f"{cocotb.utils.get_sim_time(units='ns')} ns",
                transaction.type,
                transaction.char
            )]
            table = tabulate(table_data, tablefmt="grid")
            self.spi_logger.info(table)


class IRQ_Model(AbstractModelSOC):
    def __init__(self, queue) -> None:
        self.configure_logger(logger_name="SOC_IRQ_LOG", logger_file="soc_irqs.log")
        super().__init__(queue)

    async def _model(self, queue):
        irq_cov = IRQ_Coverage()
        while True:
            transaction = await self._get_transactions(queue)
            interrupts = []
            for interrupt in transaction:
                if interrupt[0] == 0:
                    interrupts.append(("timer_interrupt", interrupt[1]))
                elif interrupt[0] == 1:
                    interrupts.append(("uart_interrupt", interrupt[1]))
                elif interrupt[0] == 2:
                    interrupts.append(("user0_interrupt", interrupt[1]))
                elif interrupt[0] == 3:
                    interrupts.append(("user1_interrupt", interrupt[1]))
                elif interrupt[0] == 4:
                    interrupts.append(("user2_interrupt", interrupt[1]))
                elif interrupt[0] == 5:
                    interrupts.append(("housekeeping_interrupt", interrupt[1]))
                elif interrupt[0] == 6:
                    interrupts.append(("external1_interrupt", interrupt[1]))
                elif interrupt[0] == 7:
                    interrupts.append(("external2_interrupt", interrupt[1]))
            for interrupt in interrupts:
                self.log_operation(interrupt)
                irq_cov.irq_cov(interrupt)

    def log_operation(self, transaction, header_logged=False):
        if header_logged:
            # Log the header
            header = tabulate([], headers=["Time","interface", "type"], tablefmt="grid")
            self.spi_logger.info(header)
            # Mark that the header has been logged
        else:
            table_data = [(
                f"{cocotb.utils.get_sim_time(units='ns')} ns",
                transaction[0],
                transaction[1]
            )]
            table = tabulate(table_data, tablefmt="grid")
            self.spi_logger.info(table)

