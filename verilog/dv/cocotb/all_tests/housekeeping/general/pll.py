import cocotb
from cocotb.triggers import RisingEdge, ClockCycles
import cocotb.log
from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test

from user_design import configure_userdesign

caravel_clock = 0
user_clock = 0


@cocotb.test()
@report_test
async def pll(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=1147279)
    debug_regs = await configure_userdesign(caravelEnv)
    error_margin = 0.1
    debug_regs = await configure_userdesign(caravelEnv)

    await debug_regs.wait_reg1(0xA1)

    await cocotb.start(calculate_clk_period(dut.gpio14_monitor, "caravel clock"))
    await cocotb.start(calculate_clk_period(dut.gpio15_monitor, "user clock"))
    await debug_regs.wait_reg1(0xA3)
    if abs(caravel_clock - user_clock) > error_margin * caravel_clock:
        cocotb.log.error(
            f"[TEST] Error: clocks should be equal in phase 1 but caravel clock = {round(1000000/caravel_clock,2)} MHz user clock = {round(1000000/user_clock,2)} MHz"
        )
    else:
        cocotb.log.info(
            f"[TEST] pass phase 1 caravel clock = {round(1000000/caravel_clock,2)} MHz user clock = {round(1000000/user_clock,2)} MHz"
        )
    await cocotb.start(calculate_clk_period(dut.gpio14_monitor, "caravel clock"))
    await cocotb.start(calculate_clk_period(dut.gpio15_monitor, "user clock"))
    await debug_regs.wait_reg1(0xA5)
    if abs(caravel_clock - user_clock) > error_margin * caravel_clock:
        cocotb.log.error(
            f"[TEST] Error: clocks should be equal in phase 2 but caravel clock = {round(1000000/caravel_clock,2)} MHz user clock = {round(1000000/user_clock,2)} MHz"
        )
    else:
        cocotb.log.info(
            f"[TEST] pass phase 2 caravel clock = {round(1000000/caravel_clock,2)} MHz user clock = {round(1000000/user_clock,2)} MHz"
        )
    await cocotb.start(calculate_clk_period(dut.gpio14_monitor, "caravel clock"))
    await cocotb.start(calculate_clk_period(dut.gpio15_monitor, "user clock"))
    await debug_regs.wait_reg1(0xA7)
    if abs(caravel_clock - user_clock * 3) > error_margin * caravel_clock:
        cocotb.log.error(
            f"[TEST] Error: user clock shoud be 3 times caravel clock in phase 3 but caravel clock = {round(1000000/caravel_clock,2)} MHz user clock = {round(1000000/user_clock,2)} MHz"
        )
    else:
        cocotb.log.info(
            f"[TEST] pass phase 3 caravel clock = {round(1000000/caravel_clock,2)} MHz user clock = {round(1000000/user_clock,2)} MHz"
        )
    await cocotb.start(calculate_clk_period(dut.gpio14_monitor, "caravel clock"))
    await cocotb.start(calculate_clk_period(dut.gpio15_monitor, "user clock "))
    await debug_regs.wait_reg1(0xA9)
    if abs(caravel_clock - user_clock * 3) > error_margin * caravel_clock:
        cocotb.log.error(
            f"[TEST] Error: user clock shoud be 3 times caravel clock in phase 4 but caravel clock = {round(1000000/caravel_clock,2)} MHz user clock = {round(1000000/user_clock,2)} MHz"
        )
    else:
        cocotb.log.info(
            f"[TEST] pass phase 4 caravel clock = {round(1000000/caravel_clock,2)} MHz user clock = {round(1000000/user_clock,2)} MHz"
        )
    await cocotb.start(calculate_clk_period(dut.gpio14_monitor, "caravel clock"))
    await cocotb.start(calculate_clk_period(dut.gpio15_monitor, "user clock"))
    await debug_regs.wait_reg1(0xAA)
    if abs(caravel_clock - user_clock * 4) > error_margin * caravel_clock:
        cocotb.log.error(
            f"[TEST] Error: user clock shoud be 4 times caravel clock in phase 5 but caravel clock = {round(1000000/caravel_clock,2)} MHz user clock = {round(1000000/user_clock,2)} MHz"
        )
    else:
        cocotb.log.info(
            f"[TEST] pass phase 5 caravel clock = {round(1000000/caravel_clock,2)} MHz user clock = {round(1000000/user_clock,2)} MHz"
        )
    await ClockCycles(caravelEnv.clk, 10000)

    # for i in range(1000):
    #     await ClockCycles(caravelEnv.clk,10000)
    #     cocotb.log.info(f"time = {cocotb.simulator.get_sim_time()}")


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

    val = str(val)
    return val
