import cocotb
from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
from all_tests.gpio.gpio_seq import gpio_all_o_seq
from all_tests.gpio.gpio_seq import gpio_all_i_seq
from all_tests.gpio.gpio_seq import gpio_all_i_pu_seq
from all_tests.gpio.gpio_seq import gpio_all_i_pd_seq
from user_design import configure_userdesign


@cocotb.test()
@report_test
async def gpio_all_o(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=1999191)
    debug_regs = await configure_userdesign(caravelEnv)
    await gpio_all_o_seq(dut, caravelEnv, debug_regs)


@cocotb.test()
@report_test
async def gpio_all_i(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=295677)
    debug_regs = await configure_userdesign(caravelEnv)
    await gpio_all_i_seq(dut, caravelEnv, debug_regs)


@cocotb.test()
@report_test
async def gpio_all_i_pu(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=69978)
    debug_regs = await configure_userdesign(caravelEnv)
    await gpio_all_i_pu_seq(dut, caravelEnv, debug_regs)


@cocotb.test()
@report_test
async def gpio_all_i_pd(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=69978)
    debug_regs = await configure_userdesign(caravelEnv)
    await gpio_all_i_pd_seq(dut, caravelEnv, debug_regs)
