import random
import cocotb
from cocotb.triggers import ClockCycles, Edge
import cocotb.log
from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test

from user_design import configure_userdesign

"""Testbench of GPIO configuration through bit-bang method using the StriVe housekeeping SPI."""


@cocotb.test()
@report_test
async def mgmt_gpio_out(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=431562)
    debug_regs = await configure_userdesign(caravelEnv)
    cocotb.log.info("[TEST] Start mgmt_gpio_out test")
    phases_fails = 3
    phases_passes = 0
    reg1 = 0  # buffer
    reg2 = 0  # buffer

    while True:
        if reg2 != debug_regs.read_debug_reg2():
            reg2 = debug_regs.read_debug_reg2()
            if reg2 == 0xFF:  # test finish
                break
        if reg1 != debug_regs.read_debug_reg1():
            reg1 = debug_regs.read_debug_reg1()
            cocotb.log.info(f"[TEST] waiting for {reg1} blinks")
            for i in range(reg1):
                while True:
                    if caravelEnv.monitor_mgmt_gpio() == "0":
                        break
                    if reg1 != debug_regs.read_debug_reg1():
                        cocotb.log.error(
                            f"[TEST] error failing to catch all blinking received: {i} expected: {reg1}"
                        )
                        return
                    await ClockCycles(caravelEnv.clk, 1)

                while True:
                    if caravelEnv.monitor_mgmt_gpio() == "1":
                        break
                    if reg1 != debug_regs.read_debug_reg1():
                        cocotb.log.error(
                            f"[TEST] error failing to catch all blinking received: {i} expected: {reg1}"
                        )
                        return
                    await ClockCycles(caravelEnv.clk, 1)
            cocotb.log.info(f"[TEST] passing sending {reg1} blinks ")
            phases_fails -= 1
            phases_passes += 1
        await ClockCycles(caravelEnv.clk, 10)

    if phases_fails != 0:
        cocotb.log.error(
            f"[TEST] finish with {phases_passes} phases passes and {phases_fails} phases fails"
        )
    else:
        cocotb.log.info(
            f"[TEST] finish with {phases_passes} phases passes and {phases_fails} phases fails"
        )


@cocotb.test()
@report_test
async def mgmt_gpio_in(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=1119535)
    caravelEnv.drive_mgmt_gpio(0)
    debug_regs = await configure_userdesign(caravelEnv)
    cocotb.log.info("[TEST] Start mgmt_gpio_in test")
    phases_fails = 3
    phases_passes = 0
    pass_list = (0x1B, 0x2B, 0xFF)
    fail_list = tuple([0xEE])
    reg1 = 0  # buffer
    reg2 = 0  # buffer
    debug_regs = await configure_userdesign(caravelEnv)

    while True:
        if reg2 != debug_regs.read_debug_reg2():
            reg2 = debug_regs.read_debug_reg2()
            if reg2 in pass_list:
                cocotb.log.info(f"[TEST] reg2 = {reg2}")
                phases_passes += 1
                phases_fails -= 1
                if reg2 == 0xFF:  # test finish
                    break
                elif reg2 == 0x1B:
                    cocotb.log.info("[TEST] pass sending 10 blink ")
                elif reg2 == 0x2B:
                    cocotb.log.info("[TEST] pass sending 20 blink ")
            if reg2 in fail_list:
                cocotb.log.error("[TEST] gpio change without sending anything")
        if reg1 != debug_regs.read_debug_reg1():
            reg1 = debug_regs.read_debug_reg1()
            cocotb.log.info(f"[TEST] start sending {reg1} blinks")
            for i in range(reg1):
                caravelEnv.drive_mgmt_gpio(1)
                await debug_regs.wait_reg2(0xAA)
                caravelEnv.drive_mgmt_gpio(0)
                await debug_regs.wait_reg2(0xBB)
            cocotb.log.info(f"[TEST] finish sending {reg1} blinks ")
        await ClockCycles(caravelEnv.clk, 10)

    if phases_fails != 0:
        cocotb.log.error(
            f"[TEST] finish with {phases_passes} phases passes and {phases_fails} phases fails"
        )
    else:
        cocotb.log.info(
            f"[TEST] finish with {phases_passes} phases passes and {phases_fails} phases fails"
        )


