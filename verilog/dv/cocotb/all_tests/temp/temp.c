#include <common.h>

void set_registers(){
    for (int i = 0; i < 38; i++){
        if (i<19){
            configure_gpio(i, GPIO_MODE_MGMT_STD_INPUT_PULLUP);

        }else{
            configure_gpio(i, GPIO_MODE_MGMT_STD_OUTPUT);
        }
    }
}
/*
@ finish configuration 
    send packet with size 1

GPIO[0:18] is configured as input pull up and mapped to GPIO[19:37]

input value send to gpio[0:18] suppose to be received as output at GPIO[19:37]
*/
void main(){
    enable_debug();
    enable_hk_spi(0);
    mgmt_gpio_wr(0);
    mgmt_gpio_o_enable();
    set_registers();
    set_gpio_h(0);
    set_gpio_l(0);
    gpio_config_load();
    int mask = 0x7FFFF;
    int mask_h = 0x7E000;
    int i_val = 0;
    int o_val_l;
    int o_val_h;
    while (true){
        mgmt_gpio_wr(1);
        set_debug_reg2(0xDEADBEEF);
        i_val = get_gpio_l() & mask;
        set_debug_reg2(i_val);
        set_debug_reg2(0xDEADBEEF);
        o_val_l = i_val << 19;
        set_debug_reg2(o_val_l);
        set_debug_reg2(0xDEADBEEF);
        o_val_h = i_val & mask_h;
        o_val_h = o_val_h >> 13;
        set_debug_reg2(o_val_h);
        set_gpio_h(o_val_h);
        set_gpio_l(o_val_l);
        mgmt_gpio_wr(0);
    }
}
