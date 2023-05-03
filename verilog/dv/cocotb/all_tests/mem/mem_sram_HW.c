#include <defs.h>

void main()
{
    #ifdef ARM // ARM use dirrent location 
    reg_wb_enable =0x8; // for enable writing to reg_debug_1 and reg_debug_2
    #else 
    reg_wb_enable =1; // for enable writing to reg_debug_1 and reg_debug_2
    #endif
    reg_debug_1  = 0x0;
    reg_debug_2  = 0x0;
    #define dff_size  (*(volatile uint32_t*)0x0)  
    #define iterator  (*(volatile uint32_t*)0x4)  // first address in the ram store the iterator 
    dff_size = 0x400;
    for (iterator = 8; iterator < dff_size; iterator++){
      // reg_debug_2 = iterator;
      *((unsigned short *) 0x00000000+iterator) = 0x5555; 

    }
    for (iterator = 8; iterator < dff_size; iterator++){
      // reg_debug_2 = iterator;
        if (*((unsigned short *) 0x00000000+iterator) !=  0x5555){
            reg_debug_2 = iterator;
            reg_debug_1 = 0x1E; 
            return;
        }
    }
    
    for (iterator = 8; iterator < dff_size; iterator++){
      // reg_debug_2 = iterator;
      *((unsigned short *) 0x00000000+iterator) = 0xAAAA; 
    }
    for (iterator = 8; iterator < dff_size; iterator++){
      // reg_debug_2 = iterator;
        if (*((unsigned short *) 0x00000000+iterator) != 0xAAAA){
            // reg_debug_2 = iterator;
            reg_debug_1 = 0x1E; 
            return;
        }
    }
    
    reg_debug_1 = 0x1B;
}