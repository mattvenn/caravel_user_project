#include <firmware_apis.h>


void main(){
    enable_debug();
    unsigned char *dff_start_address =  (unsigned char *) DFF1_START_ADDR;
    unsigned int dff_size =  DFF1_SIZE;
    unsigned char data = 0x55;
    for (unsigned int i = 0; i < dff_size; i++){
      *(dff_start_address+i) = data; 
    }
    for (unsigned int i = 0; i < dff_size; i++){
        if (data != *(dff_start_address+i)){
            set_debug_reg2(dff_start_address + i);
            set_debug_reg1(0x1E); 
            return;
        }
    }
    
    data = 0xAA;
    for (unsigned int i = 0; i < dff_size; i++){
      *(dff_start_address+i) = data; 
    }
    for (unsigned int i = 0; i < dff_size; i++){
        if (data != *(dff_start_address+i)){
            set_debug_reg2(dff_start_address + i);
            set_debug_reg1(0x1E); 
            return;
        }
    }
    
    set_debug_reg1(0x1B);
}

