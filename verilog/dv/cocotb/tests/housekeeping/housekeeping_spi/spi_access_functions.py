async def write_reg_spi(caravelEnv, address, data):
    await caravelEnv.enable_csb()
    await caravelEnv.hk_write_byte(0x80)  # Write stream command
    await caravelEnv.hk_write_byte(
        address
    )  # Address (register 19 = GPIO bit-bang control)
    await caravelEnv.hk_write_byte(data)  # Data
    await caravelEnv.disable_csb()


async def read_reg_spi(caravelEnv, address):
    await caravelEnv.enable_csb()
    await caravelEnv.hk_write_byte(0x40)  # read stream command
    await caravelEnv.hk_write_byte(address)  # Address
    data = await caravelEnv.hk_read_byte()  # Data
    await caravelEnv.disable_csb()
    return data


async def read_write_reg_spi(caravelEnv, address, data):
    await caravelEnv.enable_csb()
    await caravelEnv.hk_write_byte(0xC0)  # Write stream command
    await caravelEnv.hk_write_byte(address)
    data = await caravelEnv.hk_write_read_byte(data)
    await caravelEnv.disable_csb()
    return data


async def write_reg_spi_nbytes(caravelEnv, address, data, n_bytes):
    write_command = 0x2 << 6 | n_bytes << 3
    print(f"command = {hex(write_command)}")
    await caravelEnv.enable_csb()
    await caravelEnv.hk_write_byte(write_command)  # Write n byte command
    await caravelEnv.hk_write_byte(
        address
    )  # Address (register 19 = GPIO bit-bang control)
    for byte in data:
        await caravelEnv.hk_write_byte(byte)  # Data
    await caravelEnv.disable_csb()


async def read_reg_spi_nbytes(caravelEnv, address, n_bytes):
    data = []
    await caravelEnv.enable_csb()
    await caravelEnv.hk_write_byte(0x40)  # read stream command
    await caravelEnv.hk_write_byte(address)  # Address
    for i in range(n_bytes):
        data.append(await caravelEnv.hk_read_byte())  # Data
    await caravelEnv.disable_csb()
    return data


async def reg_spi_user_pass_thru(caravelEnv, command, address):
    await caravelEnv.enable_csb()
    await caravelEnv.hk_write_byte(
        0x02
    )  # Apply user pass-thru command to housekeeping SPI
    await caravelEnv.hk_write_byte(command)  # read command
    address = address.to_bytes(3, "big")
    await caravelEnv.hk_write_byte(address[0])  # high byte
    await caravelEnv.hk_write_byte(address[1])  # middle byte
    await caravelEnv.hk_write_byte(address[2])  # low byte


async def reg_spi_user_pass_thru_read(caravelEnv):
    data = await caravelEnv.hk_read_byte()
    return data


# use for configure in mgmt pass thru or user pass thru
async def reg_spi_op(caravelEnv, command, address):
    await caravelEnv.enable_csb()
    await caravelEnv.hk_write_byte(command)  # command
    await caravelEnv.hk_write_byte(address)  # Address
    await caravelEnv.disable_csb()
