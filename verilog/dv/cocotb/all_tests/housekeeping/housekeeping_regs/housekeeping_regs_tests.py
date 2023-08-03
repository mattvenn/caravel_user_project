from json.encoder import INFINITY
import random
import cocotb
from cocotb.triggers import ClockCycles
import cocotb.log
from caravel_cocotb.interfaces.cpu import RiskV 
from caravel_cocotb.interfaces.defsParser import Regs
from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
from caravel_cocotb.caravel_interfaces import SPI
from caravel_cocotb.caravel_interfaces import SPI
import json
from user_design import configure_userdesign
reg = Regs()
from models.housekeeping_model.hk_regs import HK_Registers


"""randomly write then read housekeeping regs through wishbone"""


@cocotb.test()
@report_test
async def hk_regs_wr_wb(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=111678, num_error=INFINITY)
    cpu = RiskV(dut)
    cpu.cpu_force_reset()
    hk_file = f'{cocotb.plusargs["MAIN_PATH"]}/models/housekeepingWB/HK_regs.json'
    if "gf180" in caravelEnv.design_macros._asdict():
        hk_file = (
            f'{cocotb.plusargs["MAIN_PATH"]}/models/housekeepingWB/HK_regs_gf.json'
        )
    with open(hk_file) as f:
        regs = json.load(f)
    await ClockCycles(caravelEnv.clk, 10)
    # write then read
    for i in range(random.randint(7, 20)):
        bits_num = 32
        mem = random.choice(
            ["GPIO"]
        )  # can't access 'SPI' and 'sys' register from interfaces.cpu / read or write
        key = random.choice(list(regs[mem].keys()))
        if key == "base_addr":
            continue
        key_num = int(key, 16) & 0xFC
        key = generate_key_from_num(key_num)
        address = int(key, 16) + regs[mem]["base_addr"][1]
        if address in [
            0x26000010,
            0x2600000C,
        ]:  # skip testing reg_mprj_datal and reg_mprj_datah because when reading them it's getting the gpio input value
            continue
        data_in = random.getrandbits(bits_num)
        cocotb.log.info(
            f"[TEST] Writing {bin(data_in)} to {regs[mem][key][0][0]} address {hex(address)} through wishbone"
        )
        await cpu.drive_data2address(address, data_in)
        # calculate the expected value for each bit
        data_exp = ""
        keys = [
            generate_key_from_num(key_num + 3),
            generate_key_from_num(key_num + 2),
            generate_key_from_num(key_num + 1),
            generate_key_from_num(key_num),
        ]
        for count, k in enumerate(keys):
            for i in range(
                int(bits_num / len(keys)) * (count),
                int(bits_num / len(keys)) * (count + 1),
            ):
                bit_exist = False
                if k in regs[mem].keys():
                    for field in regs[mem][k]:
                        field_shift = field[2]
                        field_size = field[3]
                        field_access = field[4]
                        i_temp = (bits_num - 1 - i) % (bits_num / 4)
                        if field_shift <= i_temp and i_temp <= (
                            field_shift + field_size - 1
                        ):
                            if field_access == "RW":
                                data_exp += bin(data_in)[2:].zfill(bits_num)[i]
                                bit_exist = True
                                break
                if not bit_exist:
                    data_exp += "0"
        await ClockCycles(caravelEnv.clk, 10)

        cocotb.log.info(f"[TEST] expected data calculated = {data_exp}")
        data_out = await cpu.read_address(address)
        cocotb.log.info(
            f"[TEST] Read {bin(data_out)} from {regs[mem][key][0][0]} address {hex(address)} through wishbone"
        )
        if data_out != int(data_exp, 2):
            cocotb.log.error(
                f"[TEST] wrong read from {regs[mem][key][0][0]} address {hex(address)} retuned val= {bin(data_out)[2:].zfill(bits_num)} expected = {data_exp}"
            )
        else:
            cocotb.log.info(
                f"[TEST] read the right value {hex(data_out)}  from {regs[mem][key][0][0]} address {hex(address)} "
            )


"""randomly write then read housekeeping regs through wishbone"""


@cocotb.test()
@report_test
async def hk_regs_wr_wb_cpu(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=294366)
    debug_regs = await configure_userdesign(caravelEnv)
    reg1 = 0  # buffer
    reg2 = 0
    regs_list = (
        "reg_hkspi_status",
        "reg_hkspi_chip_id",
        "reg_hkspi_user_id",
        "reg_hkspi_pll_ena",
        "reg_hkspi_pll_bypass",
        "reg_hkspi_irq",
        "reg_hkspi_trap",
        "reg_hkspi_pll_trim",
        "reg_hkspi_pll_source",
        "reg_hkspi_pll_divide",
        "reg_clk_out_des",
        "reg_hkspi_disable",
    )
    while True:
        if debug_regs.read_debug_reg2() == 0xFF:  # test finish
            break
        if reg1 != debug_regs.read_debug_reg1():
            reg1 = debug_regs.read_debug_reg1()
            if reg1 < 38:
                cocotb.log.error(
                    f"[TEST] error while writing 0xFFFFFFFF to reg_mprj_io_{reg1-1}"
                )
            else:
                cocotb.log.error(
                    f"[TEST] error while writing 0xFFFFFFFF to {regs_list[reg1-39]}"
                )
        if reg2 != debug_regs.read_debug_reg2():
            reg2 = debug_regs.read_debug_reg2()
            if reg1 < 38:
                cocotb.log.error(
                    f"[TEST] error while writing 0x0 to reg_mprj_io_{reg2-1}"
                )
            else:
                cocotb.log.error(
                    f"[TEST] error while writing 0x0 to {regs_list[reg1-39]}"
                )
        await ClockCycles(caravelEnv.clk, 1)


