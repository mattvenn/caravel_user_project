import cocotb
from cocotb.triggers import FallingEdge, RisingEdge, ClockCycles
import cocotb.log
from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
from all_tests.spi_master.SPI_VIP import read_mem, SPI_VIP
from user_design import configure_userdesign


@cocotb.test()
@report_test
async def spi_master_rd(dut):
    """the firmware is configured to always send clk to spi so I can't insert alot of logics reading values

    the method of testing used can't work if 2 addresses Consecutive have the same address
    """

    caravelEnv = await test_configure(dut, timeout_cycles=1362179)
    debug_regs = await configure_userdesign(caravelEnv)
    cocotb.log.info("[TEST] start spi_master_rd test")
    file_name = f'{cocotb.plusargs["USER_PROJECT_ROOT"]}/verilog/dv/cocotb/all_tests/spi_master/test_data'.replace('"', '')
    mem = read_mem(file_name)
    CSB = dut.gpio33_monitor
    SCK = dut.gpio32_monitor
    # SDO = dut.uut.chip_core.spi_sdo
    SDO = dut.gpio35_monitor
    SDI = (dut.gpio34_en, dut.gpio34)
    await cocotb.start(SPI_VIP(CSB, SCK, SDO, SDI, mem))  # fork for SPI

    addresses_to_read = (
        0x04,
        0x05,
        0x18,
        0x19,
        0x22,
        0x23,
        0x37,
        0x38,
        0x41,
        0x42,
        0x5f,
        0x60,
        0x64,
        0x70,
        0x8c,
        0x94,
        0xaa,
        0xb3,
        0xc7,
        0xd8,
        0xeb,
        0xff,
    )  # the addresses that the firmware read from mem file
    await debug_regs.wait_reg2(0xAA)
    cocotb.log.info(
        "[TEST] GPIO configuration finished ans start reading from mememory"
    )
    val = 0
    for address in addresses_to_read:
        # await debug_regs.wait_reg2(0x55) # value is ready to be read
        # wait until value change
        while True:
            if val != debug_regs.read_debug_reg1():
                break
            await ClockCycles(caravelEnv.clk, 100)

        expected_val = mem[address]
        val = debug_regs.read_debug_reg1()
        if val == expected_val:
            cocotb.log.info(
                f"[TEST] correct read of value {hex(val)} from address {hex(address)} "
            )
        else:
            cocotb.log.error(
                f"[TEST] wrong read from address {hex(address)} expected value = {hex(expected_val)} value {hex(val)}  "
            )
        # debug_regs.write_debug_reg2_backdoor(0xCC)

    await ClockCycles(caravelEnv.clk, 1000)


@cocotb.test()
@report_test
async def spi_master_temp(dut):
    """the firmware is configured to always send clk to spi so I can't insert alot of logics reading values

    the method of testing used can't work if 2 addresses Consecutive have the same address
    """
    caravelEnv = await test_configure(dut, timeout_cycles=114548)
    debug_regs = await configure_userdesign(caravelEnv)
    cocotb.log.info("[TEST] start spi_master_temp test")
    CSB = dut.gpio33_monitor
    SCK = dut.gpio32_monitor
    # SDO = dut.uut.chip_core.housekeeping.spi_sdo
    SDO = dut.gpio35_monitor
    # SDI = (dut.gpio34_en, dut.gpio34)
    await RisingEdge(CSB)
    await FallingEdge(CSB)
    await RisingEdge(SCK)
    a = ""
    b = ""
    # first value
    for i in range(8):
        a = a + SDO.value.binstr
        cocotb.log.info(f" [TEST] SDO = {SDO.value.binstr}")
        await RisingEdge(SCK)
    cocotb.log.info(f" [TEST] a = {a} = {int(a,2)}")

    # second val
    for i in range(8):
        b = b + SDO.value.binstr
        cocotb.log.info(f" [TEST] SDO = {SDO.value.binstr}")
        if i != 7:  # skip last cycle wait
            await RisingEdge(SCK)
    cocotb.log.info(f" [TEST] b = {b} = {int(b,2)}")

    s = int(a, 2) + int(b, 2)
    s_bin = bin(s)[2:].zfill(8)
    cocotb.log.info(f" [TEST] sending sum of {int(a,2)} + {int(b,2)} = {s} = {s_bin}")
    await FallingEdge(SCK)
    for i in range(8):
        dut.gpio34_en.value = 1
        dut.gpio34.value = int(s_bin[i], 2)  # bin
        cocotb.log.debug(f"[SPI_VIP] [SPI_op] SDO = {s_bin[i]} ")
        await FallingEdge(SCK)
    dut.gpio34_en.value = 0  # enable
    while True:
        if debug_regs.read_debug_reg1() == 0xBB:
            cocotb.log.info(f" [TEST] firmware recieve the right value {s}")
            break
        elif debug_regs.read_debug_reg1() == 0xEE:
            cocotb.log.error(
                f" [TEST] firmware recieve the incorrect value {debug_regs.read_debug_reg2()}  instead of {s}"
            )
            break

        await ClockCycles(caravelEnv.clk, 10)
