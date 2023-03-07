import cocotb
import cocotb.log
from cocotb_includes import test_configure
from cocotb_includes import repot_test
from cocotb_includes import Macros
from cocotb_includes import sky
from tests.common.debug_regs import DebugRegs

bit_size = 13
if not sky:
    bit_size = 10


def shift(gpio, shift_type):
    if shift_type:
        bits = "0101010101010"
        if not sky:
            bits = "1010101010"
    else:
        bits = "1010101010101"
        if not sky:
            bits = "0101010101"
    fail = False
    gpio_to_skip = ()

    if Macros["ARM"]:
        gpio_to_skip = (
            "gpio_control_bidir_2[0]",
            "gpio_control_bidir_2[1]",
            "gpio_control_bidir_2[2]",
        )

    if str(gpio).split(".")[-1] in gpio_to_skip:
        return

    if not Macros["GL"]:
        cocotb.log.info(
            f"[TEST] gpio {gpio} shift {gpio._id(f'shift_register',False).value} expected {bits}"
        )
    for i in range(bit_size):
        if not Macros["GL"]:
            shift_register = gpio._id("shift_register", False).value.binstr[i]
        else:
            shift_register = (
                gpio[0]
                ._id(f"\\{gpio[1]}.shift_register[{bit_size-1-i}] ", False)
                .value.binstr
            )
        if shift_register != bits[i]:
            fail = True
            cocotb.log.error(f"[TEST] wrong shift register {i} in {gpio}")
    if not fail:
        if not Macros["GL"]:
            cocotb.log.info(f"[TEST] gpio {gpio} passed")
        else:
            cocotb.log.info(f"[TEST] gpio {gpio[1]} passed")


@cocotb.test()
@repot_test
async def serial_shifting_10(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=500158)
    debug_regs = DebugRegs(caravelEnv)
    uut = dut.uut.chip_core
    debug_regs = DebugRegs(caravelEnv)
    await debug_regs.wait_reg1(0xFF)
    gpios_l = (
        "gpio_control_bidir_1[0]",
        "gpio_control_bidir_1[1]",
        "gpio_control_in_1a[0]",
        "gpio_control_in_1a[1]",
        "gpio_control_in_1a[2]",
        "gpio_control_in_1a[3]",
        "gpio_control_in_1a[4]",
        "gpio_control_in_1a[5]",
        "gpio_control_in_1[0]",
        "gpio_control_in_1[1]",
        "gpio_control_in_1[2]",
        "gpio_control_in_1[3]",
        "gpio_control_in_1[4]",
        "gpio_control_in_1[5]",
        "gpio_control_in_1[6]",
        "gpio_control_in_1[7]",
        "gpio_control_in_1[8]",
        "gpio_control_in_1[9]",
        "gpio_control_in_1[10]",
    )
    if Macros["CARAVAN"]:
        gpios_l = (
            "gpio_control_bidir_1[0]",
            "gpio_control_bidir_1[1]",
            "gpio_control_in_1a[0]",
            "gpio_control_in_1a[1]",
            "gpio_control_in_1a[2]",
            "gpio_control_in_1a[3]",
            "gpio_control_in_1a[4]",
            "gpio_control_in_1a[5]",
            "gpio_control_in_1[0]",
            "gpio_control_in_1[1]",
            "gpio_control_in_1[2]",
            "gpio_control_in_1[3]",
            "gpio_control_in_1[4]",
            "gpio_control_in_1[5]",
        )

    gpios_h = (
        "gpio_control_in_2[0]",
        "gpio_control_in_2[1]",
        "gpio_control_in_2[2]",
        "gpio_control_in_2[3]",
        "gpio_control_in_2[4]",
        "gpio_control_in_2[5]",
        "gpio_control_in_2[6]",
        "gpio_control_in_2[7]",
        "gpio_control_in_2[8]",
        "gpio_control_in_2[9]",
        "gpio_control_in_2[10]",
        "gpio_control_in_2[11]",
        "gpio_control_in_2[12]",
        "gpio_control_in_2[13]",
        "gpio_control_in_2[14]",
        "gpio_control_in_2[15]",
        "gpio_control_bidir_2[0]",
        "gpio_control_bidir_2[1]",
        "gpio_control_bidir_2[2]",
    )
    if Macros["CARAVAN"]:
        gpios_h = (
            "gpio_control_in_2[0]",
            "gpio_control_in_2[1]",
            "gpio_control_in_2[2]",
            "gpio_control_in_2[3]",
            "gpio_control_in_2[4]",
            "gpio_control_in_2[5]",
            "gpio_control_in_2[6]",
            "gpio_control_in_2[7]",
            "gpio_control_in_2[8]",
            "gpio_control_in_2[9]",
            "gpio_control_bidir_2[0]",
            "gpio_control_bidir_2[1]",
            "gpio_control_bidir_2[2]",
        )

    type = True  # type of shifting 01 or 10
    for gpio in gpios_l:
        if not Macros["GL"]:
            shift(uut._id(gpio, False), type)
        else:
            shift((uut, gpio), type)
        type = not type
    type = True  # type of shifting 01 or 10
    for gpio in reversed(gpios_h):
        if not Macros["GL"]:
            shift(uut._id(gpio, False), type)
        else:
            shift((uut, gpio), type)
        type = not type


