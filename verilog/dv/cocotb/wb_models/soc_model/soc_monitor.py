import cocotb
from cocotb.triggers import Timer,  Edge, FallingEdge, ClockCycles
from collections import namedtuple

UART_Transaction = namedtuple("UART_Transaction", ["type", "char"])


class SOC_Monitor():
    def __init__(self, Caravel_env, spi_queue):
        self.clk = Caravel_env.clk
        self.soc_hdl = Caravel_env.caravel_hdl.soc
        self._spi_fork = cocotb.scheduler.add(self._soc_uart_monitor(spi_queue, 9600))

    async def _soc_uart_monitor(self, queue, baudrate):
        self._uart_hdls()
        bit_cycles = round(1.01 * 10**7 / (baudrate))
        cocotb.log.info(f"[{__class__.__name__}][_soc_uart_monitor] bit_cycles: {bit_cycles}")
        while True:
            if self.wb_uart_en_hdl.value.integer == 0:
                await Edge(self.wb_uart_en_hdl)  # wait until uart is enabled
            rx_fork = await cocotb.start(self._soc_uart_rx_monitor(queue, bit_cycles))
            tx_fork = await cocotb.start(self._soc_uart_tx_monitor(queue, bit_cycles))
            await Edge(self.wb_uart_en_hdl)  # wait until uart is disabled
            rx_fork.kill()
            tx_fork.kill()

    async def _soc_uart_rx_monitor(self, queue, bit_cycles):
        while True:
            char = ""
            await FallingEdge(self.wb_uart_rx_hdl)  # start of char
            await ClockCycles(self.clk, bit_cycles)
            for i in range(8):
                char = self.wb_uart_rx_hdl.value.binstr + char
                await ClockCycles(self.clk, bit_cycles)
            transaction = UART_Transaction(
                type="rx", char=chr(int(char, 2)))
            queue.put_nowait(transaction)
            cocotb.log.info(f"[{__class__.__name__}][_soc_uart_rx_monitor] sending transaction {transaction} to queue")

    async def _soc_uart_tx_monitor(self, queue, bit_cycles):
        while True:
            char = ""
            await FallingEdge(self.wb_uart_tx_hdl)
            await ClockCycles(self.clk, bit_cycles)
            for i in range(8):
                char = self.wb_uart_tx_hdl.value.binstr + char
                await ClockCycles(self.clk, bit_cycles)
            transaction = UART_Transaction(
                type="tx", char=chr(int(char, 2)))
            queue.put_nowait(transaction)
            cocotb.log.info(f"[{__class__.__name__}][_soc_uart_tx_monitor] sending transaction {transaction} to queue")

    def _uart_hdls(self):
        self.wb_uart_en_hdl = self.soc_hdl.uart_enabled
        self.wb_uart_rx_hdl = self.soc_hdl.ser_rx
        self.wb_uart_tx_hdl = self.soc_hdl.ser_tx
