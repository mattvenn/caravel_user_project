import cocotb
import yaml
from cocotb_coverage.coverage import CoverPoint


class HK_Registers():
    def __init__(self, caravelEnv) -> None:
        self.regs_spi = dict()
        self.regs_wb = dict()
        self.get_regs()

    def get_regs(self):
        file_name = f"{cocotb.plusargs['USER_PROJECT_ROOT']}/verilog/dv/cocotb/models/housekeeping_model/hk_regs.yaml"
        file_name = file_name.replace('"', '')
        with open(file_name, "r") as file:
            regs = yaml.safe_load(file)["registers"]
        for reg in regs:
            register = HK_Register(reg["name"], reg["spi_address"], reg["wb_addr"], reg["width"], reg["reset"], reg["access_type"], reg["backdoor_hdl"])
            if isinstance(reg["spi_address"], list):
                for spi_addr in reg["spi_address"]:
                    self.regs_spi[int(spi_addr)] = register
            else:
                self.regs_spi[int(reg["spi_address"])] = register
            if isinstance(reg["wb_addr"], list):
                for wb_addr in reg["wb_addr"]:
                    self.regs_wb[int(wb_addr)] = register
            else:
                self.regs_wb[int(reg["wb_addr"])] = register

    def cov_register_write(self, address, interface="spi"):
        if interface == "spi":
            if address in self.regs_spi:
                self.regs_spi[address].sample_write("write")
        elif interface == "wb":
            if address in self.regs_wb:
                self.regs_wb[address].sample_write("write", interface)

    def cov_register_read(self, address, interface="spi"):
        if interface == "spi":
            if address in self.regs_spi:
                self.regs_spi[address].sample_read("read")
        elif interface == "wb":
            if address in self.regs_wb:
                self.regs_wb[address].sample_read("read", interface)


class HK_Register():
    def __init__(self, name, spi_addr, wb_addr, width, reset=0, access_type="rw", backdoor_hdl=None) -> None:
        self.name = name
        self.spi_addr = spi_addr
        self.wb_addr = wb_addr
        self.width = width
        self.access_type = access_type
        self.reset = reset
        self.value = reset
        self.backdoor_hdl = backdoor_hdl
        self.mask = (1 << width) - 1
        cocotb.log.debug(f"[{__class__.__name__}][__init__] Create register {name} at wishbone address {wb_addr}, spi address {spi_addr} with width {width} reset {reset} access_type {access_type}")
        # initialize coverage no covearge happened just sample nothing so the coverge is initialized
        self.sample_write("null")
        self.sample_read("null")
        self.sample_write("null", interface="wb")
        self.sample_read("null", interface="wb")

    def __str__(self):
        return f"Housekeeping register {self.name} at address spi address {self.spi_addr}, wb address {hex(self.wb_addr)} with width {hex(self.width)}, reset {hex(self.reset)}, access_type {self.access_type}, backdoor_hdl {self.backdoor_hdl}"
    def write(self, data):
        self.value = data & self.mask
        cocotb.log.debug(f"[{__class__.__name__}][write] write {self.value} to register {self.name}")

    def read(self):
        cocotb.log.debug(f"[{__class__.__name__}][read] read {self.value} from register {self.name}")
        return self.value

    def reset(self):
        cocotb.log.debug(f"[{__class__.__name__}][reset] reset {self.name}")
        self.write(self.reset)

    def sample_write(self, data, interface="spi"):
        @CoverPoint(
            f"top.caravel.housekeeping.registers.{self.name}.{interface}_write",
            bins=["write" if "w" in self.access_type else "null"],
        )
        def sample(data):
            pass
        sample(data)

    def sample_read(self, data, interface="spi"):
        @CoverPoint(
            f"top.caravel.housekeeping.registers.{self.name}.{interface}_read",
            bins=["read" if "r" in self.access_type else "null"],
        )
        def sample(data):
            pass
        sample(data)
