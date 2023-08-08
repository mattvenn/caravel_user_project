import random
import cocotb
from cocotb.triggers import ClockCycles, Timer
import cocotb.log
from caravel_cocotb.caravel_interfaces import report_test
from caravel_cocotb.caravel_interfaces import Caravel_env
from caravel_cocotb.interfaces.common_functions.test_functions import max_num_error
from caravel_cocotb.interfaces.common_functions.test_functions import read_config_file
from cocotb.binary import BinaryValue
from caravel_cocotb.interfaces.common_functions.test_functions import Timeout
from all_tests.mgmt_gpio.mgmt_gpio import blink_counter
from user_design import configure_userdesign
from cocotb.clock import Clock


@cocotb.test()
@report_test
async def PoR(dut):
    # configurations
    caravelEnv = Caravel_env(dut)
    Timeout(clk=caravelEnv.clk, cycle_num=1904502, precision=0.2)
    cocotb.scheduler.add(max_num_error(10, caravelEnv.clk))
    clock = Clock(
        caravelEnv.clk, read_config_file()["clock"], units="ns"
    )  # Create a 25ns period clock on port clk
    cocotb.start_soon(clock.start())  # Start the clock
    # drive reset with 1
    await caravelEnv.disable_csb()  #
    caravelEnv.dut.resetb_tb.value = BinaryValue(value=1, n_bits=1)
    await caravelEnv.power_up()
    await Timer(530, "ns")
    # await caravelEnv.reset() #
    await caravelEnv.disable_bins()
    debug_regs = await configure_userdesign(caravelEnv)

    # start test
    cocotb.log.info("[TEST] Start mgmt_gpio_bidir test")

    await debug_regs.wait_reg1(0xAA)
    num_blinks = random.randint(1, 20)
    cocotb.log.info(f"[TEST] start send {num_blinks} blinks")
    for i in range(num_blinks):
        if i == num_blinks - 1:  # last iteration
            debug_regs.write_debug_reg1_backdoor(0xFF)
        caravelEnv.drive_mgmt_gpio(1)
        await ClockCycles(caravelEnv.clk, 30000)
        caravelEnv.drive_mgmt_gpio(0)
        if i != num_blinks - 1:  # not last iteration
            await ClockCycles(caravelEnv.clk, 30000)
        else:
            # caravelEnv.drive_mgmt_gpio('z')
            await ClockCycles(caravelEnv.clk, 1)

    # caravelEnv.drive_mgmt_gpio('z')
    cocotb.log.info(f"[TEST] finish sending {num_blinks} blinks ")

    cocotb.log.info(f"[TEST] waiting for {num_blinks} blinks ")
    counter = [0]  # list to pass by ref
    # forked
    await cocotb.start(blink_counter(caravelEnv.get_mgmt_gpi_hdl(), counter))
    await debug_regs.wait_reg2(0xFF)
    recieved_blinks = counter[0]
    if recieved_blinks == num_blinks:
        cocotb.log.info(f"[TEST] recieved the correct number of blinks {num_blinks}")
    else:
        cocotb.log.error(
            f"[TEST] recieved the incorrect number of blinks recieved = {recieved_blinks} expected = {num_blinks}"
        )
    cocotb.log.info(f"[TEST] counter =  {counter}")

    if recieved_blinks == num_blinks:
        cocotb.log.info(f"[TEST] recieved the correct number of blinks {num_blinks}")
    else:
        cocotb.log.error(
            f"[TEST] recieved the incorrect number of blinks recieved = {recieved_blinks} expected = {num_blinks}"
        )
