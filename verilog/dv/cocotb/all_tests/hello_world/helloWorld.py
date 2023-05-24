import cocotb
from cocotb_includes import test_configure
from cocotb_includes import report_test
from cocotb.triggers import ClockCycles


@cocotb.test()
@report_test
async def helloWorld(dut):
    caravelEnv = await test_configure(dut)
    cocotb.log.info("[Test] Hello world")
    await ClockCycles(caravelEnv.clk, 100000)
