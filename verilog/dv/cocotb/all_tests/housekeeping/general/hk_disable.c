#include <common.h>


// --------------------------------------------------------

void main(){
    enable_debug();
    set_debug_reg2(0xBB);
    wait_debug_reg1(0xAA);
    enable_hk_spi(1);
    reg_hkspi_pll_ena =0;
    set_debug_reg1(0xBB);
    dummy_delay(100000000);
}