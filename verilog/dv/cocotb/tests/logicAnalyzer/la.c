
#include <common.h>


/*
user exmple
assign la0 to la1 if la0 output enable
assign la1 to la0 if la1 output enable
assign la2 to la3 if la2 output enable
assign la3 to la2 if la3 output enable
*/
void main(){
    enable_debug();
    enable_hk_spi(0);

    // Configure LA probes [63:32] and [127:96] as inputs to the cpu 
	// Configure LA probes [31:0] and [63:32] as outputs from the cpu
    // 0 as input
    set_la_ien(0,0xFFFFFFFF);
    set_la_oen(0,0x0);
    // 1 as output 
    set_la_ien(1,0x0);
    set_la_oen(1,0xFFFFFFFF);
    // 2 as input
    set_la_ien(2,0xFFFFFFFF);
    set_la_oen(2,0x0);
    // 3 as output 
    set_la_ien(3,0x0);
    set_la_oen(3,0xFFFFFFFF);
    // set LA 0,2
    set_la_reg(0,0xAAAAAAAA);
    set_la_reg(2,0xAAAAAAAA);

    #if LA_SIZE >= 64
    set_debug_reg2(get_la_reg(1));
    if (get_la_reg(1) != 0xAAAAAAAA)
        set_debug_reg1(0x1E);
    else 
        set_debug_reg1(0x1B);
    #endif

    #if LA_SIZE >= 128
    set_debug_reg2(get_la_reg(3));
    if (get_la_reg(3) != 0xAAAAAAAA)
        set_debug_reg1(0x2E);
    else 
        set_debug_reg1(0x2B);   
    #endif

    // set LA 0,2
    set_la_reg(0,0x55555555);
    set_la_reg(2,0x55555555);
    
    #if LA_SIZE >= 64
    set_debug_reg2(get_la_reg(1));
    if (get_la_reg(1) != 0x55555555)
        set_debug_reg1(0x3E);
    else 
        set_debug_reg1(0x3B);
    #endif

    #if LA_SIZE >= 128
    set_debug_reg2(get_la_reg(3));
    if (get_la_reg(3) != 0x55555555)
        set_debug_reg1(0x4E);
    else 
        set_debug_reg1(0x4B);    
    #endif
    // Configure LA probes [31:0] and [63:32] as inputs to the cpu 
	// Configure LA probes [63:32] and [127:96] as outputs from the cpu
    // 0 as output
    set_la_ien(0,0x0);
    set_la_oen(0,0xFFFFFFFF);
    // 1 as input 
    set_la_ien(1,0xFFFFFFFF);
    set_la_oen(1,0x0);
    // 2 as output
    set_la_ien(2,0x0);
    set_la_oen(2,0xFFFFFFFF);
    // 3 as input 
    set_la_ien(3,0xFFFFFFFF);
    set_la_oen(3,0x0);

    // set LA 1,3
    set_la_reg(1,0xAAAAAAAA);
    set_la_reg(3,0xAAAAAAAA);

    #if LA_SIZE >= 64
    set_debug_reg2(get_la_reg(0));
    if (get_la_reg(0) != 0xAAAAAAAA)
        set_debug_reg1(0x5E);
    else 
        set_debug_reg1(0x5B);
    #endif
    #if LA_SIZE >= 128
    set_debug_reg2(get_la_reg(2));
    if (get_la_reg(2) != 0xAAAAAAAA)
        set_debug_reg1(0x6E);
    else 
        set_debug_reg1(0x6B);    
    #endif

    set_la_reg(1,0x55555555);
    set_la_reg(3,0x55555555);
    #if LA_SIZE >= 64
    set_debug_reg2(get_la_reg(0));
    if (get_la_reg(0) != 0x55555555)
        set_debug_reg1(0x7E);
    else 
        set_debug_reg1(0x7B);
    #endif

    #if LA_SIZE >= 128
    set_debug_reg2(get_la_reg(2));
    if (get_la_reg(2) != 0x55555555)
        set_debug_reg1(0x8E);
    else 
        set_debug_reg1(0x8B);    
    #endif

    
    set_debug_reg2(0xFF);
    
    dummy_delay(100000000);
    
}
