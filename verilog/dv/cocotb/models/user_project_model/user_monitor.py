import cocotb
from cocotb.triggers import Timer, RisingEdge, NextTimeStep, Edge, First
from collections import namedtuple
WB_Transaction = namedtuple("WB_Transaction", ["address", "write", "write_data", "read_data", "select"])


class UserMonitor():
    def __init__(self, Caravel_env, wb_queue, la_queue, la_number=128):
        self.user_hdl = Caravel_env.user_hdl
        self._wb_fork = cocotb.scheduler.add(self._wb_monitor(wb_queue))
        self._la_fork = cocotb.scheduler.add(self._la_monitor(la_queue, la_number))

    async def _wb_monitor(self, queue):
        self._wb_hdls()
        while True:
            # valid transaction only happened if ack is sent
            await RisingEdge(self.wb_ack_hdl)
            await NextTimeStep()
            read_data = 0 if self.wb_we_hdl.value.integer == 1 else self.wb_dato_hdl.value.integer
            transaction = WB_Transaction(address=self.wb_adr_hdl.value.integer, write=self.wb_we_hdl.value.integer, write_data=self.wb_datai_hdl.value.integer, read_data=read_data, select=self.wb_sel_hdl.value.integer)
            queue.put_nowait(transaction)
            cocotb.log.debug(f"[{__class__.__name__}][_wb_monitor] sending transaction {transaction} to queue")

    async def _la_monitor(self, queue, la_number=128):
        self._la_hdls()
        for i in range(la_number):
            await cocotb.start(self._la_in_bit_monitor(i, queue, la_number))
            await cocotb.start(self._la_out_bit_monitor(i, queue, la_number))

    async def _la_in_bit_monitor(self, bit, queue, la_number=128):
        old_data = self.la_in.value[bit].integer
        la_in_edge = Edge(self.la_in)
        la_oenb_edge = Edge(self.la_oenb)
        while True:
            await First(la_in_edge, la_oenb_edge)
            await NextTimeStep()
            if self.la_oenb.value[bit].integer == 0:
                if old_data != self.la_in.value[bit].integer:
                    transaction = (la_number-bit-1, self.la_in.value[bit], "in")
                    cocotb.log.debug(f"[{__class__.__name__}][_la_in_bit_monitor] sending transaction {transaction} to queue")
                    queue.put_nowait(transaction)
                    old_data = self.la_in.value[bit].integer

    async def _la_out_bit_monitor(self, bit, queue, la_number=128):
        old_data = self.la_out.value[bit].integer
        la_in_edge = Edge(self.la_in)
        la_oenb_edge = Edge(self.la_oenb)
        while True:
            await First(la_in_edge, la_oenb_edge)
            await NextTimeStep()
            if self.la_oenb.value[bit].integer == 1:
                if old_data != self.la_out.value[bit].integer:
                    transaction = (la_number-bit-1, self.la_out.value[bit], "out")
                    cocotb.log.debug(f"[{__class__.__name__}][_la_out_bit_monitor] sending transaction {transaction} to queue")
                    queue.put_nowait(transaction)
                    old_data = self.la_out.value[bit].integer

    def _wb_hdls(self):
        self.wb_clk_hdl = self.user_hdl.wb_clk_i
        self.wb_rst_hdl = self.user_hdl.wb_rst_i
        self.wb_adr_hdl = self.user_hdl.wbs_adr_i
        self.wb_datai_hdl = self.user_hdl.wbs_dat_i
        self.wb_sel_hdl = self.user_hdl.wbs_sel_i
        self.wb_we_hdl = self.user_hdl.wbs_we_i
        self.wb_cyc_hdl = self.user_hdl.wbs_cyc_i
        self.wb_stb_hdl = self.user_hdl.wbs_stb_i
        self.wb_ack_hdl = self.user_hdl.wbs_ack_o
        self.wb_dato_hdl = self.user_hdl.wbs_dat_o

    def _la_hdls(self):
        self.la_in = self.user_hdl.la_data_in
        self.la_oenb = self.user_hdl.la_oenb
        self.la_out = self.user_hdl.la_data_out