@cocotb.test()
@repot_test
async def serial_shifting_01(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=499090)
    debug_regs = DebugRegs(caravelEnv)
    uut = dut.uut.chip_core
    debug_regs = DebugRegs(caravelEnv)
    await debug_regs.wait_reg1(0xFF)
    gpios_l = (
        "gpio_control_bidir_1[0]",
        "gpio_control_bidir_1[1]",
        "gpio_control_in_1a[0]",
        "gpio_control_in_1a[1]",
        "gpio_control_in_1a[2]",
        "gpio_control_in_1a[3]",
        "gpio_control_in_1a[4]",
        "gpio_control_in_1a[5]",
        "gpio_control_in_1[0]",
        "gpio_control_in_1[1]",
        "gpio_control_in_1[2]",
        "gpio_control_in_1[3]",
        "gpio_control_in_1[4]",
        "gpio_control_in_1[5]",
        "gpio_control_in_1[6]",
        "gpio_control_in_1[7]",
        "gpio_control_in_1[8]",
        "gpio_control_in_1[9]",
        "gpio_control_in_1[10]",
    )
    if Macros["CARAVAN"]:
        gpios_l = (
            "gpio_control_bidir_1[0]",
            "gpio_control_bidir_1[1]",
            "gpio_control_in_1a[0]",
            "gpio_control_in_1a[1]",
            "gpio_control_in_1a[2]",
            "gpio_control_in_1a[3]",
            "gpio_control_in_1a[4]",
            "gpio_control_in_1a[5]",
            "gpio_control_in_1[0]",
            "gpio_control_in_1[1]",
            "gpio_control_in_1[2]",
            "gpio_control_in_1[3]",
            "gpio_control_in_1[4]",
            "gpio_control_in_1[5]",
        )

    gpios_h = (
        "gpio_control_in_2[0]",
        "gpio_control_in_2[1]",
        "gpio_control_in_2[2]",
        "gpio_control_in_2[3]",
        "gpio_control_in_2[4]",
        "gpio_control_in_2[5]",
        "gpio_control_in_2[6]",
        "gpio_control_in_2[7]",
        "gpio_control_in_2[8]",
        "gpio_control_in_2[9]",
        "gpio_control_in_2[10]",
        "gpio_control_in_2[11]",
        "gpio_control_in_2[12]",
        "gpio_control_in_2[13]",
        "gpio_control_in_2[14]",
        "gpio_control_in_2[15]",
        "gpio_control_bidir_2[0]",
        "gpio_control_bidir_2[1]",
        "gpio_control_bidir_2[2]",
    )
    if Macros["CARAVAN"]:
        gpios_h = (
            "gpio_control_in_2[0]",
            "gpio_control_in_2[1]",
            "gpio_control_in_2[2]",
            "gpio_control_in_2[3]",
            "gpio_control_in_2[4]",
            "gpio_control_in_2[5]",
            "gpio_control_in_2[6]",
            "gpio_control_in_2[7]",
            "gpio_control_in_2[8]",
            "gpio_control_in_2[9]",
            "gpio_control_bidir_2[0]",
            "gpio_control_bidir_2[1]",
            "gpio_control_bidir_2[2]",
        )

    type = False  # type of shifting 01 or 10
    for gpio in gpios_l:
        if not Macros["GL"]:
            shift(uut._id(gpio, False), type)
        else:
            shift((uut, gpio), type)
        type = not type
    type = False  # type of shifting 01 or 10
    for gpio in reversed(gpios_h):
        if not Macros["GL"]:
            shift(uut._id(gpio, False), type)
        else:
            shift((uut, gpio), type)
        type = not type


