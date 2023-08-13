import cocotb
from caravel_cocotb.vip import WishboneInterface
from caravel_cocotb.vip import RegisterFile
from cocotb.triggers import Edge, First, ClockCycles
from models.housekeeping_model.hk_model import HK_Model
from models.soc_model.soc_model import SOC_Model
from models.user_project_model.user_model import UserModel
from models.gpio_model.gpio_model import GPIOs_Model
from models.cpu_model.cpu_model import CPU_Model


class UserDesign:
    def __init__(self, caravelEnv, used_addr=None, gpio_test=None, la_test=False):
        self.caravelEnv = caravelEnv
        inputs, outputs, IOs, LAs = self.get_hdls(caravelEnv)
        self._initalize_outputs([outputs["ack"], outputs["data"], LAs["out"], IOs["out"]])
        self.debug_regs = DebugRegs(caravelEnv)
        regfile = self.debug_regs.get_regs()
        if used_addr is not None:
            regfile = FullAddrSpaceRegs(used_addr).get_regs()
        self.wb = WishboneInterface(inputs, outputs, regfile)
        self.la_test = la_test
        self.la_testing = LA_Testing(LAs)
        self.gpio_test = GPIO_Testing(caravelEnv, gpio_test, self.debug_regs, IOs)

    def get_hdls(self, caravelEnv):
        inputs = {"clk": caravelEnv.user_hdl.wb_clk_i, "rst": caravelEnv.user_hdl.wb_rst_i, "stb": caravelEnv.user_hdl.wbs_stb_i, "we": self.caravelEnv.user_hdl.wbs_we_i, "cyc": caravelEnv.user_hdl.wbs_cyc_i, "sel": caravelEnv.user_hdl.wbs_sel_i, "addr": caravelEnv.user_hdl.wbs_adr_i, "data": caravelEnv.user_hdl.wbs_dat_i}

        outputs = {"ack": caravelEnv.user_hdl.wbs_ack_o, "data": caravelEnv.user_hdl.wbs_dat_o}

        IOs = {"out": caravelEnv.user_hdl.io_out, "oeb": caravelEnv.user_hdl.io_oeb, "in": caravelEnv.user_hdl.io_in}
        
        LAs = {"in": caravelEnv.user_hdl.la_data_in, "out": caravelEnv.user_hdl.la_data_out, "oeb":caravelEnv.user_hdl.la_oenb}

        return inputs, outputs, IOs, LAs
    
    def _initalize_outputs(self, outputs: list):
        for output in outputs:
            output.value = 0

    async def start(self):
        cocotb.log.info("[UserDesign][start] start user design")
        await cocotb.start(self.wb.start())
        await cocotb.start(self.gpio_test.start())
        if self.la_test:
            await cocotb.start(self.la_testing.start())
        
        await ClockCycles(self.caravelEnv.clk, 1)
        if "RTL" in cocotb.plusargs:
            self.coverage_models()
    
    def coverage_models(self):
        self.hk_model = HK_Model(self.caravelEnv)
        self.SOC_model = SOC_Model(self.caravelEnv)
        self.user_model = UserModel(self.caravelEnv)
        self.gpios_model = GPIOs_Model(self.caravelEnv)
        self.cpu_model = CPU_Model(self.caravelEnv)
        cocotb.plusargs["COVERAGE_COLLECT"] = True


class DebugRegs():
    def __init__(self, caravelEnv, addr_1=0x300FFFF8, addr_2=0x300FFFFC):
        """by default use the last two registers in user space"""
        self.reg_file = RegisterFile()
        self.reg_file.add_register("debug_reg_1", addr_1)
        self.reg_file.add_register("debug_reg_2", addr_2)
        self.caravelEnv = caravelEnv
        self.addr_1 = addr_1
        self.addr_2 = addr_2

    def get_regs(self):
        return self.reg_file

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
        return self.reg_file.read(self.addr_1)

    def read_debug_reg2(self):
        return self.reg_file.read(self.addr_2)

    def read_debug_reg1_str(self):
        return bin(self.reg_file.read(self.addr_1))[2:]

    def read_debug_reg2_str(self):
        return bin(self.reg_file.read(self.addr_2))[2:]

    # writing debug registers using backdoor because in GL
    # cpu can't be disabled for now because of different netlist names
    def write_debug_reg1_backdoor(self, data):
        self.reg_file.write(self.addr_1, data)

    def write_debug_reg2_backdoor(self, data):
        self.reg_file.write(self.addr_2, data)


class FullAddrSpaceRegs():
    def __init__(self, used_addr):
        """ add register in the whole address space"""
        self.reg_file = RegisterFile()
        unique_elements_set = set(used_addr)
        for address in unique_elements_set:
            self.reg_file.add_register(f"reg_{hex(address)[2:]}", address, reset_val=0x777)

    def get_regs(self):
        return self.reg_file


class GPIO_Testing:
    def __init__(self, caravelEnv, test, debug_regs, IOs):
        self.caravelEnv = caravelEnv
        self.test = test
        self.debug_regs = debug_regs
        self.IOs = IOs
    
    async def start(self):
        if self.test is not None:
            cocotb.log.info("[GPIO_Testing][start] start gpio testing")
            await cocotb.start(self.test(self.caravelEnv, self.debug_regs, self.IOs))


class LA_Testing:
    def __init__(self, LAs):
        self.la_in = LAs["in"]
        self.la_out = LAs["out"]
        self.la_oeb = LAs["oeb"]

    async def drive_out(self):
        """drive the la_out based on the value of la_in and la_oeb"""
        la_in_edge = Edge(self.la_in)
        la_oeb_edge = Edge(self.la_oeb)
        # wait over any change in la in or la out
        while True:
            await First(la_in_edge, la_oeb_edge)
            cocotb.log.debug(f"[LA_Testing][drive_out] la_in = {self.la_in.value.binstr}, la_oeb = {self.la_oeb.value.binstr}")
            la_oeb_binary = self.la_oeb.value.binstr[::-1]
            la_in_binary = self.la_in.value.binstr[::-1]
            for i, oeb in enumerate(la_oeb_binary):
                if i < 32:
                    if oeb == "1":
                        cocotb.log.debug(f"[LA_Testing][drive_out] drive la_out[{i}] = {la_in_binary[i+32]}")
                        self.la_out[i].value = int(la_in_binary[i+32])
                elif i < 64:
                    if oeb == "1":
                        cocotb.log.debug(f"[LA_Testing][drive_out] drive la_out[{i}] = {la_in_binary[i-32]}")
                        self.la_out[i].value = int(la_in_binary[i-32])
                elif i < 96:
                    if oeb == "1":
                        cocotb.log.debug(f"[LA_Testing][drive_out] drive la_out[{i}] = {la_in_binary[i+32]}")
                        self.la_out[i].value = int(la_in_binary[i+32])
                elif i < 128:
                    if oeb == "1":
                        cocotb.log.debug(f"[LA_Testing][drive_out] drive la_out[{i}] = {la_in_binary[i-32]}")
                        self.la_out[i].value = int(la_in_binary[i-32])
    
    async def start(self):
        cocotb.log.info("[LA_Testing][start] start la testing")
        await cocotb.start(self.drive_out)


async def configure_userdesign(caravelEnv, used_addr=None, gpio_test=None, la_test=False):
    user_design = UserDesign(caravelEnv, used_addr, gpio_test, la_test)
    await cocotb.start(user_design.start())
    debug_regs = user_design.debug_regs
    return debug_regs
