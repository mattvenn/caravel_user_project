#include <defs.h>

void main()
{
    #ifdef ARM // ARM use dirrent location 
    reg_wb_enable =0x8; // for enable writing to reg_debug_1 and reg_debug_2
    #else 
    reg_wb_enable =1; // for enable writing to reg_debug_1 and reg_debug_2
    #endif
    reg_debug_1  = 0;
    reg_debug_2  = 0;

    #define dff_size  (*(volatile uint32_t*)0x0)  
    dff_size = 0x200;
    #define iterator  (*(volatile uint32_t*)0x4)  // first address in the ram store the iterator 
    iterator = 0;
    for (iterator = 8; iterator < dff_size; iterator++ ){
        // reg_debug_2 = iterator;
        *((unsigned int *) 0x00000000 + iterator) = 0x55555555; 
    }
    for (iterator = 8; iterator < dff_size; iterator++ ){
        // reg_debug_2 = iterator;
        if (*((unsigned int *) 0x00000000 + iterator) !=  0x55555555){
            reg_debug_2 = iterator;
            reg_debug_1 = 0x1E; 
            return;
        }
    }
    for (iterator = 8; iterator < dff_size; iterator++ ){
        // reg_debug_2 = iterator;
        *((unsigned int *) 0x00000000 + iterator) = 0xAAAAAAAA; 
    }
    for (iterator = 8; iterator < dff_size; iterator++ ){
      // reg_debug_2 = iterator;
        if (*((unsigned int *) 0x00000000 + iterator) != 0xAAAAAAAA){
            // reg_debug_2 = iterator;
            reg_debug_1 = 0x1E; 
            return;
        }
    }

    reg_debug_1 = 0x1B;
}