import cocotb
from wb_models.housekeeping_model.hk_monitor import HK_Monitor
from wb_models.housekeeping_model.spi_coverage import SPI_Coverage
from cocotb.queue import Queue
from collections import namedtuple
from cocotb_coverage.coverage import coverage_db

SPI_Operation = namedtuple("SPI_Operation", ["command", "address", "data_in", "data_out"])


class HK_Model():
    def __init__(self, caravelEnv) -> None:
        self.caravelEnv = caravelEnv
        self._thread = cocotb.scheduler.add(self._spi())

    async def _spi(self):
        spi_cov = SPI_Coverage()
        queue = Queue()
        HK_Monitor(self.caravelEnv, queue)
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
                if bits_counter == 15:
                    address = hex(int(address, 2))
            else:
                if "read" in command:
                    data_read += str(transaction.sdo)
                if "write" in command:
                    data_write += str(transaction.sdi)
                if (bits_counter - 15) % 8 == 0:  # if it's multiple of 8 bits
                    if data_write != "":
                        data_in.append(hex(int(data_write, 2)))
                    if data_read != "":
                        data_out.append(hex(int(data_read, 2)))
                    spi_operation = SPI_Operation(command=command, address=address, data_in=data_in, data_out=data_out)
                    spi_cov.spi_cov(spi_operation)
                    cocotb.log.debug(f"[{__class__.__name__}][_housekeeping] {spi_operation} ")




    async def _get_transactions(self, queue):
        transaction = await queue.get()
        cocotb.log.debug(f"[{__class__.__name__}][spi_get_transactions] getting transaction {transaction} from queuq")
        return transaction