import cocotb
from cocotb.triggers import Timer, RisingEdge, ReadOnly, Edge
from collections import namedtuple

SPI_Transaction = namedtuple("SPI_Transaction", ["cs", "sdi", "sdo"])
WB_Transaction = namedtuple("WB_Transaction", ["address", "write", "write_data", "read_data", "select"])


class HK_Monitor():
    def __init__(self, Caravel_env, spi_queue, wb_queue):
        self.hk_hdl = Caravel_env.hk_hdl
        self._spi_fork = cocotb.scheduler.add(self._hk_spi_monitor(spi_queue))
        self._wb_fork = cocotb.scheduler.add(self._wb_monitor(wb_queue))

    async def _hk_spi_monitor(self, queue):
        self._spi_hdls()
        while True:
            if self.spi_is_enable_hdl.value.integer == 0:
                await Edge(self.spi_is_enable_hdl)  # wait until spi is enabled
            monitor_fork = await cocotb.start(self._spi_monitoring(queue))
            await Edge(self.spi_is_enable_hdl)  # wait until spi is disabled
            monitor_fork.kill()

    async def _wb_monitor(self, queue):
        self._wb_hdls()
        while True:
            # valid transaction only happened if ack is sent
            await RisingEdge(self.wb_ack_hdl)
            read_data = int(self.wb_dato_hdl.value.binstr.replace("x", "0"), 2)
            transaction = WB_Transaction(address=self.wb_adr_hdl.value.integer, write=self.wb_we_hdl.value.integer, write_data=self.wb_datai_hdl.value.integer, read_data=read_data, select=self.wb_sel_hdl.value.integer)
            queue.put_nowait(transaction)
            cocotb.log.debug(f"[{__class__.__name__}][_spi_monitoring] sending transaction {transaction} to queuq")

    async def _spi_monitoring(self, queue):
        while True:
            if self.cs_hdl.value.integer == 1:
                transaction = SPI_Transaction(cs=1, sdi=0, sdo=0)
                queue.put_nowait(transaction)
                cocotb.log.debug(f"[{__class__.__name__}][_spi_monitoring] sending transaction {transaction} to queuq")
                await Edge(self.cs_hdl)  # wait until cs is low
            await RisingEdge(self.clk_hdl)
            transaction = SPI_Transaction(cs=self.cs_hdl.value, sdi=self.sdi_hdl.value, sdo=self.sdo_hdl.value)
            queue.put_nowait(transaction)
            cocotb.log.debug(f"[{__class__.__name__}][_spi_monitoring] sending transaction {transaction} to queuq")

    def _spi_hdls(self):
        self.cs_hdl = self.hk_hdl.mgmt_gpio_in[3]
        self.clk_hdl = self.hk_hdl.mgmt_gpio_in[4]
        self.sdi_hdl = self.hk_hdl.mgmt_gpio_in[2]
        self.sdo_hdl = self.hk_hdl.mgmt_gpio_out[1]
        self.spi_is_enable_hdl = self.hk_hdl.spi_is_enabled

    def _wb_hdls(self):
        self.wb_clk_hdl = self.hk_hdl.wb_clk_i
        self.wb_rst_hdl = self.hk_hdl.wb_rstn_i
        self.wb_adr_hdl = self.hk_hdl.wb_adr_i
        self.wb_datai_hdl = self.hk_hdl.wb_dat_i
        self.wb_sel_hdl = self.hk_hdl.wb_sel_i
        self.wb_we_hdl = self.hk_hdl.wb_we_i
        self.wb_cyc_hdl = self.hk_hdl.wb_cyc_i
        self.wb_stb_hdl = self.hk_hdl.wb_stb_i
        self.wb_ack_hdl = self.hk_hdl.wb_ack_o
        self.wb_dato_hdl = self.hk_hdl.wb_dat_o
