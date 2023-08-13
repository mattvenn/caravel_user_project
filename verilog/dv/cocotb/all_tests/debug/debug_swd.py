import random
import cocotb
from cocotb.triggers import FallingEdge, RisingEdge, ClockCycles, Timer
import cocotb.log
from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
from collections import namedtuple
from cocotb.handle import Force
from cocotb.clock import Clock
from user_design import configure_userdesign


bit_time_ns = 0

Operation = namedtuple(
    "Operation", ["start", "APnDP", "RnW", "A2", "A3", "parity", "stop", "park"]
)
ACK = {int("100", 2): "OK", int("010", 2): "WAIT", int("001", 2): "FAULT"}


@cocotb.test()
@report_test
async def debug_swd(dut):
    dut._id(f"gpio{35}", False).value = 0
    dut._id(f"gpio{35}_en", False).value = Force(1)
    caravelEnv = await test_configure(dut, timeout_cycles=1131011)
    debug_regs = await configure_userdesign(caravelEnv)
    caravelEnv.drive_gpio_in(0, 1)
    caravelEnv.drive_gpio_in(35, 0)

    await debug_regs.wait_reg1(0xAA)
    swd = SWD_vip(caravelEnv, 100)
    op = Operation(1, 0, 1, 0, 0, 1, 0, 1)  # read ID
    await swd.reset_swd()
    await swd.write_op(op)
    await swd.turnaround()
    ack = await swd.read_ack()
    if ack == "OK":
        response = await swd.read_response()
        if response != 0xBB11477:
            cocotb.log.error("returned wrong ID ")
        else:
            cocotb.log.info("returned right ID ")
    else:
        cocotb.log.error("returned unexpected ack value")


class SWD_vip:
    def __init__(self, caravelEnv, period):
        self.caravelEnv = caravelEnv
        self.setup_clock(period)

    def setup_clock(self, period):
        self.drive_dio(1)
        self.clk = self.caravelEnv.dut._id("gpio35", False)
        self.caravelEnv.dut._id("gpio35_en", False).value = 1
        clock = Clock(self.clk, period, units="ns")
        cocotb.start_soon(clock.start())  # Start the clock
        cocotb.log.info(f"[SWD_vip] setup clock for swd with period {period}")
        return clock

    def drive_dio(self, data):
        cocotb.log.info(f"[SWD_vip] drive dio with {data}")
        self.caravelEnv.drive_gpio_in(0, data)

    def release_dio(self):
        cocotb.log.info("[SWD_vip] release dio")
        self.caravelEnv.release_gpio(0)

    def monitor_dio(self):
        val = self.caravelEnv.monitor_gpio((0, 0))
        cocotb.log.info(f"[SWD_vip] Monitor dio val = {val}")
        return f"{val}"

    # for reset do has to be asserted for at least 50 cycles
    async def reset_swd(self):
        cocotb.log.info("[SWD_vip] reset swd")
        self.drive_dio(1)
        await ClockCycles(self.clk, random.randint(50, 100))
        self.drive_dio(0)
        await ClockCycles(self.clk, 2)
        # self.release_dio()

    # turn around is a number of idele clock cycles between changing the do io for input to output or vice versa
    # depends on the design but here it's only 1
    async def turnaround(self):
        cocotb.log.info("[SWD_vip] turnaround swd")
        await Timer(8, "ns")
        self.release_dio()
        await ClockCycles(self.clk, 1)

    async def write_op(self, op):
        cocotb.log.info(f"[SWD_vip] write op : {op}")
        for i in range(8):
            await FallingEdge(self.clk)
            self.drive_dio(op[i])
        await RisingEdge(self.clk)

    async def read_ack(self):
        cocotb.log.info("[SWD_vip] start reading ACK ")
        ack = ""
        for i in range(3):
            await RisingEdge(self.clk)
            ack += self.monitor_dio()
        cocotb.log.info("[SWD_vip] returned ack = {ack} = {ACK[int(ack,2)]} ")
        return ACK[int(ack, 2)]

    async def read_response(self):
        cocotb.log.info("[SWD_vip] start reading response ")
        data = ""
        for i in range(32):
            await RisingEdge(self.clk)
            data += self.monitor_dio()
        data = int(data[::-1], 2)
        cocotb.log.info(f"[SWD_vip] returned response = {data}({hex(data)})")
        return data
