import random
import cocotb
from cocotb.triggers import ClockCycles
import cocotb.log
from cocotb_includes import test_configure
from cocotb_includes import repot_test
from tests.housekeeping.housekeeping_spi.spi_access_functions import write_reg_spi_nbytes
from tests.housekeeping.housekeeping_spi.spi_access_functions import read_reg_spi_nbytes
from tests.housekeeping.housekeeping_spi.spi_access_functions import read_write_reg_spi


@cocotb.test()
@repot_test
async def spi_rd_wr_nbyte(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=2646)
    cocotb.log.info("[TEST] start spi_rd_wr_nbyte test")
    nbytes_limits = 8
    #  writing to the random number(1 to 8) of bits after 0x1E (gpio_configure[4]) address  avoid changing gpio 3
    for j in range(3):
        address = random.randint(0x26, 0x67 - nbytes_limits)
        n_bytes = random.randint(1, nbytes_limits)
        await write_reg_spi_nbytes(
            caravelEnv, address, [0x3, 0x3, 0x3, 0x3, 0x3, 0x3, 0x3, 0x3], nbytes_limits
        )
        await write_reg_spi_nbytes(
            caravelEnv, address, [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0], n_bytes
        )
        data = await read_reg_spi_nbytes(caravelEnv, address, nbytes_limits)
        for i in range(nbytes_limits):
            if i >= n_bytes:
                if data[i] != 0x3:
                    cocotb.log.error(
                        f"[TEST] register {i} has returned value {data[i]} while it should return value 0x3 n_bytes = {n_bytes}"
                    )
                else:
                    cocotb.log.info(
                        f"[TEST] successful read 0 from register {i} n_bytes = {n_bytes}"
                    )
            else:
                if data[i] != 0:
                    cocotb.log.error(
                        f"[TEST] register number {i} has returned value {data[i]} > 0 while it should return value == 0 n_bytes = {n_bytes}"
                    )
                else:
                    cocotb.log.info(
                        f"[TEST] successful read {data[i]} from register {i} n_bytes = {n_bytes}"
                    )
    await ClockCycles(caravelEnv.clk, 200)


@cocotb.test()
@repot_test
async def spi_rd_wr_stream(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=1111370)
    cocotb.log.info("[TEST] start spi_rd_wr_stream test")
    #  writing to the random number(1 to 8) of bits after 0x1E (gpio_configure[4]) address  avoid changing gpio 3
    for j in range(7):
        address = random.randrange(0x26, 0x68, 2)
        data_in = random.getrandbits(8)
        data = await read_write_reg_spi(caravelEnv, address, data_in)
        cocotb.log.info(
            f"{j}: address {hex(address)} reading {hex(data)} and writing {hex(data_in)}"
        )
        data = await read_write_reg_spi(caravelEnv, address, data_in)
        cocotb.log.info(
            f"{j}: address {hex(address)} reading {hex(data)} and writing {hex(data_in)}"
        )
        if data != data_in:
            cocotb.log.error(
                f"[TEST] error address {address} data_out = {data} expected = {data_in}"
            )
    await ClockCycles(caravelEnv.clk, 200)
