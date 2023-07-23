import cocotb
from cocotb.triggers import ClockCycles
import cocotb.log
from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
from user_design import configure_userdesign


@cocotb.test()
@report_test
async def gpio_all_o_user(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=1850952)
    debug_regs = await configure_userdesign(caravelEnv)
    await debug_regs.wait_reg1(0xAA)
    await caravelEnv.release_csb()
    cocotb.log.info("[TEST] finish configuring as user output")
    i = 0x20
    for j in range(5):
        await debug_regs.wait_reg2(37 - j)
        cocotb.log.info(f"[Test] gpio out = {caravelEnv.monitor_gpio((37,0))} j = {j}")
        if caravelEnv.monitor_gpio((37, 0)).integer != i << 32:
            cocotb.log.error(
                f"[TEST] Wrong gpio high bits output {caravelEnv.monitor_gpio((37,0))} instead of {bin(i<<32)}"
            )
        await debug_regs.wait_reg2(0)
        if caravelEnv.monitor_gpio((37, 0)).integer != 0:
            cocotb.log.error(
                f"[TEST] Wrong gpio output {caravelEnv.monitor_gpio((37,0))} instead of {bin(0x00000)}"
            )
        i = i >> 1
        i |= 0x20

    i = 0x80000000
    for j in range(32):
        await debug_regs.wait_reg2(32 - j)
        cocotb.log.info(f"[Test] gpio out = {caravelEnv.monitor_gpio((37,0))} j = {j}")
        if caravelEnv.monitor_gpio((37, 32)).integer != 0x3F:
            cocotb.log.error(
                f"[TEST] Wrong gpio high bits output {caravelEnv.monitor_gpio((37,32))} instead of {bin(0x3f)} "
            )
        if caravelEnv.monitor_gpio((31, 0)).integer != i:
            cocotb.log.error(
                f"[TEST] Wrong gpio low bits output {caravelEnv.monitor_gpio((31,0))} instead of {bin(i)}"
            )
        await debug_regs.wait_reg2(0)
        if caravelEnv.monitor_gpio((37, 0)).integer != 0:
            cocotb.log.error(
                f"Wrong gpio output {caravelEnv.monitor_gpio((37,0))} instead of {bin(0x00000)}"
            )

        i = i >> 1
        i |= 0x80000000

    await debug_regs.wait_reg1(0xBB)
    data_in = 0x8F66FD7B
    cocotb.log.info(f"[TEST] try send {hex(data_in)} to gpio[31:0]")
    caravelEnv.drive_gpio_in((31, 0), data_in)
    reg2 = 0
    await debug_regs.wait_reg1(0xFF)
    try:
        reg2 = debug_regs.read_debug_reg2()
        if reg2 == data_in:
            cocotb.log.error(
                f"[TEST] Error: data {hex(data_in)} driven on gpio[31:0]  is seen by firmware while gpios are configured as output"
            )
        else:
            cocotb.log.info(
                f"[TEST] driven data {hex(data_in)} sent can't be sent to gpio[31:0] when it configure as output it can see {reg2}"
            )
    except Exception:
        cocotb.log.info(
            f"[TEST] driven data {hex(data_in)} sent can't be sent to gpio[31:0] when it configure as output"
        )
        return

    await ClockCycles(caravelEnv.clk, 10)


