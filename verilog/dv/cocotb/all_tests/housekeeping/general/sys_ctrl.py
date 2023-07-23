import cocotb
from cocotb.triggers import RisingEdge, ClockCycles
import cocotb.log
from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
from caravel_cocotb.caravel_interfaces import SPI
from user_design import configure_userdesign


caravel_clock = 0
user_clock = 0
core_clock = 0


@cocotb.test()
@report_test
async def clock_redirect(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=55565)
    spi_master = SPI(caravelEnv)
    debug_regs = await configure_userdesign(caravelEnv)
    error_margin = 0.1
    # calculate core clock
    await cocotb.start(calculate_clk_period(dut.uut.clock, "core clock"))
    await ClockCycles(caravelEnv.clk, 110)
    cocotb.log.info(
        f"[TEST]  core clock requency = {round(1000000/core_clock,2)} MHz period = {core_clock}ps"
    )
    await debug_regs.wait_reg1(0xAA)
    # check clk redirect working
    # user clock
    clock_name = "user clock"
    await spi_master.write_reg_spi(0x1B, 0x0)  # disable user clock output redirect
    await cocotb.start(calculate_clk_period(dut.gpio15_monitor, clock_name))
    await ClockCycles(caravelEnv.clk, 110)
    if user_clock != 0:
        cocotb.log.error(
            f"[TEST] Error: {clock_name} is directed while clk2_output_dest is disabled"
        )
    else:
        cocotb.log.info(
            f"[TEST] Pass: {clock_name} has not directed when reg clk2_output_dest is disabled"
        )

    await spi_master.write_reg_spi(0x1B, 0x2)  # enable user clock output redirect
    await cocotb.start(calculate_clk_period(dut.gpio15_monitor, clock_name))
    await ClockCycles(caravelEnv.clk, 110)
    if abs(user_clock - core_clock) > (error_margin * core_clock):
        cocotb.log.error(
            f"[TEST] Error: {clock_name} is directed with wrong value {clock_name} period = {user_clock} and core clock = {core_clock}"
        )
    else:
        cocotb.log.info(f"[TEST] Pass: {clock_name} has directed successfully")

    # caravel clock
    clock_name = "caravel clock"
    await spi_master.write_reg_spi(0x1B, 0x0)  # disable caravel clock output redirect
    await cocotb.start(calculate_clk_period(dut.gpio14_monitor, clock_name))
    await ClockCycles(caravelEnv.clk, 110)
    if caravel_clock != 0:
        cocotb.log.error(
            f"[TEST] Error: {clock_name} is directed while clk2_output_dest is disabled"
        )
    else:
        cocotb.log.info(
            f"[TEST] Pass: {clock_name} has not directed when reg clk2_output_dest is disabled"
        )

    await spi_master.write_reg_spi(0x1B, 0x4)  # enable caravel clock output redirect
    await cocotb.start(calculate_clk_period(dut.gpio15_monitor, clock_name))
    await ClockCycles(caravelEnv.clk, 110)
    if abs(caravel_clock - core_clock) > error_margin * core_clock:
        cocotb.log.error(
            f"[TEST] Error: {clock_name} is directed with wrong value {clock_name} period = {caravel_clock} and core clock = {core_clock}"
        )
    else:
        cocotb.log.info(f"[TEST] Pass: {clock_name} has directed successfully")


async def calculate_clk_period(clk, name):
    await RisingEdge(clk)
    initial_time = cocotb.simulator.get_sim_time()
    initial_time = (initial_time[0] << 32) | (initial_time[1])
    for i in range(100):
        await RisingEdge(clk)
    end_time = cocotb.simulator.get_sim_time()
    end_time = (end_time[0] << 32) | (end_time[1])
    val = (end_time - initial_time) / 100
    cocotb.log.debug(f"[TEST] clock of {name} is {val}")
    if name == "caravel clock":
        global caravel_clock
        caravel_clock = val
    elif name == "user clock":
        global user_clock
        user_clock = val
    elif name == "core clock":
        global core_clock
        core_clock = val
    return val


