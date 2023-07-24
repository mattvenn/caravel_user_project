import cocotb
from wb_models.housekeeping_model.hk_monitor import HK_Monitor
from cocotb.queue import Queue

class HK_Model():
    def __init__(self, caravelEnv) -> None:
        self.caravelEnv = caravelEnv
        # self._thread = cocotb.scheduler.add(self._housekeeping())

    async def _housekeeping(self):
        queue = Queue()
        HK_Monitor(self.caravelEnv, queue)
        bits_counter = -1
        command = address = data_write = data_read = ""
        while True:
            transaction = await self._get_transactions(queue)
            bits_counter += 1
            if transaction.cs == 1:
                bits_counter = -1
                command = address = data_write = data_read = ""
                continue
            elif bits_counter < 8:
                command += str(transaction.sdi)
            elif bits_counter < 16:
                address += str(transaction.sdi)
            else:
                if command == "read":
                    data_read += str(transaction.sdo)
                elif command == "write":
                    data_write += str(transaction.sdo)
            cocotb.log.info(f"[{__class__.__name__}][_housekeeping] command = {command} address = {address} data_write = {data_write} data_read = {data_read}")

    async def _get_transactions(self, queue):
        transaction = await queue.get()
        cocotb.log.info(f"[{__class__.__name__}][spi_get_transactions] getting transaction {transaction} from queuq")
        return transaction
