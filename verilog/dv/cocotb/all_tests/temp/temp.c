#include <firmware_apis.h>

void set_registers(){
    for (int i = 0; i < 38; i++){
        if (i<19){
            GPIOs_configure(i, GPIO_MODE_MGMT_STD_INPUT_PULLUP);

        }else{
            GPIOs_configure(i, GPIO_MODE_MGMT_STD_OUTPUT);
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
    enableHkSpi(0);
    ManagmentGpio_write(0);
    ManagmentGpio_outputEnable();
    set_registers();
    GPIOs_writeHigh(0);
    GPIOs_writeLow(0);
    GPIOs_loadConfigs();
    int mask = 0x7FFFF;
    int mask_h = 0x7E000;
    int i_val = 0;
    int o_val_l;
    int o_val_h;
    while (true){
        ManagmentGpio_write(1);
        set_debug_reg2(0xDEADBEEF);
        i_val = GPIOs_readLow() & mask;
        set_debug_reg2(i_val);
        set_debug_reg2(0xDEADBEEF);
        o_val_l = i_val << 19;
        set_debug_reg2(o_val_l);
        set_debug_reg2(0xDEADBEEF);
        o_val_h = i_val & mask_h;
        o_val_h = o_val_h >> 13;
        set_debug_reg2(o_val_h);
        GPIOs_writeHigh(o_val_h);
        GPIOs_writeLow(o_val_l);
        ManagmentGpio_write(0);
    }
}