@cocotb.test()
@report_test
async def gpio_all_i_user(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=258608)
    debug_regs = await configure_userdesign(caravelEnv)
    await debug_regs.wait_reg1(0xAA)
    cocotb.log.info("[TEST] configuration finished")
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
    cocotb.log.info(f"[TEST] drive {hex(data_in)} to gpio[37:32]")
    caravelEnv.drive_gpio_in((37, 32), data_in)
    await debug_regs.wait_reg1(0xD2)
    if debug_regs.read_debug_reg2() == data_in:
        cocotb.log.info(
            f"[TEST] data {hex(data_in)} sent successfully through gpio[37:32]"
        )
    else:
        cocotb.log.error(
            f"[TEST] Error: reg_mprj_datah has recieved wrong data {debug_regs.read_debug_reg2()} instead of {data_in}"
        )
    data_in = 0x0
    cocotb.log.info(f"[TEST] drive {hex(data_in)} to gpio[37:32]")
    caravelEnv.drive_gpio_in((37, 32), data_in)
    await debug_regs.wait_reg1(0xD3)
    if debug_regs.read_debug_reg2() == data_in:
        cocotb.log.info(
            f"[TEST] data {hex(data_in)} sent successfully through gpio[37:32]"
        )
    else:
        cocotb.log.error(
            f"[TEST] Error: reg_mprj_datah has recieved wrong data {debug_regs.read_debug_reg2()} instead of {data_in}"
        )
    data_in = 0x15
    cocotb.log.info(f"[TEST] drive {hex(data_in)} to gpio[37:32]")
    caravelEnv.drive_gpio_in((37, 32), data_in)
    await debug_regs.wait_reg1(0xD4)
    if debug_regs.read_debug_reg2() == data_in:
        cocotb.log.info(
            f"[TEST] data {hex(data_in)} sent successfully through gpio[37:32]"
        )
    else:
        cocotb.log.error(
            f"[TEST] Error: reg_mprj_datah has recieved wrong data {debug_regs.read_debug_reg2()} instead of {data_in}"
        )
    data_in = 0x2A
    cocotb.log.info(f"[TEST] drive {hex(data_in)} to gpio[37:32]")
    caravelEnv.drive_gpio_in((37, 32), data_in)
    await debug_regs.wait_reg1(0xD5)
    if debug_regs.read_debug_reg2() == data_in:
        cocotb.log.info(
            f"[TEST] data {hex(data_in)} sent successfully through gpio[37:32]"
        )
    else:
        cocotb.log.error(
            f"[TEST] Error: reg_mprj_datah has recieved wrong data {debug_regs.read_debug_reg2()} instead of {data_in}"
        )
    caravelEnv.release_gpio((37, 0))
    await debug_regs.wait_reg2(0xFF)
    if (
        caravelEnv.monitor_gpio((37, 0)).binstr != "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
    ):
        cocotb.log.error(
            f"[TEST] ERROR: firmware can write to the gpios while they are configured as input_nopull gpio= {caravelEnv.monitor_gpio((37,0))}"
        )
    else:
        cocotb.log.info(
            f"[TEST] [TEST] PASS: firmware cannot write to the gpios while they are configured as input_nopull gpio= {caravelEnv.monitor_gpio((37,0))}"
        )
    cocotb.log.info("[TEST] finish")


