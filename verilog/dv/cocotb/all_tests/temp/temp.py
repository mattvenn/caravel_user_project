import cocotb
from cocotb.triggers import RisingEdge, ClockCycles
import cocotb.log
from cocotb_includes import test_configure
from cocotb_includes import repot_test


@cocotb.test()
@repot_test
async def temp(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=1137599)
    cocotb.log.info("[TEST] start  temp")
    caravelEnv.release_csb()
    await caravelEnv.wait_mgmt_gpio(1)  # wait for gpio configuration to happened
    cocotb.log.info("[TEST] finish configuration")
    caravelEnv.drive_gpio_in(2,0)
    await caravelEnv.wait_mgmt_gpio(0)  # wait for gpio configuration to happened
    await caravelEnv.wait_mgmt_gpio(1)  # wait for gpio configuration to happened
    caravelEnv.release_gpio(2)
    await caravelEnv.wait_mgmt_gpio(0)  # wait for gpio configuration to happened
    await caravelEnv.wait_mgmt_gpio(1)  # wait for gpio configuration to happened
    caravelEnv.drive_gpio_in(2,1)
    await ClockCycles(caravelEnv.clk,1000)
    await caravelEnv.wait_mgmt_gpio(0)  # wait for gpio configuration to happened
    await caravelEnv.wait_mgmt_gpio(1)  # wait for gpio configuration to happened
    caravelEnv.drive_gpio_in(2,0)
    await ClockCycles(caravelEnv.clk,100000)
