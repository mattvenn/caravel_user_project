import random
import cocotb
from cocotb.triggers import ClockCycles
import cocotb.log
from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
from caravel_cocotb.caravel_interfaces import SPI
from user_design import configure_userdesign



@cocotb.test()
@report_test
async def spi_rd_wr_nbyte(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=112763)
    spi_master = SPI(caravelEnv)
    debug_regs = await configure_userdesign(caravelEnv)
    cocotb.log.info("[TEST] start spi_rd_wr_nbyte test")
    nbytes_limits = 7
    #  writing to the random number(1 to 8) of bits after 0x1E (gpio_configure[4]) address  avoid changing gpio 3
    for j in range(30):
        address = random.randint(0x26, 0x67 - nbytes_limits)
        n_bytes = random.randint(1, nbytes_limits)
        await spi_master.write_reg_spi_nbytes(address, [0x3, 0x3, 0x3, 0x3, 0x3, 0x3, 0x3, 0x3], nbytes_limits)
        await spi_master.write_reg_spi_nbytes(address, [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0], n_bytes)
        data_8_bytes = await spi_master.read_reg_spi_nbytes(address, nbytes_limits)
        data = await spi_master.read_reg_spi_nbytes(address, n_bytes)
        cocotb.log.info(f"[TEST] n_bytes = {n_bytes} address = {address} data_8_bytes = {data_8_bytes}")
        for i in range(nbytes_limits):
            if i >= n_bytes:
                if data_8_bytes[i] != 0x3:
                    cocotb.log.error(
                        f"[TEST] register {i} has returned value {data_8_bytes[i]} while it should return value 0x3 n_bytes = {n_bytes}"
                    )
                else:
                    cocotb.log.info(
                        f"[TEST] successful read 0 from register {i} n_bytes = {n_bytes}"
                    )
            else:
                if data_8_bytes[i] != data[i]:
                    cocotb.log.error(f"[TEST] register {i} has returned value {data_8_bytes[i]} in 8 bytes reading while it should return value {data[i]} in {n_bytes} reading")
                if data_8_bytes[i] != 0:
                    cocotb.log.error(
                        f"[TEST] register number {i} has returned value {data_8_bytes[i]} > 0 while it should return value == 0 n_bytes = {n_bytes}"
                    )
                else:
                    cocotb.log.info(
                        f"[TEST] successful read {data_8_bytes[i]} from register {i} n_bytes = {n_bytes}"
                    )
    await ClockCycles(caravelEnv.clk, 5)


@cocotb.test()
@report_test
async def spi_rd_wr(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=11571)
    spi_master = SPI(caravelEnv)
    debug_regs = await configure_userdesign(caravelEnv)
    cocotb.log.info("[TEST] start spi_rd_wr test")
    #  writing to the random number(1 to 8) of bits after 0x1E (gpio_configure[4]) address  avoid changing gpio 3
    for j in range(7):
        address = random.randrange(0x26, 0x68, 2)
        data_in = random.getrandbits(8)
        data = await spi_master.read_write_reg_spi(address, data_in)
        cocotb.log.info(f"{j}: address {hex(address)} reading {hex(data)} and writing {hex(data_in)}")
        data = await spi_master.read_write_reg_spi(address, data_in)
        cocotb.log.info(f"{j}: address {hex(address)} reading {hex(data)} and writing {hex(data_in)}")
        if data != data_in:
            cocotb.log.error(
                f"[TEST] error address {hex(address)} data_out = {hex(data)}({bin(data)}) expected = {hex(data_in)}({bin(data_in)})"
            )
    nbytes_limits = 7
    for j in range(30):
        address = random.randint(0x26, 0x67 - nbytes_limits)
        n_bytes = random.randint(1, nbytes_limits)
        data_in = [random.getrandbits(4) for i in range(n_bytes)]
        data = await spi_master.read_write_reg_nbytes(address, data_in, n_bytes)
        cocotb.log.info(f"{j}: address {hex(address)} reading {data} and writing {data_in}")
        data = await spi_master.read_write_reg_nbytes(address, data_in, n_bytes)
        cocotb.log.info(f"{j}: address {hex(address)} reading {data} and writing {data_in}")
        if data != data_in:
            cocotb.log.error(
                f"[TEST] error address {hex(address)} data_out = {(data)} expected = {data_in}"
            )
    await ClockCycles(caravelEnv.clk, 5)
