from caravel_cocotb.interfaces.defsParser import Regs

reg = Regs()


"""
reg_mprj_xfer contain
bit 0 : busy
bit 1 : bitbang enable
bit 2 : bitbang reset active low
bit 3 : bitbang load registers
bit 4 : bitbang clock
bit 5 : serial data 1
bit 6 : serial data 2
"""

"""shift the 2 registers with 2 ones"""


async def clock11(cpu):
    reg_mprj_xfer_addr = reg.get_addr("reg_mprj_xfer")
    await cpu.drive_data2address(reg_mprj_xfer_addr, 0x66)  # 0110_0110
    await cpu.drive_data2address(reg_mprj_xfer_addr, 0x76)  # 0111_0110


"""shift the 2 registers with 2 zeros"""


async def clock00(cpu):
    reg_mprj_xfer_addr = reg.get_addr("reg_mprj_xfer")
    await cpu.drive_data2address(reg_mprj_xfer_addr, 0x06)  # 0000_0110
    await cpu.drive_data2address(reg_mprj_xfer_addr, 0x16)  # 0001_0110


"""shift the 2 registers with 1 in the left side and zero in right side"""


async def clock01(cpu):
    reg_mprj_xfer_addr = reg.get_addr("reg_mprj_xfer")
    await cpu.drive_data2address(reg_mprj_xfer_addr, 0x26)  # 0010_0110
    await cpu.drive_data2address(reg_mprj_xfer_addr, 0x36)  # 0011_0110


"""shift the 2 registers with 1 in the left side and zero in right side"""


async def clock10(cpu):
    reg_mprj_xfer_addr = reg.get_addr("reg_mprj_xfer")
    await cpu.drive_data2address(reg_mprj_xfer_addr, 0x46)  # 0100_0110
    await cpu.drive_data2address(reg_mprj_xfer_addr, 0x56)  # 0101_0110


"""enable the serial loader bit to load registers"""


async def load(cpu):
    reg_mprj_xfer_addr = reg.get_addr("reg_mprj_xfer")
    await cpu.drive_data2address(reg_mprj_xfer_addr, 0x06)  # enable bit bang
    await cpu.drive_data2address(reg_mprj_xfer_addr, 0x0E)  # enable loader
    await cpu.drive_data2address(reg_mprj_xfer_addr, 0x06)  # enable bit bang


"""Enable bit-bang mode and clear registers"""


async def clear_registers(cpu):
    reg_mprj_xfer_addr = reg.get_addr("reg_mprj_xfer")
    await cpu.drive_data2address(reg_mprj_xfer_addr, 0x06)  # enable bit bang
    await cpu.drive_data2address(reg_mprj_xfer_addr, 0x04)  # reset
    await cpu.drive_data2address(reg_mprj_xfer_addr, 0x06)  # enable bit bang


"""
--------------------------------------------------------
Clock in an input + output configuration.  The value
passed in "ddhold" is the number of data-dependent hold
violations up to this point.
--------------------------------------------------------

 * Clock in data on the left side.  Assume standard hold
 * violation, so clock in 12 times and assume that the
 * next data to be clocked will start with "1", enforced
 * by the code.
 *
 * Left side = GPIOs 37 to 19
 """


async def clock_in_left_short(cpu, ddhold):
    await clock10(cpu)
    await clock10(cpu)

    for i in range(9):
        if ddhold != 0:
            await clock10(cpu)
            ddhold -= 1
        else:
            await clock00(cpu)

    await clock00(cpu)


async def clock_in_right_short(cpu, ddhold):
    await clock01(cpu)
    await clock01(cpu)

    for i in range(9):
        if ddhold != 0:
            await clock01(cpu)
            ddhold -= 1
        else:
            await clock00(cpu)

    await clock00(cpu)


async def clock_in_left_standard(cpu, ddhold):
    await clock10(cpu)
    await clock10(cpu)

    for i in range(7):
        if ddhold != 0:
            await clock10(cpu)
            ddhold -= 1
        else:
            await clock00(cpu)

    await clock10(cpu)
    await clock00(cpu)
    await clock00(cpu)
    await clock10(cpu)


"""right output left input"""


async def clock_in_right_o_left_i_standard(cpu):
    if sky:
        await clock11(cpu)
        await clock11(cpu)
        for i in range(7):
            await clock00(cpu)
        await clock10(cpu)
        await clock00(cpu)
        await clock01(cpu)
        await clock11(cpu)
    else:
        for i in range(6):
            await clock00(cpu)
        await clock10(cpu)
        await clock01(cpu)
        await clock11(cpu)
        await clock11(cpu)


"""right input left output"""


async def clock_in_right_i_left_o_standard(cpu):
    if sky:
        await clock11(cpu)
        await clock11(cpu)
        for i in range(7):
            await clock00(cpu)
        await clock01(cpu)
        await clock00(cpu)
        await clock10(cpu)
        await clock11(cpu)
    else:
        for i in range(6):
            await clock00(cpu)
        await clock01(cpu)
        await clock10(cpu)
        await clock11(cpu)
        await clock11(cpu)


"""right input left output"""


async def clock_in_right_i_left_i_standard(cpu):
    if sky:
        await clock11(cpu)
        await clock11(cpu)
        for i in range(7):
            await clock00(cpu)
        await clock00(cpu)
        await clock00(cpu)
        await clock11(cpu)
        await clock11(cpu)
    else:
        for i in range(6):
            await clock00(cpu)
        await clock00(cpu)
        await clock11(cpu)
        await clock11(cpu)
        await clock11(cpu)


"""right output left output"""


async def clock_in_right_o_left_o_standard(cpu):
    if sky:
        await clock11(cpu)
        await clock11(cpu)
        for i in range(7):
            await clock00(cpu)
        await clock11(cpu)
        await clock00(cpu)
        await clock00(cpu)
        await clock11(cpu)
    else:
        for i in range(6):
            await clock00(cpu)
        await clock11(cpu)
        await clock00(cpu)
        await clock11(cpu)
        await clock11(cpu)


async def clock_in_end_output(cpu):
    # Right side:  GPIO 0 configured disabled
    # /Left side:  GPIO 37 configured as output
    await clock11(cpu)
    await clock11(cpu)
    await clock00(cpu)
    await clock00(cpu)
    await clock00(cpu)
    await clock00(cpu)
    await clock00(cpu)
    await clock00(cpu)
    await clock00(cpu)
    await clock00(cpu)
    await clock00(cpu)
    await clock01(cpu)
    await clock11(cpu)
    await load(cpu)
    reg_mprj_io_37_addr = reg.get_addr("reg_mprj_io_37")
    await cpu.drive_data2address(reg_mprj_io_37_addr, 0x1809)
