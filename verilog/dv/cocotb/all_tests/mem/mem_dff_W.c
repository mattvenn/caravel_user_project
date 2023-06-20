#include <firmware_apis.h>


void main(){
    enable_debug();
    #define dff_start_address  (*(unsigned int*)0x0)  
    dff_start_address = DFF1_START_ADDR;
    #define dff_size  (*(unsigned int*)0x4)  
    dff_size = DFF1_SIZE /4;

    #define shifting  (*(unsigned int*)0x8)  
    #define data_used  (*(unsigned int*)0xC)  
    #define i  (*(volatile uint32_t*)0x10)  

    for (i = 0x14; i < dff_size; i++){
        shifting = 0xFFFFFFFF - (0x1 << i%32);
        data_used = 0x55555555 & shifting;
      *((unsigned int *) dff_start_address+i) = data_used; 
    }
    for (i = 0x14; i < dff_size; i++){
        shifting = 0xFFFFFFFF - (0x1 << i%32);
        data_used = 0x55555555 & shifting;
        if (data_used != *((unsigned int *) dff_start_address+i)){
            set_debug_reg2(dff_start_address+ i);
            set_debug_reg1(0x1E); 
            return;
        }
    }
    
    for (i = 0x14; i < dff_size; i++){
        shifting = 0xFFFFFFFF - (0x1 << i%32);
        data_used = 0xAAAAAAAA & shifting;
      *((unsigned int *)dff_start_address+i) = data_used; 
    }
    for (i = 0x14; i < dff_size; i++){
        shifting = 0xFFFFFFFF - (0x1 << i%32);
        data_used = 0xAAAAAAAA & shifting;
        if (data_used != *((unsigned int *)dff_start_address+i)){
            set_debug_reg2((unsigned int *)dff_start_address+ i);
            set_debug_reg1(0x1E); 
            return;
        }
    }
    
    set_debug_reg1(0x1B);
}