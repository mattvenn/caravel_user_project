
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

reg_mprj_xfer = 0x13


async def bb_clock11_spi(spi_master):
    await spi_master.write_reg_spi(address=reg_mprj_xfer, data=0x66) 
    await spi_master.write_reg_spi(address=reg_mprj_xfer, data=0x76)


async def bb_clock00_spi(spi_master):
    await spi_master.write_reg_spi(address=reg_mprj_xfer, data=0x06) 
    await spi_master.write_reg_spi(address=reg_mprj_xfer, data=0x16) 


async def bb_clock01_spi(spi_master):
    await spi_master.write_reg_spi(address=reg_mprj_xfer, data=0x26) 
    await spi_master.write_reg_spi(address=reg_mprj_xfer, data=0x36) 


async def bb_clock10_spi(spi_master):
    await spi_master.write_reg_spi(address=reg_mprj_xfer, data=0x46) 
    await spi_master.write_reg_spi(address=reg_mprj_xfer, data=0x56)


async def bb_load_spi(spi_master):
    await spi_master.write_reg_spi(address=reg_mprj_xfer, data=0x0E) 
    # await spi_master.write_reg_spi(address=reg_mprj_xfer, data=0x06) 

async def bb_reset_spi(spi_master):
    await spi_master.write_reg_spi(address=reg_mprj_xfer, data=0x04) 
    await spi_master.write_reg_spi(address=reg_mprj_xfer, data=0x06)

# configure the GPIO  in the left chain with configL and the GPIO  in
# the right chain with configR
# left | right
# 18	& 19
# 17	& 20
# 16	& 21
# 15	& 22
# 14	& 23
# 13	& 24
# 12	& 25
# 11	& 26
# 10	& 27
# 9	& 28
# 8	& 29
# 7	& 30
# 6	& 31
# 5	& 32
# 4	& 33
# 3	& 34
# 2	& 35
# 1	& 36
# 0	& 37
async def bb_configure_2_gpios_spi(configL, configR, spi_master):
    num_bits = 13
    mask = 0x1 << num_bits - 1
    for i in reversed(range(num_bits)):
        left = (configL & mask) >> i
        right = (configR & mask) >> i
        mask = mask >> 1
        if left:
            if right:
                await bb_clock11_spi(spi_master)
            else:
                await bb_clock10_spi(spi_master)

        else:
            if right:
                await bb_clock01_spi(spi_master)
            else:
                await bb_clock00_spi(spi_master)


async def bb_configure_all_gpios(config, spi_master):
    await bb_reset_spi(spi_master)
    await bb_configure_2_gpios_spi(config, config, spi_master)  # 18	& 19
    await bb_configure_2_gpios_spi(config, config, spi_master)  # 17	& 20
    await bb_configure_2_gpios_spi(config, config, spi_master)  # 16	& 21
    await bb_configure_2_gpios_spi(config, config, spi_master)  # 15	& 22
    await bb_configure_2_gpios_spi(config, config, spi_master)  # 14	& 23
    await bb_configure_2_gpios_spi(config, config, spi_master)  # 13	& 24
    await bb_configure_2_gpios_spi(config, config, spi_master)  # 12	& 25
    await bb_configure_2_gpios_spi(config, config, spi_master)  # 11	& 26
    await bb_configure_2_gpios_spi(config, config, spi_master)  # 10	& 27
    await bb_configure_2_gpios_spi(config, config, spi_master)  # 9	& 28
    await bb_configure_2_gpios_spi(config, config, spi_master)  # 8	& 29
    await bb_configure_2_gpios_spi(config, config, spi_master)  # 7	& 30
    await bb_configure_2_gpios_spi(config, config, spi_master)  # 6	& 31
    await bb_configure_2_gpios_spi(config, config, spi_master)  # 5	& 32
    await bb_configure_2_gpios_spi(config, config, spi_master)  # 4	& 33
    await bb_configure_2_gpios_spi(config, config, spi_master)  # 3	& 34
    await bb_configure_2_gpios_spi(config, config, spi_master)  # 2	& 35
    await bb_configure_2_gpios_spi(config, config, spi_master)  # 1	& 36
    await bb_configure_2_gpios_spi(config, config, spi_master)  # 0	& 37
    await bb_load_spi(spi_master)
