import cocotb
from cocotb.triggers import ClockCycles
import cocotb.log
from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test


@cocotb.test()
@report_test
async def user_ram(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=1167331)
    cocotb.log.info("[TEST] Start user RAM word access stress test")
    pass_list = [0x1B]
    fail_list = [0x1E]
    reg1 = 0  # buffer
    await wait_configure(caravelEnv)
    while True:
        if caravelEnv.monitor_gpio((31, 0)).integer == 0xFF:  # test finish
            break
        if reg1 != caravelEnv.monitor_gpio((31, 0)).integer:
            reg1 = caravelEnv.monitor_gpio((31, 0)).integer
            if reg1 in pass_list:  # pass phase
                cocotb.log.info("[TEST] pass writing and reading all dff2 memory ")
                break
            elif reg1 in fail_list:  # pass phase
                cocotb.log.error("[TEST] failed access address")
                break
        await ClockCycles(caravelEnv.clk, 1000)


async def wait_configure(caravelEnv):
    serial_load = caravelEnv.caravel_hdl.housekeeping.serial_load
    while True:
        if serial_load.value:
            cocotb.log.info(f"serial load is asserted serial_load = {serial_load}")
            break
        await ClockCycles(caravelEnv.clk, 1)
    await ClockCycles(caravelEnv.clk, 10)
    await caravelEnv.release_csb()
    await ClockCycles(caravelEnv.clk, 10)
