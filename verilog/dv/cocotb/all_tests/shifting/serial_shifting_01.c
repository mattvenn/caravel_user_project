#include <firmware_apis.h>



void main(){
    enable_debug();
    enableHkSpi(0);
    // write 01 
    for (int i =0;i<19;i++){
        if(i % 2 == 0)
           GPIOs_configure(i,0x1555);
        else
           GPIOs_configure(i,0xAAA); 
    }
    for (int i =37;i>=19;i--){
        if(i % 2 != 0)
           GPIOs_configure(i,0x1555);
        else
           GPIOs_configure(i,0xAAA); 
    }
    GPIOs_loadConfigs();
    dummyDelay(10);
    set_debug_reg1(0XFF); // finish configuration 
    dummyDelay(10000);
}

