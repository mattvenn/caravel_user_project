#include <firmware_apis.h>



// --------------------------------------------------------

void main()
{
    User_enableIF();
    // first 2 addresses 
    (*(volatile unsigned int*) (USER_SPACE_ADDR    )) = 0x0314DFE1; 
    (*(volatile unsigned int*) (USER_SPACE_ADDR +0x4 )) = 0x3704E836; 

    // last 2 addresses 
    (*(volatile unsigned int*) (USER_SPACE_ADDR + USER_SPACE_SIZE -0x4 )) = 0x5208E431; 
    (*(volatile unsigned int*) (USER_SPACE_ADDR + USER_SPACE_SIZE)) = 0x77748E32; 


    // random addresses inside the user space 
    (*(volatile unsigned int*) (USER_SPACE_ADDR + 0x344F4)) = 0x89158A64; 
    (*(volatile unsigned int*) (USER_SPACE_ADDR + 0x4F750)) = 0xAE603480; 
    (*(volatile unsigned int*) (USER_SPACE_ADDR + 0x6CE0C)) = 0xD24B086A; 
    (*(volatile unsigned int*) (USER_SPACE_ADDR + 0x8FEE8)) = 0xE50B1442; 
    (*(volatile unsigned int*) (USER_SPACE_ADDR + 0xB767C)) = 0xB23D7EFD; 
    (*(volatile unsigned int*) (USER_SPACE_ADDR + 0xD0A00)) = 0x41C35871; 
    (*(volatile unsigned int*) (USER_SPACE_ADDR + 0xF11D0)) = 0xC0E1638A; 
    (*(volatile unsigned int*) (USER_SPACE_ADDR + 0xC5E54)) = 0x8E16CDA9; 
    (*(volatile unsigned int*) (USER_SPACE_ADDR + 0xE9028)) = 0x42EB0C85; 
    (*(volatile unsigned int*) (USER_SPACE_ADDR + 0x023BC)) = 0xBF9E7B2E;
    // random read 
    int temp;
    temp = (*(volatile unsigned int*) (USER_SPACE_ADDR )); 
    temp = (*(volatile unsigned int*) (USER_SPACE_ADDR + 0x4)); 
    temp = (*(volatile unsigned int*) (USER_SPACE_ADDR + USER_SPACE_SIZE - 0x4)); 
    temp = (*(volatile unsigned int*) (USER_SPACE_ADDR + USER_SPACE_SIZE)); 
    temp = (*(volatile unsigned int*) (USER_SPACE_ADDR + 0x344F4)); 
    temp = (*(volatile unsigned int*) (USER_SPACE_ADDR + 0x4F750)); 
    temp = (*(volatile unsigned int*) (USER_SPACE_ADDR + 0x6CE0C)); 
    temp = (*(volatile unsigned int*) (USER_SPACE_ADDR + 0x8FEE8)); 
    temp = (*(volatile unsigned int*) (USER_SPACE_ADDR + 0xB767C)); 
    temp = (*(volatile unsigned int*) (USER_SPACE_ADDR + 0xD0A00)); 
    temp = (*(volatile unsigned int*) (USER_SPACE_ADDR + 0xF11D0)); 
    temp = (*(volatile unsigned int*) (USER_SPACE_ADDR + 0xC5E54)); 
    temp = (*(volatile unsigned int*) (USER_SPACE_ADDR + 0xE9028)); 
    temp = (*(volatile unsigned int*) (USER_SPACE_ADDR + 0x023BC)); 

    // addresses outside user space - injecting error if user project ack is affected
    GPIOs_configure(14,GPIO_MODE_MGMT_STD_OUTPUT);
    GPIOs_configure(15,GPIO_MODE_MGMT_STD_OUTPUT);
    
    // finish with writing last address with Fs
    (*(volatile unsigned int*)(USER_SPACE_ADDR + USER_SPACE_SIZE)) = 0xFFFFFFFF; 
    

}
