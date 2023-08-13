import cocotb
from cocotb.triggers import ClockCycles
import cocotb.log
from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
from user_design import configure_userdesign


@cocotb.test()
@report_test
async def mem_dff2_W(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=3478259)
    debug_regs = await configure_userdesign(caravelEnv)
    cocotb.log.info("[TEST] Start mem dff2 word access stress test")
    pass_list = [0x1B]
    fail_list = [0x1E]
    reg1 = 0  # buffer
    while True:
        if debug_regs.read_debug_reg1() == 0xFF:  # test finish
            break
        if reg1 != debug_regs.read_debug_reg1():
            reg1 = debug_regs.read_debug_reg1()
            if reg1 in pass_list:  # pass phase
                cocotb.log.info("[TEST] pass writing and reading all dff2 memory ")
                break
            elif reg1 in fail_list:  # pass phase
                cocotb.log.error(
                    f"[TEST] failed access address {hex(debug_regs.read_debug_reg2())}"
                )
                break
        await ClockCycles(caravelEnv.clk, 1000)


@cocotb.test()
@report_test
async def mem_dff2_HW(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=3931459)
    debug_regs = await configure_userdesign(caravelEnv)
    cocotb.log.info("[TEST] Start mem dff2 half word access stress test")
    pass_list = [0x1B]
    fail_list = [0x1E]
    reg1 = 0  # buffer
    while True:
        if debug_regs.read_debug_reg1() == 0xFF:  # test finish
            break
        if reg1 != debug_regs.read_debug_reg1():
            reg1 = debug_regs.read_debug_reg1()
            if reg1 in pass_list:  # pass phase
                cocotb.log.info("[TEST] pass writing and reading all dff2 memory ")
                break
            elif reg1 in fail_list:  # pass phase
                cocotb.log.error(
                    f"[TEST] failed access address {hex(debug_regs.read_debug_reg2())}"
                )
                break
        await ClockCycles(caravelEnv.clk, 1000)


@cocotb.test()
@report_test
async def mem_dff2_B(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=5333959)
    debug_regs = await configure_userdesign(caravelEnv)
    cocotb.log.info("[TEST] Start mem dff2 Byte access stress test")
    pass_list = [0x1B]
    fail_list = [0x1E]
    reg1 = 0  # buffer
    while True:
        if debug_regs.read_debug_reg1() == 0xFF:  # test finish
            break
        if reg1 != debug_regs.read_debug_reg1():
            reg1 = debug_regs.read_debug_reg1()
            if reg1 in pass_list:  # pass phase
                cocotb.log.info("[TEST] pass writing and reading all dff2 memory ")
                break
            elif reg1 in fail_list:  # pass phase
                cocotb.log.error(
                    f"[TEST] failed access address {hex(debug_regs.read_debug_reg2())}"
                )
                break
        await ClockCycles(caravelEnv.clk, 1000)


@cocotb.test()
@report_test
async def mem_dff_W(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=7219359)
    debug_regs = await configure_userdesign(caravelEnv)
    cocotb.log.info("[TEST] Start mem dff word access stress test")
    pass_list = [0x1B]
    fail_list = [0x1E]
    reg1 = 0  # buffer
    while True:
        if reg1 != debug_regs.read_debug_reg1():
            reg1 = debug_regs.read_debug_reg1()
            if reg1 in pass_list:  # pass phase
                cocotb.log.info("[TEST] pass writing and reading all dff memory ")
                break
            elif reg1 in fail_list:  # pass phase
                cocotb.log.error(
                    f"[TEST] failed access address {hex(debug_regs.read_debug_reg2())}"
                )
                break
        await ClockCycles(caravelEnv.clk, 1000)


@cocotb.test()
@report_test
async def mem_dff_HW(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=7817759)
    debug_regs = await configure_userdesign(caravelEnv)
    cocotb.log.info("[TEST] Start mem dff half word access stress test")
    pass_list = [0x1B]
    fail_list = [0x1E]
    reg1 = 0  # buffer
    while True:
        if reg1 != debug_regs.read_debug_reg1():
            reg1 = debug_regs.read_debug_reg1()
            if reg1 in pass_list:  # pass phase
                cocotb.log.info("[TEST] pass writing and reading all dff memory ")
                break
            elif reg1 in fail_list:  # pass phase
                cocotb.log.error(
                    f"[TEST] failed access address {hex(debug_regs.read_debug_reg2())}"
                )
                break
        await ClockCycles(caravelEnv.clk, 1000)


