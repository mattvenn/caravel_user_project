import cocotb
from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
from cocotb.triggers import ClockCycles


@cocotb.test()
@report_test
async def helloWorld(dut):
    caravelEnv = await test_configure(dut)
    cocotb.log.info("[Test] Hello world")
    await ClockCycles(caravelEnv.clk, 100000)