@cocotb.test()
@report_test
async def gpio_all_i_pu_user(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=75919, num_error=2000)
    debug_regs = await configure_userdesign(caravelEnv)
    await debug_regs.wait_reg1(0xAA)
    await caravelEnv.release_csb()
    # monitor the output of padframe module it suppose to be all ones  when no input is applied
    await ClockCycles(caravelEnv.clk, 100)
    gpio = dut.uut.padframe.mprj_io_in.value.binstr
    for i in range(38):
        if gpio[i] != "1":
            cocotb.log.error(
                f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 1 while configured as input pullup and float"
            )
    await ClockCycles(caravelEnv.clk, 1000)
    # drive gpios with zero
    data_in = 0x0
    caravelEnv.drive_gpio_in((37, 0), data_in)
    await ClockCycles(caravelEnv.clk, 1000)
    gpio = dut.uut.padframe.mprj_io_in.value.binstr
    for i in range(38):
        if gpio[i] != "0":
            cocotb.log.error(
                f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 0 while configured as input pullup and drived with 0"
            )
    await ClockCycles(caravelEnv.clk, 1000)
    # drive gpios with ones
    data_in = 0x3FFFFFFFFF
    caravelEnv.drive_gpio_in((37, 0), data_in)
    await ClockCycles(caravelEnv.clk, 1000)
    gpio = dut.uut.padframe.mprj_io_in.value.binstr
    for i in range(38):
        if gpio[i] != "1":
            cocotb.log.error(
                f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 1 while configured as input pullup and drived with 1"
            )
    await ClockCycles(caravelEnv.clk, 1000)
    # drive odd half gpios with zeros and float other half
    data_in = 0x0
    caravelEnv.drive_gpio_in((37, 0), data_in)
    for i in range(0, 38, 2):
        caravelEnv.release_gpio(i)  # release even gpios
    await ClockCycles(caravelEnv.clk, 1000)
    gpio = dut.uut.padframe.mprj_io_in.value.binstr
    for i in range(38):
        if i % 2 == 1:  # odd
            if gpio[i] != "1":
                cocotb.log.error(
                    f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 1 while configured as input pullup and drived with odd half with 0"
                )
        else:
            if gpio[i] != "0":
                cocotb.log.error(
                    f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 0 while configured as input pullup and drived with odd half with 0"
                )
    await ClockCycles(caravelEnv.clk, 1000)
    # drive even half gpios with zeros and float other half
    caravelEnv.drive_gpio_in((37, 0), data_in)
    for i in range(1, 38, 2):
        caravelEnv.release_gpio(i)  # release odd gpios
    await ClockCycles(caravelEnv.clk, 1000)
    gpio = dut.uut.padframe.mprj_io_in.value.binstr
    for i in range(38):
        if i % 2 == 1:  # odd
            if gpio[i] != "0":
                cocotb.log.error(
                    f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 0 while configured as input pullup and drived with even half with 0"
                )
        else:
            if gpio[i] != "1":
                cocotb.log.error(
                    f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 1 while configured as input pullup and drived with even half with 0"
                )
    await ClockCycles(caravelEnv.clk, 1000)
    # drive odd half gpios with ones and float other half
    data_in = 0x3FFFFFFFFF
    caravelEnv.drive_gpio_in((37, 0), data_in)
    for i in range(0, 38, 2):
        caravelEnv.release_gpio(i)  # release even gpios
    await ClockCycles(caravelEnv.clk, 1000)
    gpio = dut.uut.padframe.mprj_io_in.value.binstr
    for i in range(38):
        if gpio[i] != "1":
            cocotb.log.error(
                f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 1 while configured as input pullup and drived with odd half with 1"
            )

    await ClockCycles(caravelEnv.clk, 1000)
    # drive even half gpios with zeros and float other half
    caravelEnv.drive_gpio_in((37, 0), data_in)
    for i in range(1, 38, 2):
        caravelEnv.release_gpio(i)  # release odd gpios
    await ClockCycles(caravelEnv.clk, 1000)
    gpio = dut.uut.padframe.mprj_io_in.value.binstr
    for i in range(38):
        if gpio[i] != "1":
            cocotb.log.error(
                f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 1 while configured as input pullup and drived with even half with 1"
            )

    await ClockCycles(caravelEnv.clk, 1000)

    # drive with zeros then release all gpio
    data_in = 0x0
    caravelEnv.drive_gpio_in((37, 0), data_in)
    await ClockCycles(caravelEnv.clk, 1000)
    caravelEnv.release_gpio((37, 0))
    await ClockCycles(caravelEnv.clk, 1000)
    gpio = dut.uut.padframe.mprj_io_in.value.binstr
    for i in range(38):
        if gpio[i] != "1":
            cocotb.log.error(
                f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 1 while configured as input pullup and all released"
            )
    await ClockCycles(caravelEnv.clk, 1000)


