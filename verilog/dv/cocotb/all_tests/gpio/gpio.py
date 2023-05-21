import cocotb
from cocotb_includes import test_configure
from cocotb_includes import report_test
from all_tests.gpio.gpio_seq import gpio_all_o_seq
from all_tests.gpio.gpio_seq import gpio_all_i_seq
from all_tests.gpio.gpio_seq import gpio_all_i_pu_seq
from all_tests.gpio.gpio_seq import gpio_all_i_pd_seq


@cocotb.test()
@report_test
async def gpio_all_o(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=1829526)
    await gpio_all_o_seq(dut, caravelEnv)


@cocotb.test()
@report_test
async def gpio_all_i(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=273525)
    await gpio_all_i_seq(dut, caravelEnv)


@cocotb.test()
@report_test
async def gpio_all_i_pu(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=64179)
    await gpio_all_i_pu_seq(dut, caravelEnv)


@cocotb.test()
@report_test
async def gpio_all_i_pd(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=64179)
    await gpio_all_i_pd_seq(dut, caravelEnv)
