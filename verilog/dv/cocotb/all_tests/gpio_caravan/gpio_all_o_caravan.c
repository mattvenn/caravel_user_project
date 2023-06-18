#include <firmware_apis.h>


void main(){
        unsigned int i,i_temp, j, active_gpio_num,num_high_gpio;
        enable_debug();
        enable_hk_spi(0);
        configure_all_gpios(GPIO_MODE_MGMT_STD_OUTPUT);        
        gpio_config_load();      
        set_debug_reg1(0xAA); // finish configuration 
        set_gpio_l(0x0);
        set_gpio_h(0x0);
        active_gpio_num = get_active_gpios_num();
        num_high_gpio = (active_gpio_num - 32);
        i = 0x1 << num_high_gpio;
        i_temp = i;
        for (j = 0; j < num_high_gpio; j++) {
                set_gpio_h(i);
                set_debug_reg2(active_gpio_num-j);
                wait_debug_reg1(0xD1); // wait until wait until test read 1
                set_gpio_h(0x0);
                set_debug_reg2(0);
                wait_debug_reg1(0xD0);// wait until test read 0
                i >>=1;
                i |= i_temp;
        }
        i = 0x80000000;
        for (j = 0; j < 32; j++) {
                set_gpio_h(0x3f);
                set_gpio_l(i);
                set_debug_reg2(32-j);
                wait_debug_reg1(0xD1); // wait until test read 1
                set_gpio_h(0x00);
                set_gpio_l(0x0);
                set_debug_reg2(0);
                wait_debug_reg1(0xD0);// wait until test read 0
                i >>=1;
                i |= 0x80000000;
        }
        set_debug_reg1(0XFF); // configuration done wait environment to send 0xFFA88C5A to reg_mprj_datal
}