@cocotb.test()
@report_test
async def mgmt_gpio_bidir(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=1904514)
    debug_regs = await configure_userdesign(caravelEnv)
    cocotb.log.info("[TEST] Start mgmt_gpio_bidir test")
    debug_regs = await configure_userdesign(caravelEnv)
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
    await cocotb.start(blink_counter(caravelEnv.get_mgmt_gpi_hdl(), counter))  # forked
    await debug_regs.wait_reg2(0xFF)
    recieved_blinks = counter[0]
    if recieved_blinks == num_blinks:
        cocotb.log.info(f"[TEST] recieved the correct number of blinks {num_blinks}")
    else:
        cocotb.log.error(
            f"[TEST] recieved the incorrect number of blinks recieved = {recieved_blinks} expected = {num_blinks}"
        )
    cocotb.log.info(f"[TEST] counter =  {counter}")


async def blink_counter(hdl, counter):
    cocotb.log.info(f"[TEST] start Edge[{counter}]")
    while True:
        await Edge(hdl)
        await Edge(hdl)
        counter[0] += 1


@cocotb.test()
@report_test
async def mgmt_gpio_pu_pd(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=66129)
    debug_regs = await configure_userdesign(caravelEnv)
    cocotb.log.info("[TEST] Start mgmt_gpio_pu_pd test")
    debug_regs = await configure_userdesign(caravelEnv)

    await debug_regs.wait_reg1(0x1B)
    # caravelEnv.drive_mgmt_gpio('z')
    await ClockCycles(caravelEnv.clk, 1)
    gpio_in = dut.uut.chip_core.soc.core.gpio_in_pad
    if gpio_in.value.binstr != "1":
        cocotb.log.error(
            f"[TEST] mgmt gpio pull up didn't work correctly reading {gpio_in} instead of 1"
        )

    await debug_regs.wait_reg1(0x2B)
    # caravelEnv.drive_mgmt_gpio('z')
    await ClockCycles(caravelEnv.clk, 1)
    if gpio_in.value.binstr != "0":
        cocotb.log.error(
            f"[TEST] mgmt gpio pull down didn't work correctly reading {gpio_in} instead of 0"
        )

    await debug_regs.wait_reg1(0x3B)
    # caravelEnv.drive_mgmt_gpio('z')
    await ClockCycles(caravelEnv.clk, 1)
    if gpio_in.value.binstr != "x":
        cocotb.log.error(
            f"[TEST] mgmt gpio no pull didn't work correctly reading {gpio_in} instead of x"
        )


@cocotb.test()
@report_test
async def mgmt_gpio_disable(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=117797)
    debug_regs = await configure_userdesign(caravelEnv)
    cocotb.log.info("[TEST] Start mgmt_gpio_disable test")
    phases_fails = 2
    phases_passes = 0
    pass_list = (0x1B, 0x2B)
    fail_list = (0x1E, 0x2E)
    reg2 = 0  # buffer
    caravelEnv.drive_mgmt_gpio(1)
    debug_regs = await configure_userdesign(caravelEnv)
    while True:
        caravelEnv.drive_mgmt_gpio(1)
        if reg2 != debug_regs.read_debug_reg2():
            cocotb.log.info(f"[TEST] reg2 = {hex(reg2)}")
            reg2 = debug_regs.read_debug_reg2()
            if reg2 == 0xFF:  # test finish
                break
            if reg2 in pass_list:
                cocotb.log.info(f"[TEST] pass = {hex(reg2)}")
                phases_passes += 1
                phases_fails -= 1
            if reg2 in fail_list:
                cocotb.log.error(f"[TEST] fail = {hex(reg2)}")
        await ClockCycles(caravelEnv.clk, 1)
    caravelEnv.drive_mgmt_gpio("z")

    if phases_fails != 0:
        cocotb.log.error(
            f"[TEST] finish with {phases_passes} phases passes and {phases_fails} phases fails"
        )
    else:
        cocotb.log.info(
            f"[TEST] finish with {phases_passes} phases passes and {phases_fails} phases fails"
        )

    await debug_regs.wait_reg1(0x1A)
    if caravelEnv.monitor_mgmt_gpio() != "1":
        cocotb.log.error("[TEST] mgmt gpio output enable but output isn't working")

    await debug_regs.wait_reg1(0x2A)
    if caravelEnv.monitor_mgmt_gpio() == "1":
        cocotb.log.error("[TEST] mgmt gpio disabled but output is working")
