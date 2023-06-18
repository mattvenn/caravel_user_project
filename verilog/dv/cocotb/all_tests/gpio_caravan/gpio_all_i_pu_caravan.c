#include <firmware_apis.h>

void main(){
    enable_debug();
    enable_hk_spi(0);
    configure_all_gpios(GPIO_MODE_MGMT_STD_INPUT_PULLUP);
    gpio_config_load();

    set_debug_reg1(0XAA); // configuration done 
    //print("adding a very very long delay because cpu produces X's when code finish and this break the simulation");
    for(int i=0; i<100000000; i++);
    while (true);
}
