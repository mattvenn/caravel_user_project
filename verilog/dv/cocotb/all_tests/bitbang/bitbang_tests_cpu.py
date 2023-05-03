import cocotb
from cocotb.triggers import ClockCycles
import cocotb.log
from cocotb_includes import Regs
from cocotb_includes import test_configure
from cocotb_includes import repot_test
from cocotb_includes import GPIO_MODE
from all_tests.gpio.gpio_seq import gpio_all_o_seq
from all_tests.gpio.gpio_seq import gpio_all_i_seq
from all_tests.common.bitbang import bb_configure_all_gpios
from all_tests.housekeeping.housekeeping_spi.spi_access_functions import write_reg_spi

reg = Regs()


@cocotb.test()
@repot_test
async def bitbang_cpu_all_o(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=1111437008)
    await gpio_all_o_seq(dut, caravelEnv)


@cocotb.test()
@repot_test
async def bitbang_cpu_all_i(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=2835898)
    await gpio_all_i_seq(dut, caravelEnv)


"""Testbench of GPIO configuration through bit-bang method using the housekeeping SPI configure all gpio as output."""


@cocotb.test()
@repot_test
async def bitbang_spi_o(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=1802769)
    await gpio_all_o_seq(dut, caravelEnv, bitbang_spi_o_configure)


"""Testbench of GPIO configuration through bit-bang method using the housekeeping SPI configure all gpio as input."""


@cocotb.test()
@repot_test
async def bitbang_spi_i(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=295585)
    await gpio_all_i_seq(dut, caravelEnv, bitbang_spi_i_configure)


async def bitbang_spi_i_configure(caravelEnv, debug_regs):
    await bb_configure_all_gpios(
        GPIO_MODE.GPIO_MODE_MGMT_STD_INPUT_NOPULL.value, caravelEnv
    )

    # disable Housekeeping SPI
    await write_reg_spi(caravelEnv, 0x6F, 0x1)
    await ClockCycles(caravelEnv.clk, 1)
    debug_regs.write_debug_reg2_backdoor(0xDD)


async def bitbang_spi_o_configure(caravelEnv, debug_regs):
    cocotb.log.info(f"type {type(GPIO_MODE.GPIO_MODE_MGMT_STD_OUTPUT.value)} val = {GPIO_MODE.GPIO_MODE_MGMT_STD_OUTPUT.value} ")
    await bb_configure_all_gpios(GPIO_MODE.GPIO_MODE_MGMT_STD_OUTPUT.value, caravelEnv)
    debug_regs.write_debug_reg2_backdoor(0xDD)
