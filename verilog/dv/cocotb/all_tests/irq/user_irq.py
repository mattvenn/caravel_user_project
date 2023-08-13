import cocotb
from cocotb.triggers import ClockCycles
import cocotb.log
from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
from user_design import configure_userdesign

"""Testbench of GPIO configuration through bit-bang method using the StriVe housekeeping SPI."""


@cocotb.test()
@report_test
async def user0_irq(dut):
    await user_irq(dut, 0)
    
@cocotb.test()
@report_test
async def user1_irq(dut):
    await user_irq(dut, 1)
   
@cocotb.test()
@report_test
async def user2_irq(dut):
    await user_irq(dut, 2)


async def user_irq(dut, irq_num):
    caravelEnv = await test_configure(dut, timeout_cycles=295956)
    debug_regs = await configure_userdesign(caravelEnv)
    caravelEnv.user_hdl.irq0.value = 0
    caravelEnv.user_hdl.irq1.value = 0
    caravelEnv.user_hdl.irq2.value = 0
    cocotb.log.info("[TEST] Start user0_irq test")
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
            if reg2 == 0xAA:  # trigger irq
                if irq_num == 0:
                    caravelEnv.user_hdl.irq0.value = 1
                elif irq_num == 1:
                    caravelEnv.user_hdl.irq1.value = 1
                elif irq_num == 2:
                    caravelEnv.user_hdl.irq2.value = 1
        if reg1 != debug_regs.read_debug_reg1():
            reg1 = debug_regs.read_debug_reg1()
            if reg1 in pass_list:  # pass phase
                phases_passes += 1
                phases_fails -= 1
                if reg1 == 0x1B:
                    cocotb.log.info(
                        "[TEST] Pass interrupt is detected when user irq1 triggered"
                    )
                    caravelEnv.user_hdl.irq0.value = 0
                    caravelEnv.user_hdl.irq1.value = 0
                    caravelEnv.user_hdl.irq2.value = 0
                elif reg1 == 0x2B:
                    cocotb.log.info(
                        "[TEST] Pass interrupt isn't detected user irq1 cleared"
                    )
            elif reg1 in fail_list:  # pass phase
                if reg1 == 0x1E:
                    cocotb.log.error(
                        "[TEST] Failed interrupt isn't when user irq1 triggered"
                    )
                elif reg1 == 0x2E:
                    cocotb.log.error(
                        "[TEST] Failed interrupt is detected user irq1 cleared"
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