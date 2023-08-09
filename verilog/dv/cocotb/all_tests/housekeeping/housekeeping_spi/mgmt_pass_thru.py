import cocotb
from cocotb.triggers import FallingEdge, RisingEdge
from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
from caravel_cocotb.caravel_interfaces import SPI
from random import randrange
from user_design import configure_userdesign
from all_tests.common.read_hex import ReadHex
import random

bit_time_ns = 0


@cocotb.test()
@report_test
async def mgmt_pass_thru_rd(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=37247)
    spi_master = SPI(caravelEnv)
    debug_regs = await configure_userdesign(caravelEnv)
    hex_path = f"{cocotb.plusargs['SIM_DIR']}/{cocotb.plusargs['FTESTNAME']}/firmware.hex".replace('"', "")
    hex_dict = ReadHex(hex_path).read_hex()
    # check 10 read random address with diffrent read bytes numbers
    for _ in range(10):
        rand_key = random.choice(list(hex_dict.keys()))
        rand_address = random.choice(hex_dict[rand_key])
        address = rand_key + rand_address
        bytes_num = random.randint(1, 4)
        try:
            expected_val = [hex_dict[rand_key][rand_address+i] for i in range(bytes_num)]
        except IndexError:
            continue
        val = await spi_master.reg_spi_mgmt_pass_thru_read(address, bytes_num)
        if val != expected_val:
            cocotb.log.error(f"[TEST] wrong read from hex file, address {hex(address)} expected value= {expected_val}, recieved value {val}")
        else:
            cocotb.log.info(f"[TEST] correct read from hex file, address {hex(address)} expected value= {expected_val}, recieved value {val}")