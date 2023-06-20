from cocotb.triggers import ClockCycles
import cocotb

class DebugRegs():
    def __init__(self, caravelEnv):
        self.caravelEnv = caravelEnv
        self.debug_hdl = caravelEnv
        self.debug_hdl = caravelEnv.caravel_hdl.mprj.debug

    async def wait_reg1(self, data):
        while True:
            if self.read_debug_reg1() == data:
                return
            await ClockCycles(self.caravelEnv.clk, 1)

    async def wait_reg2(self, data):
        while True:
            if self.read_debug_reg2() == data:
                return
            await ClockCycles(self.caravelEnv.clk, 1)

    def read_debug_reg1(self):
        return self.debug_hdl.debug_reg_1.value.integer

    def read_debug_reg2(self):
        return self.debug_hdl.debug_reg_2.value.integer

    def read_debug_reg1_str(self):
        return self.debug_hdl.debug_reg_1.value.binstr

    def read_debug_reg2_str(self):
        return self.debug_hdl.debug_reg_2.value.binstr

    # writing debug registers using backdoor because in GL
    # cpu can't be disabled for now because of different netlist names
    def write_debug_reg1_backdoor(self, data):
        self.debug_hdl.debug_reg_1.value = data

    def write_debug_reg2_backdoor(self, data):
        self.debug_hdl.debug_reg_2.value = data