@cocotb.test()
@repot_test
async def serial_shifting_0011(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=613444)
    debug_regs = DebugRegs(caravelEnv)
    uut = dut.uut.chip_core
    debug_regs = DebugRegs(caravelEnv)
    await debug_regs.wait_reg1(0xFF)
    gpios_l = (
        "gpio_control_bidir_1[0]",
        "gpio_control_bidir_1[1]",
        "gpio_control_in_1a[0]",
        "gpio_control_in_1a[1]",
        "gpio_control_in_1a[2]",
        "gpio_control_in_1a[3]",
        "gpio_control_in_1a[4]",
        "gpio_control_in_1a[5]",
        "gpio_control_in_1[0]",
        "gpio_control_in_1[1]",
        "gpio_control_in_1[2]",
        "gpio_control_in_1[3]",
        "gpio_control_in_1[4]",
        "gpio_control_in_1[5]",
        "gpio_control_in_1[6]",
        "gpio_control_in_1[7]",
        "gpio_control_in_1[8]",
        "gpio_control_in_1[9]",
        "gpio_control_in_1[10]",
    )
    if Macros["CARAVAN"]:
        gpios_l = (
            "gpio_control_bidir_1[0]",
            "gpio_control_bidir_1[1]",
            "gpio_control_in_1a[0]",
            "gpio_control_in_1a[1]",
            "gpio_control_in_1a[2]",
            "gpio_control_in_1a[3]",
            "gpio_control_in_1a[4]",
            "gpio_control_in_1a[5]",
            "gpio_control_in_1[0]",
            "gpio_control_in_1[1]",
            "gpio_control_in_1[2]",
            "gpio_control_in_1[3]",
            "gpio_control_in_1[4]",
            "gpio_control_in_1[5]",
        )

    gpios_h = (
        "gpio_control_in_2[0]",
        "gpio_control_in_2[1]",
        "gpio_control_in_2[2]",
        "gpio_control_in_2[3]",
        "gpio_control_in_2[4]",
        "gpio_control_in_2[5]",
        "gpio_control_in_2[6]",
        "gpio_control_in_2[7]",
        "gpio_control_in_2[8]",
        "gpio_control_in_2[9]",
        "gpio_control_in_2[10]",
        "gpio_control_in_2[11]",
        "gpio_control_in_2[12]",
        "gpio_control_in_2[13]",
        "gpio_control_in_2[14]",
        "gpio_control_in_2[15]",
        "gpio_control_bidir_2[0]",
        "gpio_control_bidir_2[1]",
        "gpio_control_bidir_2[2]",
    )
    if Macros["CARAVAN"]:
        gpios_h = (
            "gpio_control_in_2[0]",
            "gpio_control_in_2[1]",
            "gpio_control_in_2[2]",
            "gpio_control_in_2[3]",
            "gpio_control_in_2[4]",
            "gpio_control_in_2[5]",
            "gpio_control_in_2[6]",
            "gpio_control_in_2[7]",
            "gpio_control_in_2[8]",
            "gpio_control_in_2[9]",
            "gpio_control_bidir_2[0]",
            "gpio_control_bidir_2[1]",
            "gpio_control_bidir_2[2]",
        )

    type = 2  # type of shifting 01 or 10
    for gpio in gpios_l:
        if not Macros["GL"]:
            shift_2(uut._id(gpio, False), type)
        else:
            shift_2((uut, gpio), type)
        type = (type + 1) % 4
    type = 2  # type of shifting 01 or 10
    for gpio in reversed(gpios_h):
        if not Macros["GL"]:
            shift_2(uut._id(gpio, False), type)
        else:
            shift_2((uut, gpio), type)
        type = (type + 1) % 4


