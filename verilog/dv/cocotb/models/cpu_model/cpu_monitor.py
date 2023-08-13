import cocotb
from cocotb.triggers import RisingEdge
from collections import namedtuple

WB_Transaction = namedtuple("WB_Transaction", ["address", "write", "data", "select"])


class CPU_Monitor():
    def __init__(self, Caravel_env, dbus_queue, ibus_queue):
        self.cpu_hdl = Caravel_env.caravel_hdl.soc.core.VexRiscv
        self._dbus_fork = cocotb.scheduler.add(self._dbus_monitor(dbus_queue))
        self._ibus_fork = cocotb.scheduler.add(self._ibus_monitor(ibus_queue))

    async def _dbus_monitor(self, queue):
        self._dbus_hdls()
        while True:
            # valid transaction only happened if ack is sent
            await RisingEdge(self.dbus_ack_hdl)
            is_write = self.dbus_we_hdl.value.integer
            transaction = WB_Transaction(address=self.dbus_adr_hdl.value.integer, write=is_write, data=self.dbus_data_write_hdl.value if is_write else self.dbus_data_read_hdl.value, select=self.dbus_sel_hdl.value.integer)
            queue.put_nowait(transaction)
            cocotb.log.debug(f"[{__class__.__name__}][_dbus_monitor] sending transaction {transaction} to queuq")
    
    async def _ibus_monitor(self, queue):
        self._ibus_hdls()
        while True:
            # valid transaction only happened if ack is sent
            await RisingEdge(self.ibus_ack_hdl)
            is_write = self.ibus_we_hdl.value.integer
            transaction = WB_Transaction(address=self.ibus_adr_hdl.value.integer, write=is_write, data=self.ibus_data_write_hdl.value if is_write else self.ibus_data_read_hdl.value, select=self.ibus_sel_hdl.value.integer)
            queue.put_nowait(transaction)
            cocotb.log.debug(f"[{__class__.__name__}][_ibus_monitor] sending transaction {transaction} to queuq")

    def _dbus_hdls(self):
        self.dbus_clk_hdl = self.cpu_hdl.clk
        self.dbus_rst_hdl = self.cpu_hdl.reset
        self.dbus_adr_hdl = self.cpu_hdl.dBusWishbone_ADR
        self.dbus_data_read_hdl = self.cpu_hdl.dBusWishbone_DAT_MISO
        self.dbus_sel_hdl = self.cpu_hdl.dBusWishbone_SEL
        self.dbus_we_hdl = self.cpu_hdl.dBusWishbone_WE
        self.dbus_cyc_hdl = self.cpu_hdl.dBusWishbone_CYC
        self.dbus_stb_hdl = self.cpu_hdl.dBusWishbone_STB
        self.dbus_ack_hdl = self.cpu_hdl.dBusWishbone_ACK
        self.dbus_data_write_hdl = self.cpu_hdl.dBusWishbone_DAT_MOSI

    def _ibus_hdls(self):
        self.ibus_clk_hdl = self.cpu_hdl.clk
        self.ibus_rst_hdl = self.cpu_hdl.reset
        self.ibus_adr_hdl = self.cpu_hdl.iBusWishbone_ADR
        self.ibus_data_read_hdl = self.cpu_hdl.iBusWishbone_DAT_MISO
        self.ibus_sel_hdl = self.cpu_hdl.iBusWishbone_SEL
        self.ibus_we_hdl = self.cpu_hdl.iBusWishbone_WE
        self.ibus_cyc_hdl = self.cpu_hdl.iBusWishbone_CYC
        self.ibus_stb_hdl = self.cpu_hdl.iBusWishbone_STB
        self.ibus_ack_hdl = self.cpu_hdl.iBusWishbone_ACK
        self.ibus_data_write_hdl = self.cpu_hdl.iBusWishbone_DAT_MOSI