"""randomly write then read housekeeping regs through SPI"""


@cocotb.test()
@report_test
async def hk_regs_wr_spi(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=20681, num_error=0)
    spi_master = SPI(caravelEnv)
    debug_regs = await configure_userdesign(caravelEnv)
    regs = HK_Registers(caravelEnv).regs_spi
    for reg in regs.values():
        cocotb.log.debug(f"[TEST] reg {reg}")
        address = reg.spi_addr
        expected_data = reg.reset
        if reg.name in ["housekeeping_disable", "gpio_configure_3"]:
            cocotb.log.debug(f"[TEST] skipping writing to {reg.name} as to keep housekeeping spi running")
            continue
        if "w" not in reg.access_type:
            cocotb.log.warning(f"[TEST] skipping writting for {reg.name} as it has access attribute: {reg.access_type}")
            continue
        if isinstance(address, list):
            data_in = random.getrandbits(8 * len(address))
            data_list = [(data_in & (0xFF << i)) >> i for i in range(len(address))]
            cocotb.log.info(f"[TEST] start writing register {reg.name} addresses {[hex(a) for a in address]}")
            await spi_master.write_reg_spi_nbytes(address=address[0], data=data_list, n_bytes=len(data_list))
            reg.write(data_in)
        else:
            data_in = random.getrandbits(8)
            cocotb.log.info(f"[TEST] start writing {hex(data_in)} to register {reg.name} address {hex(address)}")
            await spi_master.write_reg_spi(address=address, data=data_in)
            reg.write(data_in)

    for reg in regs.values():
        cocotb.log.debug(f"[TEST] reg {reg}")
        address = reg.spi_addr
        expected_data = reg.read()
        if "r" not in reg.access_type or "w" not in reg.access_type:
            cocotb.log.warning(f"[TEST] skipping check for {reg.name} as it has access attribute: {reg.access_type}")
            continue
        if isinstance(address, list):
            cocotb.log.info(f"[TEST] start reading register {reg.name} addresses {[hex(a) for a in address]}")
            data_out_list = await spi_master.read_reg_spi_nbytes(address=address[0], n_bytes=len(address))
            data_out = 0
            cocotb.log.debug(f"[TEST] list of data read from {reg.name} data {[hex(a) for a in data_out_list]} ")
            for i in range(len(data_out_list)):
                cocotb.log.debug(f"[TEST] data_out {hex(data_out)} = data_out_list[{i}] {hex(data_out_list[i])} << (8*{i}) = {hex(data_out_list[i] << (8 * i))}")
                data_out |= data_out_list[i] << (8 * i)
        else: 
            data_out = await spi_master.read_reg_spi(address=address)
            if data_out != expected_data:
                cocotb.log.error(
                    f"[TEST] wrong read from {reg.name} address {hex(address)} retuned val= {hex(data_out)} expected = {hex(expected_data)}"
                )
            else:
                cocotb.log.info(
                    f"[TEST] read the right value {hex(data_out)}  from {reg.name} address {hex(address)} "
                )

"""check reset value of house keeping register"""

@cocotb.test()
@report_test
async def hk_regs_rst_spi(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=20681, num_error=INFINITY)
    spi_master = SPI(caravelEnv)
    debug_regs = await configure_userdesign(caravelEnv)
    regs = HK_Registers(caravelEnv).regs_spi
    for reg in regs.values():
        cocotb.log.debug(f"[TEST] reg {reg}")
        address = reg.spi_addr
        expected_data = reg.reset
        if "r" not in reg.access_type:
            cocotb.log.warning(f"[TEST] skipping check for {reg.name} as it has access attribute: {reg.access_type}")
            continue
        if isinstance(address, list):
            cocotb.log.info(f"[TEST] start reading register {reg.name} addresses {[hex(a) for a in address]}")
            data_out_list = await spi_master.read_reg_spi_nbytes(address=address[0], n_bytes=len(address))
            data_out = 0
            cocotb.log.debug(f"[TEST] list of data read from {reg.name} data {[hex(a) for a in data_out_list]} ")
            for i in range(len(data_out_list)):
                cocotb.log.debug(f"[TEST] data_out {hex(data_out)} = data_out_list[{i}] {hex(data_out_list[i])} << (8*{i}) = {hex(data_out_list[i] << (8 * i))}")
                data_out |= data_out_list[i] << (8 * i)
            if data_out != expected_data:
                cocotb.log.error(f"[TEST] wrong read from {reg.name} address {[hex(a) for a in address]} retuned val= {bin(data_out)[2:].zfill(32)} expected = {bin(expected_data)[2:].zfill(32)}")  
            else:
                cocotb.log.info(f"[TEST] read the right reset value {hex(data_out)}  from {reg.name} address {[hex(a) for a in address]} ")
        else: 
            cocotb.log.info(f"[TEST] start reading register {reg.name} address {hex(address)}")
            data_out = await spi_master.read_reg_spi(address=address)
            if data_out != expected_data:
                cocotb.log.error(f"[TEST] wrong read from {reg.name} address {hex(address)} retuned val= {bin(data_out)[2:].zfill(32)} expected = {bin(expected_data)[2:].zfill(32)}")
            else: 
                cocotb.log.info(f"[TEST] read the right reset value {hex(data_out)}  from {reg.name} address {hex(address)} ")


def generate_key_from_num(num):
    hex_string = hex(num)
    hex_list = [i for i in hex_string]
    if len(hex_list) == 3:
        hex_list.insert(2, "0")
    hex_string = "".join(hex_list)
    return hex_string
