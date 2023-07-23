import cocotb
from cocotb.triggers import ClockCycles
import cocotb.log
from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
from caravel_cocotb.caravel_interfaces import SPI
from user_design import configure_userdesign


@cocotb.test()
@report_test
async def cpu_reset(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=121372)
    spi_master = SPI(caravelEnv)
    debug_regs = await configure_userdesign(caravelEnv)
    cocotb.log.info("[TEST] Start cpu_reset test")
    # wait for CPU to write 5 at debug_reg1
    while True:
        if debug_regs.read_debug_reg1() == 5:
            cocotb.log.info("[TEST] debug reg 1 = 5")
            break
        await ClockCycles(caravelEnv.clk, 1)

    # put the cpu under reset using spi
    cocotb.log.info("[TEST] asserting cpu reset register using SPI")
    await spi_master.write_reg_spi(0xB, 1)

    await ClockCycles(caravelEnv.clk, 1000)
    if debug_regs.read_debug_reg1() == 0:
        cocotb.log.info(
            "[TEST] asserting cpu reset register using SPI successfully rest the cpu"
        )
    else:
        cocotb.log.error(
            "[TEST] asserting  cpu reset register using SPI successfully doesn't rest the cpu"
        )

    cocotb.log.info("[TEST] deasserting cpu reset register using SPI")
    await spi_master.write_reg_spi(0xB, 0)
    watchdog = 50000
    while True:
        if debug_regs.read_debug_reg1() == 5:
            cocotb.log.info(
                "[TEST] deasserting cpu reset register using SPI  wakes the cpu up"
            )
            break
        watchdog -= 1
        if watchdog < 0:
            cocotb.log.error(
                "[TEST] deasserting cpu reset register using SPI doesn't wake the cpu up"
            )
            break

        await ClockCycles(caravelEnv.clk, 1)

    cocotb.log.info("[TEST] asserting cpu reset register using firmware")
    debug_regs.write_debug_reg2_backdoor(0xAA)
    await ClockCycles(caravelEnv.clk, 10000)

    watchdog = 8000
    while True:
        if debug_regs.read_debug_reg1() == 0:
            cocotb.log.info(
                "[TEST] asserting cpu reset register using firmware successfully rest the cpu"
            )
            break
        watchdog -= 1
        if watchdog < 0:
            cocotb.log.error(
                "[TEST] asserting  cpu reset register using firmware successfully doesn't rest the cpu"
            )
            break

    await ClockCycles(caravelEnv.clk, 100)
