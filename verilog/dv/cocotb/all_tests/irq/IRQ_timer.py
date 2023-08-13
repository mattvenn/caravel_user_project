import cocotb
from cocotb.triggers import ClockCycles
import cocotb.log
from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
from user_design import configure_userdesign

"""Testbench of GPIO configuration through bit-bang method using the StriVe housekeeping SPI."""


@cocotb.test()
@report_test
async def IRQ_timer(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=579003)
    debug_regs = await configure_userdesign(caravelEnv)
    cocotb.log.info("[TEST] Start IRQ_timer test")
    pass_list = (0x1B, 0x2B)
    fail_list = (0x1E, 0x2E)
    phases_fails = 2
    phases_passes = 0
    reg1 = 0  # buffer
    while True:
        if debug_regs.read_debug_reg2() == 0xFF:  # test finish
            break
        if reg1 != debug_regs.read_debug_reg1():
            reg1 = debug_regs.read_debug_reg1()
            if reg1 in pass_list:  # pass phase
                phases_passes += 1
                phases_fails -= 1
                if reg1 == 0x1B:
                    cocotb.log.info(
                        "[TEST] Pass interrupt is detected when timer is used"
                    )
                elif reg1 == 0x2B:
                    cocotb.log.info(
                        "[TEST] Pass interrupt isn't detected when timer isnt used"
                    )
            elif reg1 in fail_list:  # pass phase
                if reg1 == 0x1E:
                    cocotb.log.info(
                        "[TEST] Failed interrupt isn't detected when timer is used"
                    )
                elif reg1 == 0x2E:
                    cocotb.log.error(
                        "[TEST] Failed interrupt is detected when timer isnt used"
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
