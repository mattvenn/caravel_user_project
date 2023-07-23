import cocotb
from cocotb.triggers import ClockCycles
import cocotb.log
from caravel_cocotb.interfaces.defsParser import Regs
from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
from caravel_cocotb.caravel_interfaces import SPI
from user_design import configure_userdesign

reg = Regs()
"""Testbench of GPIO configuration through bit-bang method using the StriVe housekeeping SPI."""


@cocotb.test()
@report_test
async def IRQ_external2(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=428337)
    spi_master = SPI(caravelEnv)
    debug_regs = await configure_userdesign(caravelEnv)
    cocotb.log.info("[TEST] Start IRQ_external2 test")
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
            if reg2 == 0xAA:  # assert mprj 12
                caravelEnv.drive_gpio_in((12, 12), 0)
                await spi_master.write_reg_spi(0x1C, 2)
                # cocotb.log.info(
                #     f"irq 2 = {dut.uut.chip_core.housekeeping.irq_2_inputsrc.value}"
                # )
                caravelEnv.drive_gpio_in((12, 12), 1)
                await ClockCycles(caravelEnv.clk, 10)
                caravelEnv.drive_gpio_in((12, 12), 0)

            # if reg2 == 0xBB:  # deassert mprj 12
            #     caravelEnv.drive_gpio_in((12,12),0)

        if reg1 != debug_regs.read_debug_reg1():
            reg1 = debug_regs.read_debug_reg1()
            if reg1 in pass_list:  # pass phase
                phases_passes += 1
                phases_fails -= 1
                if reg1 == 0x1B:
                    cocotb.log.info(
                        "[TEST] Pass interrupt is detected when mprj 12 asserted"
                    )
                elif reg1 == 0x2B:
                    cocotb.log.info(
                        "[TEST] Pass interrupt isn't detected when mprj 12 deasserted"
                    )
            elif reg1 in fail_list:  # pass phase
                if reg1 == 0x1E:
                    cocotb.log.error(
                        "[TEST] Failed interrupt isn't detected when mprj 12 asserted"
                    )
                elif reg1 == 0x2E:
                    cocotb.log.error(
                        "[TEST] Failed interrupt is detected when mprj 12 deasserted"
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
