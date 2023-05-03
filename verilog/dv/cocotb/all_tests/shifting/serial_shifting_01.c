#include <common.h>



void main(){
    enable_debug();
    enable_hk_spi(0);
    // write 01 
    for (int i =0;i<19;i++){
        if(i % 2 == 0)
           configure_gpio(i,0x1555);
        else
           configure_gpio(i,0xAAA); 
    }
    for (int i =37;i>=19;i--){
        if(i % 2 != 0)
           configure_gpio(i,0x1555);
        else
           configure_gpio(i,0xAAA); 
    }
    gpio_config_load();
    dummy_delay(10);
    set_debug_reg1(0XFF); // finish configuration 
    dummy_delay(10000);
}