@cocotb.test()
@report_test
async def hk_disable(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=51474)
    spi_master = SPI(caravelEnv)
    debug_regs = await configure_userdesign(caravelEnv)
    debug_regs = await configure_userdesign(caravelEnv)
    try:
        hk_hdl = dut.uut.chip_core.housekeeping
    except AttributeError:
        hk_hdl = dut.uut.chip_core.housekeeping_alt
    # check spi working by writing to PLL enables
    old_pll_enable = hk_hdl.pll_ena.value.integer
    cocotb.log.info(f"[TEST] pll_enable = {old_pll_enable}")
    await spi_master.write_reg_spi(0x8, 1 - old_pll_enable)

    pll_enable = hk_hdl.pll_ena.value.integer
    cocotb.log.info(f"[TEST] pll_enable = {pll_enable}")
    if pll_enable == 1 - old_pll_enable:
        cocotb.log.info(
            f"[TEST] Pass: SPI swap pll_enable value from {old_pll_enable} to {pll_enable}"
        )
    else:
        cocotb.log.error(
            f"[TEST] Error: SPI isn't working correctly it cant change pll from {old_pll_enable} to {1-old_pll_enable}"
        )
    old_pll_enable = hk_hdl.pll_ena.value.integer
    cocotb.log.info(f"[TEST] pll_enable = {old_pll_enable}")
    await spi_master.write_reg_spi(0x8, 1 - old_pll_enable)
    pll_enable = hk_hdl.pll_ena.value.integer
    cocotb.log.info(f"[TEST] pll_enable = {pll_enable}")
    if pll_enable == 1 - old_pll_enable:
        cocotb.log.info(
            f"[TEST] Pass: SPI swap pll_enable value from {old_pll_enable} to {pll_enable}"
        )
    else:
        cocotb.log.error(
            f"[TEST] Error: SPI isn't working correctly it cant change pll from {old_pll_enable} to {1-old_pll_enable}"
        )

    # disable Housekeeping SPIca
    await spi_master.write_reg_spi(0x6F, 0x1)

    # try to change pll_en
    old_pll_enable = hk_hdl.pll_ena.value.integer
    cocotb.log.debug(f"[TEST] pll_enable = {old_pll_enable}")
    await spi_master.write_reg_spi(0x8, 1 - old_pll_enable)
    pll_enable = hk_hdl.pll_ena.value.integer
    cocotb.log.debug(f"[TEST] pll_enable = {pll_enable}")
    if pll_enable == 1 - old_pll_enable:
        cocotb.log.error(
            f"[TEST] Error: SPI swap pll_enable value from {old_pll_enable} to {pll_enable} while housekeeping spi is disabled"
        )
    else:
        cocotb.log.info(
            "[TEST] pass: SPI isn't working when SPI housekeeping is disabled"
        )

    # enable SPI housekeeping through firmware
    await debug_regs.wait_reg2(0xBB)  # start waiting on reg1 AA
    debug_regs.write_debug_reg1_backdoor(0xAA)
    await debug_regs.wait_reg1(0xBB)  # enabled the housekeeping

    old_pll_enable = hk_hdl.pll_ena.value.integer
    cocotb.log.debug(f"[TEST] pll_enable = {old_pll_enable}")
    await spi_master.write_reg_spi(0x8, 1 - old_pll_enable)
    pll_enable = hk_hdl.pll_ena.value.integer
    cocotb.log.debug(f"[TEST] pll_enable = {pll_enable}")
    if pll_enable == 1 - old_pll_enable:
        cocotb.log.info(
            "[TEST] Pass: Housekeeping SPI has been enabled correctly through firmware"
        )
    else:
        cocotb.log.error(
            "[TEST] Error: Housekeeping SPI failed to be enabled through firmware"
        )
