#include <firmware_apis.h>


// --------------------------------------------------------

void main(){
    enable_debug();
    /* Monitor pins must be set to output */
    GPIOs_configure(14,GPIO_MODE_MGMT_STD_OUTPUT);
    GPIOs_configure(15,GPIO_MODE_MGMT_STD_OUTPUT);
    /* Apply configuration */
    GPIOs_loadConfigs();
    set_debug_reg1(0xAA);
    dummyDelay(100000000);
    return; 
}