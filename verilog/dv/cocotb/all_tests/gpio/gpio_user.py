import cocotb
from cocotb.triggers import ClockCycles
import cocotb.log
from cocotb_includes import test_configure
from cocotb_includes import report_test
from all_tests.gpio.gpio_seq import gpio_all_o_seq
from all_tests.gpio.gpio_seq import gpio_all_i_seq
from all_tests.gpio.gpio_seq import gpio_all_i_pu_seq
from all_tests.gpio.gpio_seq import gpio_all_i_pd_seq
from all_tests.common.debug_regs import DebugRegs


@cocotb.test()
@report_test
async def gpio_all_o_user(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=11538624)
    await gpio_all_o_seq(dut, caravelEnv)


@cocotb.test()
@report_test
async def gpio_all_i_user(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=11498255)
    await gpio_all_i_seq(dut, caravelEnv)


@cocotb.test()
@report_test
async def gpio_all_i_pu_user(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=1154138)
    await gpio_all_i_pu_seq(dut, caravelEnv)


@cocotb.test()
@report_test
async def gpio_all_i_pd_user(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=67759)
    await gpio_all_i_pd_seq(dut, caravelEnv)


@cocotb.test()
@report_test
async def gpio_all_bidir_user(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=111266662)
    active_gpios_num = caravelEnv.active_gpios_num
    debug_regs = DebugRegs(caravelEnv)
    debug_regs = DebugRegs(caravelEnv)
    await debug_regs.wait_reg1(0x1A)
    await caravelEnv.release_csb()
    cocotb.log.info("[TEST] finish configuring ")
    i = 0x1 << (active_gpios_num - 32)
    i_temp = i
    for j in range(active_gpios_num - 32):
        await debug_regs.wait_reg2(active_gpios_num - j)
        cocotb.log.info(
            f"[Test] gpio out = {caravelEnv.monitor_gpio((active_gpios_num,0))} j = {j}"
        )
        if caravelEnv.monitor_gpio((active_gpios_num, 0)).integer != i << 32:
            cocotb.log.error(
                f"[TEST] Wrong gpio high bits output {caravelEnv.monitor_gpio((active_gpios_num,0))} instead of {bin(i<<32)}"
            )
        debug_regs.write_debug_reg1_backdoor(0xD1)  # finsh reading 1
        await debug_regs.wait_reg2(0)
        if caravelEnv.monitor_gpio((active_gpios_num, 0)).integer != 0:
            cocotb.log.error(
                f"[TEST] Wrong gpio output {caravelEnv.monitor_gpio((active_gpios_num,0))} instead of {bin(0x00000)}"
            )
        debug_regs.write_debug_reg1_backdoor(0xD0)  # finsh reading 0
        i = i >> 1
        i |= i_temp

    i = 0x80000000
    for j in range(32):
        await debug_regs.wait_reg2(32 - j)
        cocotb.log.info(
            f"[Test] gpio out = {caravelEnv.monitor_gpio((active_gpios_num,0))} j = {j}"
        )
        high_gpio_val = 0x3F
        if "CPU_TYPE_ARM" in caravelEnv.design_macros._asdict():
            high_gpio_val = 0x7  # with ARM the last 3 gpios are not configurable
        if caravelEnv.monitor_gpio((active_gpios_num, 32)).integer != high_gpio_val:
            cocotb.log.error(
                f"[TEST] Wrong gpio high bits output {caravelEnv.monitor_gpio((active_gpios_num,32))} instead of {bin(high_gpio_val)} "
            )
        if caravelEnv.monitor_gpio((31, 0)).integer != i:
            cocotb.log.error(
                f"[TEST] Wrong gpio low bits output {caravelEnv.monitor_gpio((31,0))} instead of {bin(i)}"
            )
        debug_regs.write_debug_reg1_backdoor(0xD1)  # finsh reading 1
        await debug_regs.wait_reg2(0)
        if caravelEnv.monitor_gpio((active_gpios_num, 0)).integer != 0:
            cocotb.log.error(
                f"Wrong gpio output {caravelEnv.monitor_gpio((active_gpios_num,0))} instead of {bin(0x00000)}"
            )
        debug_regs.write_debug_reg1_backdoor(0xD0)  # finsh reading 0
        i = i >> 1
        i |= 0x80000000

    # input
    caravelEnv.release_gpio((active_gpios_num, 0))
    await ClockCycles(caravelEnv.clk, 10)
    caravelEnv.drive_gpio_in((active_gpios_num, 0), 0)
    await ClockCycles(caravelEnv.clk, 10)
    await debug_regs.wait_reg1(0xAA)
    data_in = 0xFFFFFFFF
    cocotb.log.info(f"[TEST] drive {hex(data_in)} to gpio[31:0]")
    caravelEnv.drive_gpio_in((31, 0), data_in)
    await debug_regs.wait_reg1(0xBB)
    if debug_regs.read_debug_reg2() == data_in:
        cocotb.log.info(
            f"[TEST] data {hex(data_in)} sent successfully through gpio[31:0]"
        )
    else:
        cocotb.log.error(
            f"[TEST] Error: reg_mprj_datal has recieved wrong data {debug_regs.read_debug_reg2()} instead of {data_in}"
        )
    data_in = 0xAAAAAAAA
    cocotb.log.info(f"[TEST] drive {hex(data_in)} to gpio[31:0]")
    caravelEnv.drive_gpio_in((31, 0), data_in)
    await debug_regs.wait_reg1(0xCC)
    if debug_regs.read_debug_reg2() == data_in:
        cocotb.log.info(
            f"[TEST] data {hex(data_in)} sent successfully through gpio[31:0]"
        )
    else:
        cocotb.log.error(
            f"[TEST] Error: reg_mprj_datal has recieved wrong data {debug_regs.read_debug_reg2()} instead of {data_in}"
        )
    data_in = 0x55555555
    cocotb.log.info(f"[TEST] drive {hex(data_in)} to gpio[31:0]")
    caravelEnv.drive_gpio_in((31, 0), data_in)
    await debug_regs.wait_reg1(0xDD)
    if debug_regs.read_debug_reg2() == data_in:
        cocotb.log.info(
            f"[TEST] data {hex(data_in)} sent successfully through gpio[31:0]"
        )
    else:
        cocotb.log.error(
            f"[TEST] Error: reg_mprj_datal has recieved wrong data {debug_regs.read_debug_reg2()} instead of {data_in}"
        )
    data_in = 0x0
    cocotb.log.info(f"[TEST] drive {hex(data_in)} to gpio[31:0]")
    caravelEnv.drive_gpio_in((31, 0), data_in)
    await debug_regs.wait_reg1(0xD1)
    if debug_regs.read_debug_reg2() == data_in:
        cocotb.log.info(
            f"[TEST] data {hex(data_in)} sent successfully through gpio[31:0]"
        )
    else:
        cocotb.log.error(
            f"[TEST] Error: reg_mprj_datal has recieved wrong data {debug_regs.read_debug_reg2()} instead of {data_in}"
        )
    data_in = 0x3F
    data_in = int(bin(data_in).replace("0b", "")[31 - active_gpios_num:], 2)
    cocotb.log.info(f"[TEST] drive {hex(data_in)} to gpio[{active_gpios_num}:32]")
    caravelEnv.drive_gpio_in((active_gpios_num, 32), data_in)
    await debug_regs.wait_reg1(0xD2)
    if debug_regs.read_debug_reg2() == data_in:
        cocotb.log.info(
            f"[TEST] data {hex(data_in)} sent successfully through gpio[{active_gpios_num}:32]"
        )
    else:
        cocotb.log.error(
            f"[TEST] Error: reg_mprj_datah has recieved wrong data {debug_regs.read_debug_reg2()} instead of {data_in}"
        )
    data_in = 0x0
    cocotb.log.info(f"[TEST] drive {hex(data_in)} to gpio[{active_gpios_num}:32]")
    caravelEnv.drive_gpio_in((active_gpios_num, 32), data_in)
    await debug_regs.wait_reg1(0xD3)
    if debug_regs.read_debug_reg2() == data_in:
        cocotb.log.info(
            f"[TEST] data {hex(data_in)} sent successfully through gpio[{active_gpios_num}:32]"
        )
    else:
        cocotb.log.error(
            f"[TEST] Error: reg_mprj_datah has recieved wrong data {debug_regs.read_debug_reg2()} instead of {data_in}"
        )
    data_in = 0x15
    data_in = int(bin(data_in).replace("0b", "")[31 - active_gpios_num:], 2)

    cocotb.log.info(f"[TEST] drive {hex(data_in)} to gpio[{active_gpios_num}:32]")
    caravelEnv.drive_gpio_in((active_gpios_num, 32), data_in)
    await debug_regs.wait_reg1(0xD4)
    if debug_regs.read_debug_reg2() == data_in:
        cocotb.log.info(
            f"[TEST] data {hex(data_in)} sent successfully through gpio[{active_gpios_num}:32]"
        )
    else:
        cocotb.log.error(
            f"[TEST] Error: reg_mprj_datah has recieved wrong data {debug_regs.read_debug_reg2()} instead of {data_in}"
        )
    data_in = 0x2A
    data_in = int(bin(data_in).replace("0b", "")[31 - active_gpios_num:], 2)
    cocotb.log.info(f"[TEST] drive {hex(data_in)} to gpio[{active_gpios_num}:32]")
    caravelEnv.drive_gpio_in((active_gpios_num, 32), data_in)
    await debug_regs.wait_reg2(0xFF)
    cocotb.log.info("[TEST] finish")
