#include <firmware_apis.h>


int main(){
    enable_debug();
    unsigned int j = 0x77;
    set_debug_reg1(0x66);
    set_debug_reg1(j);
    // set_debug_reg1(1);
    // set_debug_reg1(j);
    // set_debug_reg1(1);
    // set_debug_reg1(j);
    // (*(volatile uint32_t*)0x0 ) = 0x11; 
    // (*(volatile uint32_t*)0x4 ) = 0x17; 
    // (*(volatile uint32_t*)0x4 ) = 0x17; 
    // (*(volatile uint32_t*)0x8 ) = (*(volatile uint32_t*)0x4 ); 
    // (*(volatile uint32_t*)0x4 ) = 0x17; 
    // (*(volatile uint32_t*)0x4 ) = 0x17; 
    // (*(volatile uint32_t*)0x4 ) = 0x17; 
    // (*(volatile uint32_t*)0x4 ) = 0x17; 
    // (*(volatile uint32_t*)0x4 ) = 0x17; 
    // (*(volatile uint32_t*)0x4 ) = 0x88888888; 
    // (*(volatile uint32_t*)0x4 ) = 0x17; 
    // (*(volatile uint32_t*)0x4 ) = 0x17; 
    // (*(volatile uint32_t*)0x4 ) = 0x17; 
    // (*(volatile uint32_t*)0x4 ) = 0x17; 
    // (*(volatile uint32_t*)0x4 ) = 0x17; 
    // (*(volatile uint32_t*)0x4 ) = 0x17; 
    // (*(volatile uint32_t*)0x2 ) = 0x14; 

    return 0;
}