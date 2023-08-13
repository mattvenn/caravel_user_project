
#include <firmware_apis.h>

void main(){
    enable_debug();
    enableHkSpi(0);
    ManagmentGpio_outputEnable();
    while (true){
        GPIOs_writeLow(0x0);
        GPIOs_writeHigh(0x0);
        // write input to the user project
        int gpio_l = GPIOs_readLow();
        int gpio_h = GPIOs_readHigh();
        set_debug_reg1(gpio_l);
        set_debug_reg2(gpio_h);
        ManagmentGpio_write(0);
        GPIOs_writeLow(0xFFFFFFFF);
        GPIOs_writeHigh(0x3F);
        ManagmentGpio_write(1);  
    }
}