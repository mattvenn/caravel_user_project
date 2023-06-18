#include <firmware_apis.h>


// --------------------------------------------------------

void main(){
    enable_debug();
    set_debug_reg2(0xBB);
    wait_debug_reg1(0xAA);
    enableHkSpi(1);
    reg_hkspi_pll_ena =0;
    set_debug_reg1(0xBB);
    dummyDelay(100000000);
}