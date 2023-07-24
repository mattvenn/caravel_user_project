import cocotb
from cocotb.triggers import Timer, RisingEdge, ReadOnly, Edge
from collections import namedtuple

SPI_Transaction = namedtuple("SPI_Transaction", ["cs", "sdi", "sdo"])

class HK_Monitor():
    def __init__(self, Caravel_env, queue):
        self.hk_hdl = Caravel_env.hk_hdl
        self._thread = cocotb.scheduler.add(self._hk_spi_monitor(queue))

    async def _hk_spi_monitor(self, queue):
        self._spi_hdls()
        while True:
            if self.spi_is_enable_hdl.value.integer == 0:
                await Edge(self.spi_is_enable_hdl)  # wait until spi is enabled
            monitor_fork = await cocotb.start(self._spi_monitoring(queue))
            await Edge(self.spi_is_enable_hdl)  # wait until spi is disabled
            monitor_fork.kill()

    async def _spi_monitoring(self, queue):
        while True:
            if self.cs_hdl.value.integer == 1:
                transaction = SPI_Transaction(cs=1, sdi=0, sdo=0)
                await queue.put(transaction)
                cocotb.log.info(f"[{__class__.__name__}][_spi_monitoring] sending transaction {transaction} to queuq")
                await Edge(self.cs_hdl)  # wait until cs is low
            await RisingEdge(self.clk_hdl)
            transaction = SPI_Transaction(cs=self.cs_hdl.value, sdi=self.sdi_hdl.value, sdo=self.sdo_hdl.value)
            await queue.put(transaction)
            cocotb.log.info(f"[{__class__.__name__}][_spi_monitoring] sending transaction {transaction} to queuq")

    def _spi_hdls(self):
        self.cs_hdl = self.hk_hdl.mgmt_gpio_in[3]
        self.clk_hdl = self.hk_hdl.mgmt_gpio_in[4]
        self.sdi_hdl = self.hk_hdl.mgmt_gpio_in[2]
        self.sdo_hdl = self.hk_hdl.mgmt_gpio_out[1]
        self.spi_is_enable_hdl = self.hk_hdl.spi_is_enabled