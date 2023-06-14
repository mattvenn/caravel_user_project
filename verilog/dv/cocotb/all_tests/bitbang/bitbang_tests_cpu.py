import cocotb
from cocotb.triggers import ClockCycles
import cocotb.log
from cocotb_includes import Regs
from cocotb_includes import test_configure
from cocotb_includes import report_test
from cocotb_includes import GPIO_MODE
from all_tests.gpio.gpio_seq import gpio_all_o_seq
from all_tests.gpio.gpio_seq import gpio_all_i_seq
from all_tests.common.bitbang import bb_configure_all_gpios
from cocotb_includes import SPI

reg = Regs()


@cocotb.test()
@report_test
async def bitbang_cpu_all_o(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=5004275)
    await gpio_all_o_seq(dut, caravelEnv)


@cocotb.test()
@report_test
async def bitbang_cpu_all_i(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=3311179)
    await gpio_all_i_seq(dut, caravelEnv)


"""Testbench of GPIO configuration through bit-bang method using the housekeeping SPI configure all gpio as output."""


@cocotb.test()
@report_test
async def bitbang_spi_o(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=2008592)
    await gpio_all_o_seq(dut, caravelEnv, bitbang_spi_o_configure)


"""Testbench of GPIO configuration through bit-bang method using the housekeeping SPI configure all gpio as input."""


@cocotb.test()
@report_test
async def bitbang_spi_i(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=316406)
    await gpio_all_i_seq(dut, caravelEnv, bitbang_spi_i_configure)


async def bitbang_spi_i_configure(caravelEnv, debug_regs):
    spi_master = SPI(caravelEnv)
    await caravelEnv.disable_csb()
    await bb_configure_all_gpios(
        GPIO_MODE.GPIO_MODE_MGMT_STD_INPUT_NOPULL.value, spi_master
    )

    # disable Housekeeping SPI
    await spi_master.write_reg_spi( 0x6F, 0x1)
    await ClockCycles(caravelEnv.clk, 1)
    debug_regs.write_debug_reg2_backdoor(0xDD)


async def bitbang_spi_o_configure(caravelEnv, debug_regs):
    spi_master = SPI(caravelEnv)
    await caravelEnv.disable_csb()
    await bb_configure_all_gpios(GPIO_MODE.GPIO_MODE_MGMT_STD_OUTPUT.value, spi_master)
    debug_regs.write_debug_reg2_backdoor(0xDD)
