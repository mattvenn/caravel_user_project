import cocotb
from cocotb.triggers import RisingEdge, NextTimeStep
import cocotb.log
from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test
from user_design import configure_userdesign


@cocotb.test()
@report_test
async def user_address_space(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=31776)
    cocotb.log.info("[TEST] Start user_address_space test")
    ack_hdl = caravelEnv.caravel_hdl.mprj.wbs_ack_o
    addr_hdl = caravelEnv.caravel_hdl.mprj.wbs_adr_i
    data_o_hdl = caravelEnv.caravel_hdl.mprj.wbs_dat_o
    data_i_hdl = caravelEnv.caravel_hdl.mprj.wbs_dat_i
    we_hdl = caravelEnv.caravel_hdl.mprj.wbs_we_i
    
    start_addr = int(caravelEnv.design_macros.USER_SPACE_ADDR)
    print(f"user space adddress = {start_addr}")
    user_size = int(caravelEnv.design_macros.USER_SPACE_SIZE)
    addr_arr = (
        start_addr,
        start_addr + 4,
        start_addr + user_size - 4,
        start_addr + user_size,
        start_addr + 0x344F4,
        start_addr + 0x4F750,
        start_addr + 0x6CE0C,
        start_addr + 0x8FEE8,
        start_addr + 0xB767C,
        start_addr + 0xD0A00,
        start_addr + 0xF11D0,
        start_addr + 0xC5E54,
        start_addr + 0xE9028,
        start_addr + 0x023BC,
        #read 
        start_addr,
        start_addr + 4,
        start_addr + user_size - 4,
        start_addr + user_size,
        start_addr + 0x344F4,
        start_addr + 0x4F750,
        start_addr + 0x6CE0C,
        start_addr + 0x8FEE8,
        start_addr + 0xB767C,
        start_addr + 0xD0A00,
        start_addr + 0xF11D0,
        start_addr + 0xC5E54,
        start_addr + 0xE9028,
        start_addr + 0x023BC,
        start_addr + user_size 
    )
    data_arr = (
        0x0314DFE1,
        0x3704E836,
        0x5208E431,
        0x77748E32,
        0x89158A64,
        0xAE603480,
        0xD24B086A,
        0xE50B1442,
        0xB23D7EFD,
        0x41C35871,
        0xC0E1638A,
        0x8E16CDA9,
        0x42EB0C85,
        0xBF9E7B2E, 
        #read
        0x0314DFE1,
        0x3704E836,
        0x5208E431,
        0x77748E32,
        0x89158A64,
        0xAE603480,
        0xD24B086A,
        0xE50B1442,
        0xB23D7EFD,
        0x41C35871,
        0xC0E1638A,
        0x8E16CDA9,
        0x42EB0C85,
        0xBF9E7B2E
    )
    await configure_userdesign(caravelEnv, used_addr=addr_arr)
    print([hex(i) for i in addr_arr])
    for addr, data in zip(addr_arr, data_arr):
        await RisingEdge(ack_hdl)
        await NextTimeStep()
        if addr_hdl.value.integer != addr:
            cocotb.log.error(
                f"[TEST] seeing unexpected address {hex(addr_hdl.value.integer)} expected {hex(addr)}"
            )
        elif we_hdl.value.integer == 1:# write
            if data_i_hdl.value.integer != data:
                cocotb.log.error(
                    f"[TEST] seeing unexpected write data {hex(data_i_hdl.value.integer)} expected {hex(data)} address {hex(addr)}"
                )
            else:
                cocotb.log.info(
                    f"[TEST] seeing the correct data {hex(data)} from address {hex(addr)}"
                )
        elif we_hdl.value.integer == 0:# read
            if data_o_hdl.value.integer != data:
                cocotb.log.error(
                    f"[TEST] seeing unexpected read data {hex(data_o_hdl.value.integer)} expected {hex(data)} address {hex(addr)}"
                )
        
            else:
                cocotb.log.info(
                    f"[TEST] seeing the correct data {hex(data)} from address {hex(addr)}"
                )
