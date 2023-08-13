import cocotb
from cocotb.triggers import RisingEdge,  Edge, FallingEdge, ClockCycles, NextTimeStep
from collections import namedtuple

UART_Transaction = namedtuple("UART_Transaction", ["type", "char"])
SPI_Transaction = namedtuple("SPI_Transaction", ["cs", "sdi", "sdo"])


class SOC_Monitor():
    def __init__(self, Caravel_env, spi_queue, uart_queue, debug_queue, irq_queue):
        self.clk = Caravel_env.clk
        self.soc_hdl = Caravel_env.caravel_hdl.soc
        self._uart_fork = cocotb.scheduler.add(self._soc_uart_monitor(uart_queue, 9600))
        self._spi_fork = cocotb.scheduler.add(self._soc_spi_monitoring(spi_queue))
        self._debug_fork = cocotb.scheduler.add(self._soc_debug_monitor(debug_queue, 115200))
        self._irq_fork = cocotb.scheduler.add(self._soc_irq_monitor(irq_queue))

    async def _soc_spi_monitoring(self, queue):
        self._spi_hdls()
        while True:
            if self.cs_hdl.value.integer == 1:
                transaction = SPI_Transaction(cs=1, sdi=0, sdo=0)
                queue.put_nowait(transaction)
                cocotb.log.debug(f"[{__class__.__name__}][_soc_spi_monitoring] sending transaction {transaction} to queuq")
                await Edge(self.cs_hdl)  # wait until cs is low
            await RisingEdge(self.clk_hdl)
            transaction = SPI_Transaction(cs=self.cs_hdl.value, sdi=self.sdi_hdl.value.binstr if self.sdi_hdl.value.binstr != "x" else "0", sdo=self.sdo_hdl.value)
            queue.put_nowait(transaction)
            cocotb.log.debug(f"[{__class__.__name__}][_soc_spi_monitoring] sending transaction {transaction} to queuq")

    async def _soc_uart_monitor(self, queue, baudrate):
        self._uart_hdls()
        bit_cycles = round(1.01 * 10**7 / (baudrate))
        cocotb.log.debug(f"[{__class__.__name__}][_soc_uart_monitor] bit_cycles: {bit_cycles}")
        while True:
            if self.wb_uart_en_hdl.value.integer == 0:
                await Edge(self.wb_uart_en_hdl)  # wait until uart is enabled
            rx_fork = await cocotb.start(self._soc_uart_rx_monitor(queue, bit_cycles))
            tx_fork = await cocotb.start(self._soc_uart_tx_monitor(queue, bit_cycles))
            await Edge(self.wb_uart_en_hdl)  # wait until uart is disabled
            rx_fork.kill()
            tx_fork.kill()

    async def _soc_debug_monitor(self, queue, baudrate):
        self._debug_hdls()
        bit_cycles = round(1.01 * 10**7 / (baudrate))
        cocotb.log.debug(f"[{__class__.__name__}][_soc_debug_monitor] bit_cycles: {bit_cycles}")
        while True:
            if self.wb_debug_mode_hdl.value.integer == 0:
                await Edge(self.wb_debug_mode_hdl)  # wait until uart is enabled
            rx_fork = await cocotb.start(self._soc_uart_rx_monitor(queue, bit_cycles, not_ascii=True))
            tx_fork = await cocotb.start(self._soc_uart_tx_monitor(queue, bit_cycles, not_ascii=True))
            await Edge(self.wb_debug_mode_hdl)  # wait until uart is disabled
            rx_fork.kill()
            tx_fork.kill()

    async def _soc_uart_rx_monitor(self, queue, bit_cycles, not_ascii=False):
        while True:
            char = ""
            await FallingEdge(self.wb_uart_rx_hdl)  # start of char
            await ClockCycles(self.clk, bit_cycles+1)
            await NextTimeStep()
            for i in range(8):
                char = self.wb_uart_rx_hdl.value.binstr + char
                await ClockCycles(self.clk, bit_cycles+1)
                await NextTimeStep()
            transaction = UART_Transaction(
                type="rx", char=chr(int(char, 2)) if not not_ascii else hex(int(char, 2)))
            queue.put_nowait(transaction)
            cocotb.log.debug(f"[{__class__.__name__}][_soc_uart_rx_monitor] sending transaction {transaction} to queue")

    async def _soc_uart_tx_monitor(self, queue, bit_cycles, not_ascii=False):
        while True:
            char = ""
            await FallingEdge(self.wb_uart_tx_hdl)
            await ClockCycles(self.clk, bit_cycles)
            for i in range(8):
                char = self.wb_uart_tx_hdl.value.binstr + char
                await ClockCycles(self.clk, bit_cycles)
            transaction = UART_Transaction(
                type="tx", char=chr(int(char, 2)) if not not_ascii else hex(int(char, 2)))
            queue.put_nowait(transaction)
            cocotb.log.debug(f"[{__class__.__name__}][_soc_uart_tx_monitor] sending transaction {transaction} to queue")
        
    async def _soc_irq_monitor(self, queue):
        self._irq_hdls()
        irq_arr_old = "00000000000000000000000000000000"
        transaction = [] # list of changed bits
        while True:
            await Edge(self.irq_arr_hdl)
            irq_arr = self.irq_arr_hdl.value.binstr[::-1]
            for i in range(32):
                if irq_arr[i] != irq_arr_old[i]:
                    transaction.append((i, "interrupt" if irq_arr[i] == "1" else "clear"))
            irq_arr_old = irq_arr
            queue.put_nowait(transaction)
            cocotb.log.debug(f"[{__class__.__name__}][_soc_irq_monitor] sending transaction {transaction} to queue ")

    def _uart_hdls(self):
        self.wb_uart_en_hdl = self.soc_hdl.uart_enabled
        self.wb_uart_rx_hdl = self.soc_hdl.ser_rx
        self.wb_uart_tx_hdl = self.soc_hdl.ser_tx

    def _debug_hdls(self):
        self._uart_hdls()
        self.wb_debug_mode_hdl = self.soc_hdl.debug_mode

    def _spi_hdls(self):
        self.cs_hdl = self.soc_hdl.spi_csb
        self.clk_hdl = self.soc_hdl.spi_sck
        self.sdi_hdl = self.soc_hdl.spi_sdi
        self.sdo_hdl = self.soc_hdl.spi_sdo
        self.sdo_enb_hdl = self.soc_hdl.spi_sdoenb

    def _irq_hdls(self):
        self.irq_arr_hdl = self.soc_hdl.core.VexRiscv.externalInterruptArray
