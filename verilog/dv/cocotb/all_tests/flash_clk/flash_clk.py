import cocotb
from cocotb.triggers import Edge, RisingEdge, FallingEdge, ClockCycles
from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
@cocotb.test()
@report_test
async def flash_clk(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=1999191)
    clock = caravelEnv.get_clock_period()
    csb = dut.flash_csb_tb
    clk = dut.flash_clk_tb
    await FallingEdge(csb)
    await ClockCycles(clk,10)
    cocotb.log.info("after 10 clocks")
    start_time = cocotb.utils.get_sim_time("ns")
    await ClockCycles(clk,10)
    end_time = cocotb.utils.get_sim_time("ns")
    period = (end_time - start_time) / 10
    if abs(period - clock *4 ) < 0.05:
        cocotb.log.info(f"period = {period}ns start_time at {start_time}ns end_time at {end_time}ns")
    else:
        cocotb.log.error(f"period = {period}ns suppose to be 100ns start_time at {start_time}ns end_time at {end_time}ns")
