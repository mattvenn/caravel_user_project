import cocotb
from cocotb.triggers import ClockCycles, Edge
import cocotb.log
from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
from caravel_cocotb.caravel_interfaces import UART
from user_design import configure_userdesign


@cocotb.test()
@report_test
async def uart_tx(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=444465)
    debug_regs = await configure_userdesign(caravelEnv)
    cocotb.log.info("[TEST] Start uart test")
    expected_msg = "Monitor: Test UART (RTL) passed"
    uart = UART(caravelEnv)
    # wait for start of sending
    await debug_regs.wait_reg1(0xAA)
    msg = await uart.get_line()
    if msg == expected_msg:
        cocotb.log.info(f"[TEST] Pass recieve the full expected msg '{msg}'")
    else:
        cocotb.log.error(
            f"[TEST] recieved wrong msg from uart msg recieved:'{msg}' expected '{expected_msg}'"
        )


@cocotb.test()
@report_test
async def uart_rx(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=188729)
    debug_regs = await configure_userdesign(caravelEnv)
    uart = UART(caravelEnv)
    cocotb.log.info("[TEST] Start uart test")
    # IO[0] affects the uart selecting btw system and debug
    caravelEnv.drive_gpio_in((0, 0), 0)
    caravelEnv.drive_gpio_in((5, 5), 1)
    # send first char
    await debug_regs.wait_reg1(0xAA)
    await uart.uart_send_char("B")
    await uart_check_char_recieved(caravelEnv, debug_regs)
    # send second char
    await debug_regs.wait_reg1(0xBB)
    await uart.uart_send_char("M")
    await uart_check_char_recieved(caravelEnv, debug_regs)
    # send third char
    await debug_regs.wait_reg1(0xCC)
    await uart.uart_send_char("A")
    await uart_check_char_recieved(caravelEnv, debug_regs)


async def uart_check_char_recieved(caravelEnv, debug_regs):
    # check cpu recieved the correct character
    while True:
        if 'GL' not in caravelEnv.design_macros._asdict():
            if 'CPU_TYPE_ARM' in caravelEnv.design_macros._asdict():
                reg_uart_data = (
                    caravelEnv.caravel_hdl.soc.core.AHB.APB_S3.S3_UART.reg_rx_buf.value.binstr
                )
            else:
                reg_uart_data = caravelEnv.caravel_hdl.soc.core.uart_rxtx_w.value.binstr
        else:
            reg_uart_data = "1001110"

        reg2 = debug_regs.read_debug_reg2()
        cocotb.log.debug(f"[TEST] reg2 = {hex(reg2)}")
        if reg2 == 0x1B:
            cocotb.log.info(
                f"[TEST] Pass cpu has recieved the correct character {chr(int(reg_uart_data,2))}({reg_uart_data})"
            )
            return
        if reg2 == 0x1E:
            cocotb.log.error(
                f"[TEST] Failed cpu has recieved the wrong character {chr(int(reg_uart_data,2))}({reg_uart_data})"
            )
            return

        await ClockCycles(caravelEnv.clk, 1)


@cocotb.test()
@report_test
async def uart_loopback(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=216759)
    debug_regs = await configure_userdesign(caravelEnv)
    cocotb.log.info("[TEST] Start uart test")
    debug_regs = await configure_userdesign(caravelEnv)
    await cocotb.start(connect_5_6(dut, caravelEnv))  # short gpio 6 and 5
    caravelEnv.drive_gpio_in(
        (0, 0), 0
    )  # IO[0] affects the uart selecting btw system and debug

    # setup watcher loopback results
    await cocotb.start(uart_check_char_recieved_loopback(caravelEnv, debug_regs))

    await ClockCycles(caravelEnv.clk, 197000)


async def connect_5_6(dut, caravelEnv):
    while True:
        caravelEnv.drive_gpio_in(5, dut.gpio6_monitor.value)
        await Edge(dut.gpio6_monitor)


async def uart_check_char_recieved_loopback(caravelEnv, debug_regs):
    # check cpu recieved the correct character
    while True:
        if 'GL' not in caravelEnv.design_macros._asdict():
            if 'CPU_TYPE_ARM' in caravelEnv.design_macros._asdict():
                reg_uart_data = (
                    caravelEnv.caravel_hdl.soc.core.AHB.APB_S3.S3_UART.reg_rx_buf.value.binstr
                )
            else:
                reg_uart_data = caravelEnv.caravel_hdl.soc.core.uart_rxtx_w.value.binstr
        else:
            reg_uart_data = "1001110"

        reg2 = debug_regs.read_debug_reg2()
        cocotb.log.debug(f"[TEST] reg2 = {hex(reg2)}")
        if reg2 == 0x1B:
            cocotb.log.info(
                f"[TEST] Pass cpu has sent and recieved the correct character {chr(int(reg_uart_data,2))}"
            )
            await debug_regs.wait_reg2(0)

        if reg2 == 0x1E:
            cocotb.log.error(
                f"[TEST] Failed cpu has sent and recieved the wrong character {chr(int(reg_uart_data,2))}"
            )
            await debug_regs.wait_reg2(0)

        await ClockCycles(caravelEnv.clk, 1)

@cocotb.test()
@report_test
async def uart_rx_msg(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=111154409)
    uart = UART(caravelEnv)
    debug_regs = await configure_userdesign(caravelEnv)
    # IO[0] affects the uart selecting btw system and debug
    caravelEnv.drive_gpio_in((0, 0), 0)
    caravelEnv.drive_gpio_in((5, 5), 1)
    await debug_regs.wait_reg1(0xAA)
    await ClockCycles(caravelEnv.clk, 30)
    msg = "Hello+World; "
    await uart.uart_send_line(msg)
    msg_received = await uart.get_line()
    if msg_received != msg:
        cocotb.log.error(
            f"[TEST] recieved wrong msg from uart msg recieved:'{msg_received}' expected '{msg}'"
        )
    else:
        cocotb.log.info(f"[TEST] Pass recieve the full expected msg '{msg}'")