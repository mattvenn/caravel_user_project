

#include <firmware_apis.h>




// --------------------------------------------------------

void main()
{

    enable_debug();
    mgmt_debug_enable();
    set_debug_reg1(0xAA);
    // very long wait
    dummyDelay(150000000);


}
