import cocotb
from cocotb.triggers import FallingEdge, RisingEdge
import cocotb.log
from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
from all_tests.spi_master.SPI_VIP import read_mem, SPI_VIP
from caravel_cocotb.caravel_interfaces import SPI
from random import randrange
from user_design import configure_userdesign


bit_time_ns = 0


@cocotb.test()
@report_test
async def user_pass_thru_rd(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=89712)
    spi_master = SPI(caravelEnv)
    debug_regs = await configure_userdesign(caravelEnv)
    cocotb.log.info("[TEST] start spi_master_rd test")
    file_name = f"{cocotb.plusargs['USER_PROJECT_ROOT']}/verilog/dv/cocotb/all_tests/housekeeping/housekeeping_spi/test_data"
    file_name = file_name.replace('"', '')
    mem = read_mem(file_name)
    await cocotb.start(
        SPI_VIP(
            dut.gpio8_monitor,
            dut.gpio9_monitor,
            dut.gpio10_monitor,
            (dut.gpio11_en, dut.gpio11),
            mem, remove_clk=1
        )
    )  # fork for SPI
    await debug_regs.wait_reg1(0xAA)
    cocotb.log.info("[TEST] Configuration finished")
    # start reading from memory
    address = 0x00.to_bytes(3, "big")

    data_received = await spi_master.reg_spi_user_pass_thru(send_data=[0x03, address[0], address[1], address[2]], read_byte_num=8)
    address = int.from_bytes(address, "big")
    for data in data_received:
        if data != mem[address]:
            cocotb.log.error(
                f"[TEST] reading incorrect value from address {hex(address)} expected = {hex(mem[address])} returened = {hex(data)}"
            )
        else:
            cocotb.log.info(
                f"[TEST] reading correct value {hex(data)} from address {hex(address)} "
            )
        address += 1
    await spi_master.disable_csb()

    # Wait for processor to restart
    await debug_regs.wait_reg1(0xBB)
    cocotb.log.info("[TEST] processor has restarted successfully")


@cocotb.test()
@report_test
async def user_pass_thru_connection(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=86033)
    spi_master = SPI(caravelEnv)
    debug_regs = await configure_userdesign(caravelEnv)
    await debug_regs.wait_reg1(0xAA)
    await spi_master.enable_csb()
    await spi_master._hk_write_byte(spi_master.SPI_COMMAND.USER_PASS_THRU.value)  
    await FallingEdge(spi_master.clk)
    spi_master._kill_spi_clk()
    caravelEnv.drive_gpio_in(4, 0)  # finish the clock cycle
    await RisingEdge(caravelEnv.clk)
    # check sdo and clk are following the spi
    for i in range(randrange(10, 50)):
        clk = randrange(0, 2)  # drive random value from 0 to 3 to clk and SDO
        sdo = randrange(0, 2)  # drive random value from 0 to 3 to clk and SDO
        caravelEnv.drive_gpio_in(4, clk)
        caravelEnv.drive_gpio_in(2, sdo)
        await RisingEdge(caravelEnv.clk)
        expected = int(f"0b{sdo}{clk}0", 2)
        if caravelEnv.monitor_gpio((10, 8)).integer != expected:
            cocotb.log.error(
                f"[TEST] checker 1 error the value seen at user pass through didn't match the value passed to SPI returend = {bin(caravelEnv.monitor_gpio((10,8)).integer)} expected = {bin(expected)}"
            )

    # check sdo and clk are not following the spi when enable but command 0xc2 isn't passed
    await spi_master.disable_csb()
    await spi_master.enable_csb()
    await spi_master._hk_write_byte(spi_master.SPI_COMMAND.NO_OP.value)
    spi_master._kill_spi_clk()
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
    await spi_master.disable_csb()
    await spi_master.enable_csb()
    await spi_master._hk_write_byte(spi_master.SPI_COMMAND.USER_PASS_THRU.value)
    await FallingEdge(spi_master.clk)
    spi_master._kill_spi_clk()
    caravelEnv.drive_gpio_in(4, 0)  # finish the clock cycle
    await RisingEdge(caravelEnv.clk)
    caravelEnv.drive_gpio_in(4, 1)  # finish the clock cycle
    for i in range(randrange(10, 50)):
        sdi = randrange(0, 2)  # drive random value from 0 to 3 to clk and SDO
        caravelEnv.drive_gpio_in(11, sdi)
        await RisingEdge(caravelEnv.clk)
        expected = sdi
        if caravelEnv.monitor_gpio((1, 1)).integer != expected:
            cocotb.log.error(
                f"[TEST] checker 3 error the value seen at user pass through didn't match the value passed to SPI returend = {bin(caravelEnv.monitor_gpio((1,1)).integer)} expected = {bin(expected)}"
            )
