#include <common.h>



// --------------------------------------------------------

void main()
{
    User_enableIF();
    // first 3 addresses 
    (*(volatile unsigned int*) (USER_SPACE_ADDR    )) = 0x97cf0d2d; 
    (*(volatile unsigned int*) (USER_SPACE_ADDR +4 )) = 0xbc748313; 
    (*(volatile unsigned int*) (USER_SPACE_ADDR +8 )) = 0xbfda8146; 

    // last 3 addresses 
    (*(volatile unsigned int*) (USER_SPACE_ADDR + USER_SPACE_SIZE -8 )) = 0x5f5e36b1; 
    (*(volatile unsigned int*) (USER_SPACE_ADDR + USER_SPACE_SIZE -4 )) = 0x0c1fe9d9; 
    (*(volatile unsigned int*) (USER_SPACE_ADDR + USER_SPACE_SIZE    )) = 0x6d12d2b8; 


    // random addresses inside the user space 
    (*(volatile unsigned int*) (USER_SPACE_ADDR + 0x72C  )) = 0xdcd244d1; 
    (*(volatile unsigned int*) (USER_SPACE_ADDR + 0x41198)) = 0x0da37088; 
    (*(volatile unsigned int*) (USER_SPACE_ADDR + 0x7770 )) = 0x7b8e4345; 
    // random read 
    int temp;
    temp = (*(volatile unsigned int*) (USER_SPACE_ADDR + 0x9F44  )); 
    temp = (*(volatile unsigned int*) (USER_SPACE_ADDR + 0x58    )); 
    temp = (*(volatile unsigned int*) (USER_SPACE_ADDR + 0x3602EC)); 

    // addresses outside user space - injecting error if user project ack is affected
    GPIOs_configure(14,GPIO_MODE_MGMT_STD_OUTPUT);
    GPIOs_configure(15,GPIO_MODE_MGMT_STD_OUTPUT);
    
    // finish with writing last address with Fs
    (*(volatile unsigned int*)(USER_SPACE_ADDR + USER_SPACE_SIZE)) = 0xFFFFFFFF; 
    

}
