import cocotb
import cocotb.log
from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
from user_design import configure_userdesign


def shift(gpio, shift_type, caravelEnv):
    bit_size = int(caravelEnv.design_macros.IO_CTRL_BITS)
    if shift_type:
        bits = "0101010101010"
        if bit_size != 13:
            bits = bits[0:bit_size-1]
    else:
        bits = "1010101010101"
        if bit_size != 13:
            bits = bits[0:bit_size-1]
    fail = False
    gpio_to_skip = ()

    if "CPU_TYPE_ARM" in caravelEnv.design_macros._asdict():
        gpio_to_skip = (
            "gpio_control_bidir_2[0]",
            "gpio_control_bidir_2[1]",
            "gpio_control_bidir_2[2]",
        )

    if str(gpio).split(".")[-1] in gpio_to_skip:
        return

    if 'GL' not in caravelEnv.design_macros._asdict():
        cocotb.log.info(
            f"[TEST] gpio {gpio} shift {gpio._id(f'shift_register',False).value} expected {bits}"
        )
    for i in range(bit_size):
        if 'GL' not in caravelEnv.design_macros._asdict():
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
        if 'GL' not in caravelEnv.design_macros._asdict():
            cocotb.log.info(f"[TEST] gpio {gpio} passed")
        else:
            cocotb.log.info(f"[TEST] gpio {gpio[1]} passed")


@cocotb.test()
@report_test
async def serial_shifting_10(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=540110)
    debug_regs = await configure_userdesign(caravelEnv)
    uut = dut.uut.chip_core
    debug_regs = await configure_userdesign(caravelEnv)
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
    if 'CARAVAN' in caravelEnv.design_macros._asdict():
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
    if 'CARAVAN' in caravelEnv.design_macros._asdict():
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
        if 'GL' not in caravelEnv.design_macros._asdict():
            shift(uut._id(gpio, False), type, caravelEnv)
        else:
            shift((uut, gpio), type, caravelEnv)
        type = not type
    type = True  # type of shifting 01 or 10
    for gpio in reversed(gpios_h):
        if 'GL' not in caravelEnv.design_macros._asdict():
            shift(uut._id(gpio, False), type, caravelEnv)
        else:
            shift((uut, gpio), type, caravelEnv)
        type = not type


@cocotb.test()
@report_test
async def serial_shifting_01(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=541278)
    debug_regs = await configure_userdesign(caravelEnv)
    uut = dut.uut.chip_core
    debug_regs = await configure_userdesign(caravelEnv)
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
    if 'CARAVAN' in caravelEnv.design_macros._asdict():
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
    if 'CARAVAN' in caravelEnv.design_macros._asdict():
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
        if 'GL' not in caravelEnv.design_macros._asdict():
            shift(uut._id(gpio, False), type, caravelEnv)
        else:
            shift((uut, gpio), type, caravelEnv)
        type = not type
    type = False  # type of shifting 01 or 10
    for gpio in reversed(gpios_h):
        if 'GL' not in caravelEnv.design_macros._asdict():
            shift(uut._id(gpio, False), type, caravelEnv)
        else:
            shift((uut, gpio), type, caravelEnv)
        type = not type


@cocotb.test()
@report_test
async def serial_shifting_0011(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=700516)
    debug_regs = await configure_userdesign(caravelEnv)
    uut = dut.uut.chip_core
    debug_regs = await configure_userdesign(caravelEnv)
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
    if 'CARAVAN' in caravelEnv.design_macros._asdict():
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
    if 'CARAVAN' in caravelEnv.design_macros._asdict():
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
        if 'GL' not in caravelEnv.design_macros._asdict():
            shift_2(uut._id(gpio, False), type, caravelEnv)
        else:
            shift_2((uut, gpio), type, caravelEnv)
        type = (type + 1) % 4
    type = 2  # type of shifting 01 or 10
    for gpio in reversed(gpios_h):
        if 'GL' not in caravelEnv.design_macros._asdict():
            shift_2(uut._id(gpio, False), type, caravelEnv)
        else:
            shift_2((uut, gpio), type, caravelEnv)
        type = (type + 1) % 4


@cocotb.test()
@report_test
async def serial_shifting_1100(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=700331)
    debug_regs = await configure_userdesign(caravelEnv)
    uut = dut.uut.chip_core
    debug_regs = await configure_userdesign(caravelEnv)
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
    if 'CARAVAN' in caravelEnv.design_macros._asdict():
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
    if 'CARAVAN' in caravelEnv.design_macros._asdict():
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
        if 'GL' not in caravelEnv.design_macros._asdict():
            shift_2(uut._id(gpio, False), type, caravelEnv)
        else:
            shift_2((uut, gpio), type, caravelEnv)
        type = (type + 1) % 4
    type = 0  # type of shifting 01 or 10
    for gpio in reversed(gpios_h):
        if 'GL' not in caravelEnv.design_macros._asdict():
            shift_2(uut._id(gpio, False), type, caravelEnv)
        else:
            shift_2((uut, gpio), type, caravelEnv)
        type = (type + 1) % 4


def shift_2(gpio, shift_type, caravelEnv):
    bit_size = int(caravelEnv.design_macros.IO_CTRL_BITS)
    if shift_type == 0:
        bits = "0011001100110"
        if bit_size != 13:
            bits = bits[0:bit_size-1]
    elif shift_type == 1:
        bits = "0110011001100"
        if bit_size != 13:
            bits = bits[0:bit_size-1]
    elif shift_type == 2:
        bits = "1100110011001"
        if bit_size != 13:
            bits = bits[0:bit_size-1]
    elif shift_type == 3:
        bits = "1001100110011"
        if bit_size != 13:
            bits = bits[0:bit_size-1]
    gpio_to_skip = ()
    if "CPU_TYPE_ARM" in caravelEnv.design_macros._asdict():
        gpio_to_skip = (
            "gpio_control_bidir_2[0]",
            "gpio_control_bidir_2[1]",
            "gpio_control_bidir_2[2]",
        )

    if str(gpio).split(".")[-1] in gpio_to_skip:
        return

    fail = False
    if 'GL' not in caravelEnv.design_macros._asdict():
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
        if 'GL' not in caravelEnv.design_macros._asdict():
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
        if 'GL' not in caravelEnv.design_macros._asdict():
            cocotb.log.info(f"[TEST] gpio {gpio} passed")
        else:
            cocotb.log.info(f"[TEST] gpio {gpio[1]} passed")
