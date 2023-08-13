import cocotb
from cocotb.triggers import ClockCycles
import cocotb.log
from caravel_cocotb.interfaces.defsParser import Regs
from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
from user_design import configure_userdesign


async def write_reg_spi(caravelEnv, address, data):
    await caravelEnv.enable_csb()
    await caravelEnv.hk_write_byte(0x80)  # Write stream command
    await caravelEnv.hk_write_byte(
        address
    )  # Address (register 19 = GPIO bit-bang control)
    await caravelEnv.hk_write_byte(data)  # Data = 0x01 (enable bit-bang mode)
    await caravelEnv.disable_csb()


reg = Regs()
"""Testbench of GPIO configuration through bit-bang method using the StriVe housekeeping SPI."""


@cocotb.test()
@report_test
async def IRQ_uart(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=896457)
    debug_regs = await configure_userdesign(caravelEnv)
    cocotb.log.info("[TEST] Start IRQ_uart test")
    pass_list = (0x1B, 0x2B)
    fail_list = (0x1E, 0x2E)
    phases_fails = 2
    phases_passes = 0
    reg1 = 0  # buffer
    reg2 = 0  # buffer
    while True:
        if reg2 != debug_regs.read_debug_reg2():
            reg2 = debug_regs.read_debug_reg2()
            if reg2 == 0xFF:  # test finish
                break
            if reg2 == 0xAA:
                cocotb.log.info("[TEST] start sending through uart")

        if reg1 != debug_regs.read_debug_reg1():
            reg1 = debug_regs.read_debug_reg1()
            if reg1 in pass_list:  # pass phase
                phases_passes += 1
                phases_fails -= 1
                if reg1 == 0x1B:
                    cocotb.log.info(
                        "[TEST] Pass interrupt is detected when uart is sending data"
                    )
                elif reg1 == 0x2B:
                    cocotb.log.info(
                        "[TEST] Pass interrupt isn't detected when uart isnt sending data"
                    )
            elif reg1 in fail_list:  # pass phase
                if reg1 == 0x1E:
                    cocotb.log.info(
                        "[TEST] Failed interrupt isn't detected uart is sending data"
                    )
                elif reg1 == 0x2E:
                    cocotb.log.error(
                        "[TEST] Failed interrupt is detected uart isnt sending data"
                    )
            else:
                cocotb.log.error("[TEST] debug register 1 has illegal value")
        await ClockCycles(caravelEnv.clk, 1)

    if phases_fails != 0:
        cocotb.log.error(
            f"[TEST] finish with {phases_passes} phases passes and {phases_fails} phases fails"
        )
    else:
        cocotb.log.info(
            f"[TEST] finish with {phases_passes} phases passes and {phases_fails} phases fails"
        )
