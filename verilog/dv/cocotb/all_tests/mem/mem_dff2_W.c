#include <firmware_apis.h>


void main(){
    enable_debug();
    unsigned int *dff2_start_address =  (unsigned int *) DFF2_START_ADDR;
    unsigned int dff2_size =  DFF2_SIZE / 4;
    unsigned int data = 0x55555555;
    unsigned int mask = 0xFFFFFFFF;
    unsigned int shifting =0;
    unsigned int data_used = 0;
    for (unsigned int i = 0; i < dff2_size; i++){
        shifting = mask - (0x1 << i%32);
        data_used = data & shifting;
        data_used = data_used | i; // to dectect if rollover to the address happened before size reached
      *(dff2_start_address+i) = data_used; 
    }
    for (unsigned int i = 0; i < dff2_size; i++){
        shifting = mask - (0x1 << i%32);
        data_used = data & shifting;
        data_used = data_used | i; // to dectect if rollover to the address happened before size reached
        if (data_used != *(dff2_start_address+i)){
            set_debug_reg2(dff2_start_address + i);
            set_debug_reg1(0x1E); 
            return;
        }
    }

    data = 0xAAAAAAAA;
    for (unsigned int i = 0; i < dff2_size; i++){
        shifting = mask - (0x1 << i%32);
        data_used = data & shifting;
        data_used = data_used | i; // to dectect if rollover to the address happened before size reached
      *(dff2_start_address+i) = data_used; 
    }
    for (unsigned int i = 0; i < dff2_size; i++){
        shifting = mask - (0x1 << i%32);
        data_used = data & shifting;
        data_used = data_used | i; // to dectect if rollover to the address happened before size reached
        if (data_used != *(dff2_start_address+i)){
            set_debug_reg2(dff2_start_address + i);
            set_debug_reg1(0x1E); 
            return;
        }
    }

    set_debug_reg1(0x1B);

}