

#include <common.h>




// --------------------------------------------------------

void main()
{

    enable_debug();
    mgmt_debug_enable();
    set_debug_reg1(0xAA);
    // very long wait
    dummy_delay(150000000);


}