@cocotb.test()
@report_test
async def gpio_all_i_pd_user(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=1158961, num_error=2000)
    debug_regs = await configure_userdesign(caravelEnv)
    debug_regs = await configure_userdesign(caravelEnv)
    await debug_regs.wait_reg1(0xAA)
    await caravelEnv.release_csb()
    # monitor the output of padframe module it suppose to be all ones  when no input is applied
    await ClockCycles(caravelEnv.clk, 100)
    gpio = dut.uut.padframe.mprj_io_in.value.binstr
    for i in range(38):
        if gpio[i] != "0":
            cocotb.log.error(
                f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 0 while configured as input pulldown and float"
            )
    await ClockCycles(caravelEnv.clk, 1000)
    # drive gpios with zero
    data_in = 0x0
    caravelEnv.drive_gpio_in((37, 0), data_in)
    await ClockCycles(caravelEnv.clk, 1000)
    gpio = dut.uut.padframe.mprj_io_in.value.binstr
    for i in range(38):
        if gpio[i] != "0":
            cocotb.log.error(
                f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 0 while configured as input pulldown and drived with 0"
            )
    await ClockCycles(caravelEnv.clk, 1000)
    # drive gpios with ones
    data_in = 0x3FFFFFFFFF
    caravelEnv.drive_gpio_in((37, 0), data_in)
    await ClockCycles(caravelEnv.clk, 1000)
    gpio = dut.uut.padframe.mprj_io_in.value.binstr
    for i in range(38):
        if gpio[i] != "1":
            cocotb.log.error(
                f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 1 while configured as input pulldown and drived with 1"
            )
    await ClockCycles(caravelEnv.clk, 1000)
    # drive odd half gpios with zeros and float other half
    data_in = 0x0
    caravelEnv.drive_gpio_in((37, 0), data_in)
    for i in range(0, 38, 2):
        caravelEnv.release_gpio(i)  # release even gpios
    await ClockCycles(caravelEnv.clk, 1000)
    gpio = dut.uut.padframe.mprj_io_in.value.binstr
    for i in range(38):
        if gpio[i] != "0":
            cocotb.log.error(
                f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 0 while configured as input pulldown and drived with odd half with 0"
            )

    await ClockCycles(caravelEnv.clk, 1000)
    # drive even half gpios with zeros and float other half
    caravelEnv.drive_gpio_in((37, 0), data_in)
    for i in range(1, 38, 2):
        caravelEnv.release_gpio(i)  # release odd gpios
    await ClockCycles(caravelEnv.clk, 1000)
    gpio = dut.uut.padframe.mprj_io_in.value.binstr
    for i in range(38):
        if gpio[i] != "0":
            cocotb.log.error(
                f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 0 while configured as input pulldown and drived with even half with 0"
            )
    await ClockCycles(caravelEnv.clk, 1000)
    # drive odd half gpios with ones and float other half
    data_in = 0x3FFFFFFFFF
    caravelEnv.drive_gpio_in((37, 0), data_in)
    for i in range(0, 38, 2):
        caravelEnv.release_gpio(i)  # release even gpios
    await ClockCycles(caravelEnv.clk, 1000)
    gpio = dut.uut.padframe.mprj_io_in.value.binstr
    for i in range(38):
        if i % 2 == 0:  # even
            if gpio[i] != "1":
                cocotb.log.error(
                    f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 1 while configured as input pulldown and drived with odd half with 1"
                )
        else:
            if gpio[i] != "0":
                cocotb.log.error(
                    f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 0 while configured as input pulldown and drived with odd half with 1"
                )

    await ClockCycles(caravelEnv.clk, 1000)
    # drive even half gpios with zeros and float other half
    caravelEnv.drive_gpio_in((37, 0), data_in)
    for i in range(1, 38, 2):
        caravelEnv.release_gpio(i)  # release odd gpios
    await ClockCycles(caravelEnv.clk, 1000)
    gpio = dut.uut.padframe.mprj_io_in.value.binstr
    for i in range(38):
        if i % 2 == 1:  # odd
            if gpio[i] != "1":
                cocotb.log.error(
                    f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 1 while configured as input pulldown and drived with odd half with 1"
                )
        else:
            if gpio[i] != "0":
                cocotb.log.error(
                    f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 0 while configured as input pulldown and drived with odd half with 1"
                )

    await ClockCycles(caravelEnv.clk, 1000)

    # drive with ones then release all gpio
    data_in = 0x3FFFFFFFFF
    caravelEnv.drive_gpio_in((37, 0), data_in)
    await ClockCycles(caravelEnv.clk, 1000)
    caravelEnv.release_gpio((37, 0))
    await ClockCycles(caravelEnv.clk, 1000)
    gpio = dut.uut.padframe.mprj_io_in.value.binstr
    for i in range(38):
        if gpio[i] != "0":
            cocotb.log.error(
                f"[TEST] gpio[{i}] is having wrong value {gpio[i]} instead of 0 while configured as input pulldown and all released"
            )
    await ClockCycles(caravelEnv.clk, 1000)


