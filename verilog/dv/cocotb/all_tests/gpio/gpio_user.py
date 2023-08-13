import cocotb
from cocotb.triggers import ClockCycles, Edge
import cocotb.log
from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
from all_tests.gpio.gpio_seq import gpio_all_o_seq
from all_tests.gpio.gpio_seq import gpio_all_i_seq
from all_tests.gpio.gpio_seq import gpio_all_i_pu_seq
from all_tests.gpio.gpio_seq import gpio_all_i_pd_seq
from user_design import configure_userdesign


@cocotb.test()
@report_test
async def gpio_all_o_user(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=2010463)
    debug_regs = await configure_userdesign(caravelEnv, gpio_test=gpio_all_o_vip)
    await gpio_all_o_seq(dut, caravelEnv, debug_regs)

async def gpio_all_o_vip(caravelEnv, debug_regs, IOs):
    cocotb.log.debug("[gpio_all_o_vip] start gpio gpio_all_o_vip")
    IOs["oeb"].value = 0
    IOs["out"].value = 0
    active_gpios_num = caravelEnv.active_gpios_num-1
    i = 0x2000000000
    await debug_regs.wait_reg1(0xAA)
    for j in range(active_gpios_num + 1, 0, -1):
        IOs["out"].value = i
        await ClockCycles(caravelEnv.clk, 1)
        debug_regs.write_debug_reg2_backdoor(j)
        await debug_regs.wait_reg1(0xD1)  # wait until wait until test read 1
        IOs["out"].value = 0
        await ClockCycles(caravelEnv.clk, 1)
        debug_regs.write_debug_reg2_backdoor(0)
        await debug_regs.wait_reg1(0xD0)  # wait until wait until test read 0
        i >>= 1
        i |= 0x2000000000
    debug_regs.write_debug_reg1_backdoor(0xFF)
    
     

@cocotb.test()
@report_test
async def gpio_all_i_user(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=287465)
    debug_regs = await configure_userdesign(caravelEnv, gpio_test=gpio_all_i_vip)
    await gpio_all_i_seq(dut, caravelEnv, debug_regs)


async def gpio_all_i_vip(caravelEnv, debug_regs, IOs):
    cocotb.log.debug("[gpio_all_o_vip] start gpio gpio_all_i_vip")
    IOs["oeb"].value = 1
    await debug_regs.wait_reg2(0x77)
    await wait_over_input(0xAA, 0xFFFFFFFF, debug_regs, IOs["in"])
    await wait_over_input(0XBB, 0xAAAAAAAA, debug_regs, IOs["in"])
    await wait_over_input(0XCC, 0x55555555, debug_regs, IOs["in"])
    await wait_over_input(0XDD, 0x0, debug_regs, IOs["in"])
    #high
    await wait_over_input(0XD1, 0x3F, debug_regs, IOs["in"], high=True)
    await wait_over_input(0XD2, 0x00, debug_regs, IOs["in"], high=True)
    await wait_over_input(0XD3, 0x15, debug_regs, IOs["in"], high=True)
    await wait_over_input(0XD4, 0x2A, debug_regs, IOs["in"], high=True)
    debug_regs.write_debug_reg1_backdoor(0xD5)


async def wait_over_input(start_code, exp_val, debug_regs, io_in, high=False):
    debug_regs.write_debug_reg1_backdoor(start_code)
    while True:
        io_in_val = io_in.value.integer if not high else io_in.value.integer >> 32
        if io_in_val == exp_val:
            break
        await Edge(io_in)
    debug_regs.write_debug_reg2_backdoor(io_in_val)
    


@cocotb.test()
@report_test
async def gpio_all_i_pu_user(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=86252)
    debug_regs = await configure_userdesign(caravelEnv, gpio_test=gpio_all_pu_vip)
    await gpio_all_i_pu_seq(dut, caravelEnv, debug_regs)


async def gpio_all_pu_vip(caravelEnv, debug_regs, IOs):
    cocotb.log.debug("[gpio_all_o_vip] start  gpio_all_pu_vip")
    IOs["oeb"].value = 0
    IOs["out"].value = 0x3FFFFFFFFF


@cocotb.test()
@report_test
async def gpio_all_i_pd_user(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=76198)
    debug_regs = await configure_userdesign(caravelEnv, gpio_test=gpio_all_pd_vip)
    await gpio_all_i_pd_seq(dut, caravelEnv, debug_regs)


async def gpio_all_pd_vip(caravelEnv, debug_regs, IOs):
    cocotb.log.info("[gpio_all_o_vip] start gpio_all_pu_vip")
    IOs["oeb"].value = 0
    IOs["out"].value = 0


@cocotb.test()
@report_test
async def gpio_all_bidir_user(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=2259813)
    active_gpios_num = caravelEnv.active_gpios_num -1
    debug_regs = await configure_userdesign(caravelEnv, gpio_test=gpio_all_bidir_vip)
    await debug_regs.wait_reg1(0x1A)
    await caravelEnv.release_csb()
    cocotb.log.info("[TEST] finish configuring ")
    i = 0x1 << (active_gpios_num - 32)
    i_temp = i
    for j in range(active_gpios_num - 31):
        await debug_regs.wait_reg2(active_gpios_num + 1 - j)
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
    cocotb.log.info("[TEST] finish output")
    # input
    caravelEnv.release_gpio((active_gpios_num, 0))
    await ClockCycles(caravelEnv.clk, 1)
    caravelEnv.drive_gpio_in((active_gpios_num, 0), 0)
    await ClockCycles(caravelEnv.clk, 1)
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

async def gpio_all_bidir_vip(caravelEnv, debug_regs, IOs):
    IOs["oeb"].value = 0
    IOs["out"].value = 0
    active_gpios_num = caravelEnv.active_gpios_num-1
    i = 0x2000000000
    await debug_regs.wait_reg1(0x1A)
    for j in range(active_gpios_num + 1, 0, -1):
        IOs["out"].value = i
        await ClockCycles(caravelEnv.clk, 1)
        debug_regs.write_debug_reg2_backdoor(j)
        await debug_regs.wait_reg1(0xD1)  # wait until wait until test read 1
        IOs["out"].value = 0
        await ClockCycles(caravelEnv.clk, 1)
        debug_regs.write_debug_reg2_backdoor(0)
        await debug_regs.wait_reg1(0xD0)  # wait until wait until test read 0
        i >>= 1
        i |= 0x2000000000
    cocotb.log.info("[TEST] finish output vip")
    IOs["oeb"].value = 0X3FFFFFFFFF
    await ClockCycles(caravelEnv.clk, 10)
    # input 
    await wait_over_input(0xAA, 0xFFFFFFFF, debug_regs, IOs["in"])
    await wait_over_input(0XBB, 0xAAAAAAAA, debug_regs, IOs["in"])
    await wait_over_input(0XCC, 0x55555555, debug_regs, IOs["in"])
    await wait_over_input(0XDD, 0x0, debug_regs, IOs["in"])
    # high
    await wait_over_input(0XD1, 0x3F, debug_regs, IOs["in"], high=True)
    await wait_over_input(0XD2, 0x00, debug_regs, IOs["in"], high=True)
    await wait_over_input(0XD3, 0x15, debug_regs, IOs["in"], high=True)
    await wait_over_input(0XD4, 0x2A, debug_regs, IOs["in"], high=True)
    debug_regs.write_debug_reg2_backdoor(0xFF)
    