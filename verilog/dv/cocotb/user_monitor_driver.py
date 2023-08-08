import cocotb
from cocotb.binary import BinaryValue
from collections.abc import Iterable


class UserPins:
    def __init__(self, caravelEnv) -> None:
        self.user_hdl = caravelEnv.user_hdl
        pass

    def hdls(self):
        self.io_in = self.user_hdl.io_in
        self.io_out = self.user_hdl.io_out
        self.io_oeb = self.user_hdl.io_oeb
        self.la_data_in = self.user_hdl.la_data_in
        self.la_data_out = self.user_hdl.la_data_out
        self.la_oenb = self.user_hdl.la_oenb
        self.irq0 = self.user_hdl.irq0
        self.irq1 = self.user_hdl.irq1
        self.irq2 = self.user_hdl.irq2

    def drive_io_out(self, bits, data):
        data_bits = []
        is_list = isinstance(bits, (list, tuple))
        if is_list:
            cocotb.log.debug(
                f"[UserPins] [drive_io_out] start bits[1] = {bits[1]} bits[0]= {bits[0]}"
            )
            data_bits = BinaryValue(
                value=data, n_bits=bits[0] - bits[1] + 1, bigEndian=(bits[0] < bits[1])
            )
            for i, bits2 in enumerate(range(bits[1], bits[0] + 1)):
                self.user_hdl._id(f"io_out{bits2}", False).value = data_bits[i]
                cocotb.log.debug(
                    f"[UserPins] [drive_io_out] drive gpio{bits2} with {data_bits[i]}"
                )
        else:
            self.user_hdl._id(f"io_out{bits}", False).value = data
            cocotb.log.debug(
                f"[UserPins] [drive_io_out] drive gpio{bits} with {data} and gpio{bits}_en with 1"
            )

    def drive_io_oeb(self, bits, data):
        data_bits = []
        is_list = isinstance(bits, (list, tuple))
        if is_list:
            cocotb.log.debug(
                f"[UserPins] [drive_io_oeb] start bits[1] = {bits[1]} bits[0]= {bits[0]}"
            )
            data_bits = BinaryValue(
                value=data, n_bits=bits[0] - bits[1] + 1, bigEndian=(bits[0] < bits[1])
            )
            for i, bits2 in enumerate(range(bits[1], bits[0] + 1)):
                self.user_hdl._id(f"io_oeb{bits2}", False).value = data_bits[i]
                cocotb.log.debug(
                    f"[UserPins] [drive_io_oeb] drive gpio{bits2} with {data_bits[i]}"
                )
        else:
            self.user_hdl._id(f"io_oeb{bits}", False).value = data
            cocotb.log.debug(
                f"[UserPins] [drive_io_oeb] drive gpio{bits} with {data} and gpio{bits}_en with 1"
            )
    
    def monitor_io_in(self, h_bit, l_bit=None) -> cocotb.binary.BinaryValue:
        mprj = self.user_hdl.io_in.value
        size = mprj.n_bits - 1  # size of pins array
        if isinstance(h_bit, Iterable):
            l_bit = h_bit[1]
            h_bit = h_bit[0]
        if l_bit is None:
            l_bit = h_bit
        mprj_out = self.user_hdl.io_in.value[size - h_bit: size - l_bit]
        if mprj_out.is_resolvable:
            cocotb.log.debug(
                f" [UserPins] Monitor : mprj[{h_bit}:{l_bit}] = {hex(mprj_out)}"
            )
        else:
            cocotb.log.debug(f" [caravel] Monitor : mprj[{h_bit}:{l_bit}] = {mprj_out}")
        return mprj_out