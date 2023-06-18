#include <firmware_apis.h>



void main(){
    enable_debug();
    enableHkSpi(0);
    int counter = 0;
    for (int i =0;i<19;i++){
        if(counter == 0)
           GPIOs_configure(i,0x666);
        else if (counter == 1)
           GPIOs_configure(i,0xccc); 
        else if (counter == 2)
           GPIOs_configure(i,0x1999); 
        else if (counter == 3)
           GPIOs_configure(i,0x1333); 
        counter++; 
        counter %= 4;
    }
    counter =0;
    for (int i =37;i>=19;i--){
        if(counter == 0)
           GPIOs_configure(i,0x666);
        else if (counter == 1)
           GPIOs_configure(i,0xccc); 
        else if (counter == 2)
           GPIOs_configure(i,0x1999); 
        else if (counter == 3)
           GPIOs_configure(i,0x1333); 
        counter++; 
        counter %= 4;
    }
    GPIOs_loadConfigs();
    dummyDelay(10);
    set_debug_reg1(0XFF); // finish configuration 
    dummyDelay(10000); 
}
