import cocotb
from cocotb.triggers import RisingEdge
import cocotb.log
from caravel_cocotb.caravel_interfaces import test_configure
from caravel_cocotb.caravel_interfaces import report_test


@cocotb.test()
@report_test
async def user_address_space(dut):
    caravelEnv = await test_configure(dut, timeout_cycles=40620)
    cocotb.log.info("[TEST] Start user_address_space test")
    ack_hdl = caravelEnv.caravel_hdl.mprj.addr_space_testing.wbs_ack_o
    addr_hdl = caravelEnv.caravel_hdl.mprj.addr_space_testing.addr
    data_hdl = caravelEnv.caravel_hdl.mprj.addr_space_testing.data
    start_addr = int(caravelEnv.design_macros.USER_SPACE_ADDR)
    print(f"user space adddress = {start_addr}")
    user_size = int(caravelEnv.design_macros.USER_SPACE_SIZE)
    addr_arr = (
        start_addr,
        start_addr + 4,
        start_addr + 8,
        start_addr + user_size - 8,
        start_addr + user_size - 4,
        start_addr + user_size,
        start_addr + 0x72C,
        start_addr + 0x41198,
        start_addr + 0x7770,
        start_addr + 0x9F44,
        start_addr + 0x58,
        start_addr + 0x3602EC,
        start_addr + user_size,
    )
    data_arr = (
        0x97CF0D2D,
        0xBC748313,
        0xBFDA8146,
        0x5F5E36B1,
        0x0C1FE9D9,
        0x6D12D2B8,
        0xDCD244D1,
        0x0DA37088,
        0x7B8E4345,
        0x00000777,
        0x00000777,
        0x00000777,
        0xFFFFFFFF,
    )
    print([hex(i) for i in addr_arr])
    for addr, data in zip(addr_arr, data_arr):
        await RisingEdge(ack_hdl)
        if addr_hdl.value.integer != addr:
            cocotb.log.error(
                f"[TEST] seeing unexpected address {hex(addr_hdl.value.integer)} expected {hex(addr)}"
            )
        elif data_hdl.value.integer != data:
            cocotb.log.error(
                f"[TEST] seeing unexpected data {hex(data_hdl.value.integer)} expected {hex(data)} address {hex(addr)}"
            )
        else:
            cocotb.log.info(
                f"[TEST] seeing the correct data {hex(data)} from address {hex(addr)}"
            )