@cocotb.test()
@repot_test
async def serial_shifting_1100(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=603431)
    debug_regs = DebugRegs(caravelEnv)
    uut = dut.uut.chip_core
    debug_regs = DebugRegs(caravelEnv)
    await debug_regs.wait_reg1(0xFF)
    gpios_l = (
        "gpio_control_bidir_1[0]",
        "gpio_control_bidir_1[1]",
        "gpio_control_in_1a[0]",
        "gpio_control_in_1a[1]",
        "gpio_control_in_1a[2]",
        "gpio_control_in_1a[3]",
        "gpio_control_in_1a[4]",
        "gpio_control_in_1a[5]",
        "gpio_control_in_1[0]",
        "gpio_control_in_1[1]",
        "gpio_control_in_1[2]",
        "gpio_control_in_1[3]",
        "gpio_control_in_1[4]",
        "gpio_control_in_1[5]",
        "gpio_control_in_1[6]",
        "gpio_control_in_1[7]",
        "gpio_control_in_1[8]",
        "gpio_control_in_1[9]",
        "gpio_control_in_1[10]",
    )
    if Macros["CARAVAN"]:
        gpios_l = (
            "gpio_control_bidir_1[0]",
            "gpio_control_bidir_1[1]",
            "gpio_control_in_1a[0]",
            "gpio_control_in_1a[1]",
            "gpio_control_in_1a[2]",
            "gpio_control_in_1a[3]",
            "gpio_control_in_1a[4]",
            "gpio_control_in_1a[5]",
            "gpio_control_in_1[0]",
            "gpio_control_in_1[1]",
            "gpio_control_in_1[2]",
            "gpio_control_in_1[3]",
            "gpio_control_in_1[4]",
            "gpio_control_in_1[5]",
        )

    gpios_h = (
        "gpio_control_in_2[0]",
        "gpio_control_in_2[1]",
        "gpio_control_in_2[2]",
        "gpio_control_in_2[3]",
        "gpio_control_in_2[4]",
        "gpio_control_in_2[5]",
        "gpio_control_in_2[6]",
        "gpio_control_in_2[7]",
        "gpio_control_in_2[8]",
        "gpio_control_in_2[9]",
        "gpio_control_in_2[10]",
        "gpio_control_in_2[11]",
        "gpio_control_in_2[12]",
        "gpio_control_in_2[13]",
        "gpio_control_in_2[14]",
        "gpio_control_in_2[15]",
        "gpio_control_bidir_2[0]",
        "gpio_control_bidir_2[1]",
        "gpio_control_bidir_2[2]",
    )
    if Macros["CARAVAN"]:
        gpios_h = (
            "gpio_control_in_2[0]",
            "gpio_control_in_2[1]",
            "gpio_control_in_2[2]",
            "gpio_control_in_2[3]",
            "gpio_control_in_2[4]",
            "gpio_control_in_2[5]",
            "gpio_control_in_2[6]",
            "gpio_control_in_2[7]",
            "gpio_control_in_2[8]",
            "gpio_control_in_2[9]",
            "gpio_control_bidir_2[0]",
            "gpio_control_bidir_2[1]",
            "gpio_control_bidir_2[2]",
        )
    type = 0  # type of shifting 01 or 10
    for gpio in gpios_l:
        if not Macros["GL"]:
            shift_2(uut._id(gpio, False), type)
        else:
            shift_2((uut, gpio), type)
        type = (type + 1) % 4
    type = 0  # type of shifting 01 or 10
    for gpio in reversed(gpios_h):
        if not Macros["GL"]:
            shift_2(uut._id(gpio, False), type)
        else:
            shift_2((uut, gpio), type)
        type = (type + 1) % 4


def shift_2(gpio, shift_type):
    if shift_type == 0:
        bits = "0011001100110"
        if not sky:
            bits = "1001100110"
    elif shift_type == 1:
        bits = "0110011001100"
        if not sky:
            bits = "0011001100"
    elif shift_type == 2:
        bits = "1100110011001"
        if not sky:
            bits = "0110011001"
    elif shift_type == 3:
        bits = "1001100110011"
        if not sky:
            bits = "1100110011"
    gpio_to_skip = ()
    if Macros["ARM"]:
        gpio_to_skip = (
            "gpio_control_bidir_2[0]",
            "gpio_control_bidir_2[1]",
            "gpio_control_bidir_2[2]",
        )

    if str(gpio).split(".")[-1] in gpio_to_skip:
        return

    fail = False
    if not Macros["GL"]:
        cocotb.log.info(
            f"[TEST] gpio {gpio} shift {hex(int(gpio._id(f'shift_register',False).value.binstr,2))}({gpio._id(f'shift_register',False).value.binstr}) expected {hex(int(bits,2))}({bits})"
        )
    else:
        shift_reg = ""
        for i in range(bit_size):
            shift_reg += (
                gpio[0]
                ._id(f"\\{gpio[1]}.shift_register[{bit_size-1-i}] ", False)
                .value.binstr
            )
        cocotb.log.info(
            f"[TEST] gpio {gpio[0]}.{gpio[1]}.shift_register shift {hex(int(shift_reg,2))}({shift_reg}) expected {hex(int(bits,2))}({bits})"
        )
    for i in range(bit_size):
        if not Macros["GL"]:
            shift_register = gpio._id("shift_register", False).value.binstr[i]
        else:
            shift_register = (
                gpio[0]
                ._id(f"\\{gpio[1]}.shift_register[{bit_size-1-i}] ", False)
                .value.binstr
            )
        if shift_register != bits[i]:
            fail = True
            cocotb.log.error(f"[TEST] wrong shift register {i} in {gpio}")
    if not fail:
        if not Macros["GL"]:
            cocotb.log.info(f"[TEST] gpio {gpio} passed")
        else:
            cocotb.log.info(f"[TEST] gpio {gpio[1]} passed")
