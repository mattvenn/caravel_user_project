#include <firmware_apis.h>



void main()
{
    enable_debug();
    set_debug_reg1(0x0);
    set_debug_reg1(0x1);
    set_debug_reg1(0x2);
    set_debug_reg1(0x3);
    set_debug_reg1(0x4);
    set_debug_reg1(0x5);
    while(get_debug_reg2() == 0x0);
    reg_hkspi_reset = 1;
}
