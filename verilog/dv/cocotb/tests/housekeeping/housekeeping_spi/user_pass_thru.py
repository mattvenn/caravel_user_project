import cocotb
from cocotb.triggers import FallingEdge, RisingEdge
import cocotb.log
from cocotb_includes import test_configure
from cocotb_includes import repot_test
from tests.spi_master.SPI_VIP import read_mem, SPI_VIP
from tests.housekeeping.housekeeping_spi.spi_access_functions import write_reg_spi
from tests.housekeeping.housekeeping_spi.spi_access_functions import reg_spi_user_pass_thru
from tests.housekeeping.housekeeping_spi.spi_access_functions import reg_spi_user_pass_thru_read
from random import randrange
from tests.common.debug_regs import DebugRegs


bit_time_ns = 0


@cocotb.test()
@repot_test
async def user_pass_thru_rd(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=77637)
    debug_regs = DebugRegs(caravelEnv)
    cocotb.log.info("[TEST] start spi_master_rd test")
    file_name = (
        f"{cocotb.plusargs['MAIN_PATH']}/tests/housekeeping/housekeeping_spi/test_data"
    )
    mem = read_mem(file_name)
    await cocotb.start(
        SPI_VIP(
            dut.bin8_monitor,
            dut.bin9_monitor,
            dut.bin10_monitor,
            (dut.bin11_en, dut.bin11),
            mem,
        )
    )  # fork for SPI
    await debug_regs.wait_reg1(0xAA)
    cocotb.log.info("[TEST] Configuration finished")
    # The SPI flash may need to be reset
    # 0xff and 0xAB commands are suppose to have functionality in the future but for now they would do nothing
    await write_reg_spi(
        caravelEnv, 0x02, 0xFF
    )  # 0xc2 is for appling user pass-thru command to housekeeping SPI
    await write_reg_spi(
        caravelEnv, 0x02, 0xAB
    )  # 0xc2 is for appling user pass-thru command to housekeeping SPI

    # start reading from memory
    address = 0x0
    await reg_spi_user_pass_thru(
        caravelEnv, command=0x3, address=address
    )  # read command
    for i in range(8):
        val = await reg_spi_user_pass_thru_read(caravelEnv)
        if val != mem[address]:
            cocotb.log.error(
                f"[TEST] reading incorrect value from address {hex(address)} expected = {hex(mem[address])} returened = {val}"
            )
        else:
            cocotb.log.info(
                f"[TEST] reading correct value {hex(val)} from address {hex(address)} "
            )
        address += 1

    await caravelEnv.disable_csb()

    # Wait for processor to restart
    await debug_regs.wait_reg1(0xBB)
    cocotb.log.info("[TEST] processor has restarted successfully")


@cocotb.test()
@repot_test
async def user_pass_thru_connection(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=74319)
    debug_regs = DebugRegs(caravelEnv)
    await debug_regs.wait_reg1(0xAA)
    await caravelEnv.enable_csb()
    await caravelEnv.hk_write_byte(
        0x02
    )  # Apply user pass-thru command to housekeeping SPI
    caravelEnv.drive_gpio_in(4, 0)  # finish the clock cycle
    await FallingEdge(caravelEnv.clk)
    # check sdo and clk are following the spi
    for i in range(randrange(10, 50)):
        clk = randrange(0, 2)  # drive random value from 0 to 3 to clk and SDO
        sdo = randrange(0, 2)  # drive random value from 0 to 3 to clk and SDO
        caravelEnv.drive_gpio_in(4, clk)
        caravelEnv.drive_gpio_in(2, sdo)
        await FallingEdge(caravelEnv.clk)
        expected = int(f"0b{sdo}{clk}0", 2)
        if caravelEnv.monitor_gpio((10, 8)).integer != expected:
            cocotb.log.error(
                f"[TEST] checker 1 error the value seen at user pass through didn't match the value passed to SPI returend = {bin(caravelEnv.monitor_gpio((10,8)).integer)} expected = {bin(expected)}"
            )

    # check sdo and clk are not following the spi when enable but command 0xc2 isn't passed
    await caravelEnv.disable_csb()
    await caravelEnv.enable_csb()
    await caravelEnv.hk_write_byte(0x00)
    for i in range(randrange(10, 50)):
        clk = randrange(0, 2)  # drive random value from 0 to 3 to clk and SDO
        sdo = randrange(0, 2)  # drive random value from 0 to 3 to clk and SDO
        await RisingEdge(caravelEnv.clk)
        caravelEnv.drive_gpio_in(4, clk)
        caravelEnv.drive_gpio_in(2, sdo)
        await FallingEdge(caravelEnv.clk)
        await FallingEdge(caravelEnv.clk)
        expected = int("0b0", 2)
        if caravelEnv.monitor_gpio((10, 8)).integer != expected:
            cocotb.log.error(
                f"[TEST] checker 2 error the value seen at user pass through didn't match the value passed to SPI returend = {bin(caravelEnv.monitor_gpio((10,8)).integer)} expected = {bin(expected)}"
            )

    # check SDI
    await caravelEnv.disable_csb()
    await caravelEnv.enable_csb()
    await caravelEnv.hk_write_byte(
        0x02
    )  # Apply user pass-thru command to housekeeping SPI
    caravelEnv.drive_gpio_in(4, 0)  # finish the clock cycle
    await FallingEdge(caravelEnv.clk)
    caravelEnv.drive_gpio_in(4, 1)  # finish the clock cycle
    for i in range(randrange(10, 50)):
        sdi = randrange(0, 2)  # drive random value from 0 to 3 to clk and SDO
        caravelEnv.drive_gpio_in(11, sdi)
        await FallingEdge(caravelEnv.clk)
        expected = sdi
        if caravelEnv.monitor_gpio((1, 1)).integer != expected:
            cocotb.log.error(
                f"[TEST] checker 3 error the value seen at user pass through didn't match the value passed to SPI returend = {bin(caravelEnv.monitor_gpio((1,1)).integer)} expected = {bin(expected)}"
            )
