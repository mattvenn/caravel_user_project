#include <firmware_apis.h>

void main(){
    unsigned int i,i_temp, j, active_gpio_num,num_high_gpio;
    enable_debug();
    enableHkSpi(0);
    GPIOs_configureAll(GPIO_MODE_USER_STD_BIDIRECTIONAL);
    GPIOs_loadConfigs();      
    set_debug_reg1(0x1A); // finish configuration

    // // try as output 
    // output_enable_all_gpio_user(1);
    // active_gpio_num = get_active_gpios_num();
    // num_high_gpio = (active_gpio_num - 32);
    // i = 0x1 << num_high_gpio;
    // i_temp = i;
    // for (j = 0; j < num_high_gpio; j++) {
    //         set_gpio_user_h(i);
    //         set_debug_reg2(active_gpio_num-j);
    //         wait_debug_reg1(0xD1); // wait until wait until test read 1
    //         set_gpio_user_h(0x0);
    //         set_debug_reg2(0);
    //         wait_debug_reg1(0xD0);// wait until test read 0
    //         i >>=1;
    //         i |= i_temp;
    // }
    // i = 0x80000000;
    // for (j = 0; j < 32; j++) {
    //         set_gpio_user_h(0x3f);
    //         set_gpio_user_l(i);
    //         set_debug_reg2(32-j);
    //         wait_debug_reg1(0xD1); // wait until test read 1
    //         set_gpio_user_h(0x00);
    //         set_gpio_user_l(0x0);
    //         set_debug_reg2(0);
    //         wait_debug_reg1(0xD0);// wait until test read 0
    //         i >>=1;
    //         i |= 0x80000000;
    // }
    // // try as input
    // output_enable_all_gpio_user(0);
    // // low
    // wait_over_input_l(0xAA,0xFFFFFFFF);
    // wait_over_input_l(0XBB,0xAAAAAAAA);
    // wait_over_input_l(0XCC,0x55555555);
    // wait_over_input_l(0XDD,0x0);
    // // high
    // wait_over_input_h(0XD1,0x3F);
    // wait_over_input_h(0XD2,0x0);
    // wait_over_input_h(0XD3,0x15);
    // wait_over_input_h(0XD4,0x2A);
    // set_debug_reg2(0xFF);
}


void wait_over_input_l(unsigned int start_code, unsigned int exp_val){
    set_debug_reg1(start_code); // configuration done wait environment to send exp_val to reg_mprj_datal
    wait_gpio_user_l(exp_val);
    set_debug_reg2(get_gpio_user_l());

}
void wait_over_input_h(unsigned int start_code, unsigned int exp_val){
    set_debug_reg1(start_code); 
    wait_gpio_user_h(exp_val);
    set_debug_reg2(get_gpio_user_h());
}