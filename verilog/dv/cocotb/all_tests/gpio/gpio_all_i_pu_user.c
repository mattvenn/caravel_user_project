#include <common.h>



void main(){
    enable_debug();
    enable_hk_spi(0);
    output_enable_all_gpio_user(1);
    set_gpio_user_l(0xFFFFFFFF);
    set_gpio_user_h(0x3F);
    configure_all_gpios(GPIO_MODE_USER_STD_INPUT_PULLUP);
    gpio_config_load();      
    set_debug_reg1(0xAA); // finish configuration 
    //print("adding a very very long delay because cpu produces X's when code finish and this break the simulation");
    for(int i=0; i<100000000; i++);

    while (1);
}