@cocotb.test()
@report_test
async def gpio_all_bidir_user(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=2001341)
    debug_regs = await configure_userdesign(caravelEnv)
    debug_regs = await configure_userdesign(caravelEnv)
    await debug_regs.wait_reg1(0x1A)
    await caravelEnv.release_csb()
    cocotb.log.info("[TEST] finish configuring ")
    i = 0x20
    for j in range(5):
        await debug_regs.wait_reg2(37 - j)
        cocotb.log.info(f"[Test] gpio out = {caravelEnv.monitor_gpio((37,0))} j = {j}")
        if caravelEnv.monitor_gpio((37, 0)).integer != i << 32:
            cocotb.log.error(
                f"[TEST] Wrong gpio high bits output {caravelEnv.monitor_gpio((37,0))} instead of {bin(i << 32)}"
            )
        await debug_regs.wait_reg2(0)
        if caravelEnv.monitor_gpio((37, 0)).integer != 0:
            cocotb.log.error(
                f"[TEST] Wrong gpio output {caravelEnv.monitor_gpio((37,0))} instead of {bin(0x00000)}"
            )
        i = i >> 1
        i |= 0x20

    i = 0x80000000
    for j in range(32):
        await debug_regs.wait_reg2(32 - j)
        cocotb.log.info(f"[Test] gpio out = {caravelEnv.monitor_gpio((37,0))} j = {j}")
        if caravelEnv.monitor_gpio((37, 32)).integer != 0x3F:
            cocotb.log.error(
                f"[TEST] Wrong gpio high bits output {caravelEnv.monitor_gpio((37,32))} instead of {bin(0x3f)} "
            )
        if caravelEnv.monitor_gpio((31, 0)).integer != i:
            cocotb.log.error(
                f"[TEST] Wrong gpio low bits output {caravelEnv.monitor_gpio((31,0))} instead of {bin(i)}"
            )
        await debug_regs.wait_reg2(0)
        if caravelEnv.monitor_gpio((37, 0)).integer != 0:
            cocotb.log.error(
                f"Wrong gpio output {caravelEnv.monitor_gpio((37,0))} instead of {bin(0x00000)}"
            )

        i = i >> 1
        i |= 0x80000000
    caravelEnv.release_gpio((37, 0))
    await ClockCycles(caravelEnv.clk, 10)
    caravelEnv.drive_gpio_in((31, 0), 0)
    await ClockCycles(caravelEnv.clk, 10)
    await debug_regs.wait_reg1(0xAA)
    cocotb.log.info("[TEST] configuration finished")
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
    cocotb.log.info(f"[TEST] drive {hex(data_in)} to gpio[37:32]")
    caravelEnv.drive_gpio_in((37, 32), data_in)
    await debug_regs.wait_reg1(0xD2)
    if debug_regs.read_debug_reg2() == data_in:
        cocotb.log.info(
            f"[TEST] data {hex(data_in)} sent successfully through gpio[37:32]"
        )
    else:
        cocotb.log.error(
            f"[TEST] Error: reg_mprj_datah has recieved wrong data {debug_regs.read_debug_reg2()} instead of {data_in}"
        )
    data_in = 0x0
    cocotb.log.info(f"[TEST] drive {hex(data_in)} to gpio[37:32]")
    caravelEnv.drive_gpio_in((37, 32), data_in)
    await debug_regs.wait_reg1(0xD3)
    if debug_regs.read_debug_reg2() == data_in:
        cocotb.log.info(
            f"[TEST] data {hex(data_in)} sent successfully through gpio[37:32]"
        )
    else:
        cocotb.log.error(
            f"[TEST] Error: reg_mprj_datah has recieved wrong data {debug_regs.read_debug_reg2()} instead of {data_in}"
        )
    data_in = 0x15
    cocotb.log.info(f"[TEST] drive {hex(data_in)} to gpio[37:32]")
    caravelEnv.drive_gpio_in((37, 32), data_in)
    await debug_regs.wait_reg1(0xD4)
    if debug_regs.read_debug_reg2() == data_in:
        cocotb.log.info(
            f"[TEST] data {hex(data_in)} sent successfully through gpio[37:32]"
        )
    else:
        cocotb.log.error(
            f"[TEST] Error: reg_mprj_datah has recieved wrong data {debug_regs.read_debug_reg2()} instead of {data_in}"
        )
    data_in = 0x2A
    cocotb.log.info(f"[TEST] drive {hex(data_in)} to gpio[37:32]")
    caravelEnv.drive_gpio_in((37, 32), data_in)
    await debug_regs.wait_reg1(0xD5)

    await debug_regs.wait_reg2(0xFF)

    cocotb.log.info("[TEST] finish")
    await ClockCycles(caravelEnv.clk, 10)
