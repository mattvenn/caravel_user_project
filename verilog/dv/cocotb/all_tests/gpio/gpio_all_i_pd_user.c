#include <firmware_apis.h>



void main(){
    enable_debug();
    enableHkSpi(0);
    // output_enable_all_gpio_user(1);
    GPIOs_configureAll(GPIO_MODE_USER_STD_INPUT_PULLDOWN);
    GPIOs_loadConfigs();      
    set_debug_reg1(0xAA); // finish configuration 
    //print("adding a very very long delay because cpu produces X's when code finish and this break the simulation");
    for(int i=0; i<100000000; i++);

    while (1);
}