@cocotb.test()
@report_test
async def mem_dff_B(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=10640359)
    debug_regs = await configure_userdesign(caravelEnv)
    cocotb.log.info("[TEST] Start mem dff Byte access stress test")
    pass_list = [0x1B]
    fail_list = [0x1E]
    reg1 = 0  # buffer
    while True:
        if reg1 != debug_regs.read_debug_reg1():
            reg1 = debug_regs.read_debug_reg1()
            if reg1 in pass_list:  # pass phase
                cocotb.log.info("[TEST] pass writing and reading all dff memory ")
                break
            elif reg1 in fail_list:  # pass phase
                cocotb.log.error(
                    f"[TEST] failed access address {hex(debug_regs.read_debug_reg2())}"
                )
                break
        await ClockCycles(caravelEnv.clk, 1000)


@cocotb.test()
@report_test
async def mem_sram_W(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=118083081)
    debug_regs = await configure_userdesign(caravelEnv)
    cocotb.log.info("[TEST] Start sram word access stress test")
    pass_list = [0x1B]
    fail_list = [0x1E]
    reg1 = 0  # buffer
    reg2 = 0
    while True:
        if reg1 != debug_regs.read_debug_reg1():
            reg1 = debug_regs.read_debug_reg1()
            if reg1 in pass_list:  # pass phase
                cocotb.log.info("[TEST] pass writing and reading all sram memory")
                break
            elif reg1 in fail_list:  # pass phase
                cocotb.log.error(
                    f"[TEST] failed access address {hex(debug_regs.read_debug_reg2())}"
                )
                break
        if reg2 != debug_regs.read_debug_reg2():
            reg2 = debug_regs.read_debug_reg2()
            cocotb.log.info(f"[TEST] iterator = {hex(reg2)} ")
        await ClockCycles(caravelEnv.clk, 1000)


@cocotb.test()
@report_test
async def mem_sram_HW(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=1116274181)
    debug_regs = await configure_userdesign(caravelEnv)
    cocotb.log.info("[TEST] Start sram halfword access stress test")
    pass_list = [0x1B]
    fail_list = [0x1E]
    reg1 = 0  # buffer
    while True:
        if reg1 != debug_regs.read_debug_reg1():
            reg1 = debug_regs.read_debug_reg1()
            if reg1 in pass_list:  # pass phase
                cocotb.log.info("[TEST] pass writing and reading all srram memory")
                break
            elif reg1 in fail_list:  # pass phase
                cocotb.log.error(
                    f"[TEST] failed access address {hex(debug_regs.read_debug_reg2())}"
                )
                break
        # if reg2 != debug_regs.read_debug_reg2():
        #     reg2 = debug_regs.read_debug_reg2()
        #     cocotb.log.info(f"[TEST] iterator = {hex(reg2)} ")
        await ClockCycles(caravelEnv.clk, 1000)


@cocotb.test()
@report_test
async def mem_sram_B(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=1128500231)
    debug_regs = await configure_userdesign(caravelEnv)
    cocotb.log.info("[TEST] Start sram byte access stress test")
    pass_list = [0x1B]
    fail_list = [0x1E]
    reg1 = 0  # buffer
    while True:
        if reg1 != debug_regs.read_debug_reg1():
            reg1 = debug_regs.read_debug_reg1()
            if reg1 in pass_list:  # pass phase
                cocotb.log.info("[TEST] pass writing and reading all sram memory ")
                break
            elif reg1 in fail_list:  # pass phase
                cocotb.log.error(
                    "[TEST] failed access address {hex(debug_regs.read_debug_reg2())}"
                )
                break
        # if reg2 != debug_regs.read_debug_reg2():
        #     reg2 = debug_regs.read_debug_reg2()
        #     cocotb.log.info(f"[TEST] iterator = {hex(reg2)} ")
        await ClockCycles(caravelEnv.clk, 1000)


@cocotb.test()
@report_test
async def mem_sram_smoke(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=11655541)
    debug_regs = await configure_userdesign(caravelEnv)
    cocotb.log.info("[TEST] Start sram smoke test")
    pass_list = [0x1B]
    fail_list = [0x1E]
    reg1 = 0  # buffer
    while True:
        if reg1 != debug_regs.read_debug_reg1():
            reg1 = debug_regs.read_debug_reg1()
            if reg1 in pass_list:  # pass phase
                cocotb.log.info("[TEST] pass writing and reading all sram memory ")
                break
            elif reg1 in fail_list:  # pass phase
                cocotb.log.error(
                    f"[TEST] failed access address {hex(debug_regs.read_debug_reg2())}"
                )
                break
        # if reg2 != debug_regs.read_debug_reg2():
        #     reg2 = debug_regs.read_debug_reg2()
        #     cocotb.log.info(f"[TEST] iterator = {hex(reg2)} ")
        await ClockCycles(caravelEnv.clk, 1000)
