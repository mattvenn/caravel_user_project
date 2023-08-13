
#include <firmware_apis.h>


/*
user exmple
assign la0 to la1 if la0 output enable
assign la1 to la0 if la1 output enable
assign la2 to la3 if la2 output enable
assign la3 to la2 if la3 output enable
*/
void main(){
    enable_debug();
    enableHkSpi(0);

    // Configure LA probes [63:32] and [127:96] as inputs to the cpu 
	// Configure LA probes [31:0] and [63:32] as outputs from the cpu
    // 0 as input
    LogicAnalyzer_inputEnable(0,0xFFFFFFFF);
    LogicAnalyzer_outputEnable(0,0x0);
    // 1 as output 
    LogicAnalyzer_inputEnable(1,0x0);
    LogicAnalyzer_outputEnable(1,0xFFFFFFFF);
    // 2 as input
    LogicAnalyzer_inputEnable(2,0xFFFFFFFF);
    LogicAnalyzer_outputEnable(2,0x0);
    // 3 as output 
    LogicAnalyzer_inputEnable(3,0x0);
    LogicAnalyzer_outputEnable(3,0xFFFFFFFF);
    // set LA 0,2
    LogicAnalyzer_write(0,0xAAAAAAAA);
    LogicAnalyzer_write(2,0xAAAAAAAA);

    #if LA_SIZE >= 64
    set_debug_reg2(LogicAnalyzer_read(1));
    if (LogicAnalyzer_read(1) != 0xAAAAAAAA)
        set_debug_reg1(0x1E);
    else 
        set_debug_reg1(0x1B);
    #endif

    #if LA_SIZE >= 128
    set_debug_reg2(LogicAnalyzer_read(3));
    if (LogicAnalyzer_read(3) != 0xAAAAAAAA)
        set_debug_reg1(0x2E);
    else 
        set_debug_reg1(0x2B);   
    #endif

    // set LA 0,2
    LogicAnalyzer_write(0,0x55555555);
    LogicAnalyzer_write(2,0x55555555);
    
    #if LA_SIZE >= 64
    set_debug_reg2(LogicAnalyzer_read(1));
    if (LogicAnalyzer_read(1) != 0x55555555)
        set_debug_reg1(0x3E);
    else 
        set_debug_reg1(0x3B);
    #endif

    #if LA_SIZE >= 128
    set_debug_reg2(LogicAnalyzer_read(3));
    if (LogicAnalyzer_read(3) != 0x55555555)
        set_debug_reg1(0x4E);
    else 
        set_debug_reg1(0x4B);    
    #endif

    // to make sure all transations from 1 to 0 happen
    LogicAnalyzer_write(0,0xAAAAAAAA);
    LogicAnalyzer_write(2,0xAAAAAAAA);
    
    #if LA_SIZE >= 64
    set_debug_reg2(LogicAnalyzer_read(1));
    if (LogicAnalyzer_read(1) != 0xAAAAAAAA)
        set_debug_reg1(0x5E);
    else 
        set_debug_reg1(0x5B);
    #endif

    #if LA_SIZE >= 128
    set_debug_reg2(LogicAnalyzer_read(3));
    if (LogicAnalyzer_read(3) != 0xAAAAAAAA)
        set_debug_reg1(0x6E);
    else 
        set_debug_reg1(0x6B);    
    #endif
    // Configure LA probes [31:0] and [63:32] as inputs to the cpu 
	// Configure LA probes [63:32] and [127:96] as outputs from the cpu
    // 0 as output
    LogicAnalyzer_inputEnable(0,0x0);
    LogicAnalyzer_outputEnable(0,0xFFFFFFFF);
    // 1 as input 
    LogicAnalyzer_inputEnable(1,0xFFFFFFFF);
    LogicAnalyzer_outputEnable(1,0x0);
    // 2 as output
    LogicAnalyzer_inputEnable(2,0x0);
    LogicAnalyzer_outputEnable(2,0xFFFFFFFF);
    // 3 as input 
    LogicAnalyzer_inputEnable(3,0xFFFFFFFF);
    LogicAnalyzer_outputEnable(3,0x0);

    // set LA 1,3
    LogicAnalyzer_write(1,0xAAAAAAAA);
    LogicAnalyzer_write(3,0xAAAAAAAA);

    #if LA_SIZE >= 64
    set_debug_reg2(LogicAnalyzer_read(0));
    if (LogicAnalyzer_read(0) != 0xAAAAAAAA)
        set_debug_reg1(0x7E);
    else 
        set_debug_reg1(0x7B);
    #endif
    #if LA_SIZE >= 128
    set_debug_reg2(LogicAnalyzer_read(2));
    if (LogicAnalyzer_read(2) != 0xAAAAAAAA)
        set_debug_reg1(0x8E);
    else 
        set_debug_reg1(0x8B);    
    #endif

    LogicAnalyzer_write(1,0x55555555);
    LogicAnalyzer_write(3,0x55555555);
    #if LA_SIZE >= 64
    set_debug_reg2(LogicAnalyzer_read(0));
    if (LogicAnalyzer_read(0) != 0x55555555)
        set_debug_reg1(0x9E);
    else 
        set_debug_reg1(0x9B);
    #endif

    #if LA_SIZE >= 128
    set_debug_reg2(LogicAnalyzer_read(2));
    if (LogicAnalyzer_read(2) != 0x55555555)
        set_debug_reg1(0xaE);
    else 
        set_debug_reg1(0xaB);    
    #endif

    // to make sure all transations from 1 to 0 happen
    LogicAnalyzer_write(1,0xAAAAAAAA);
    LogicAnalyzer_write(3,0xAAAAAAAA);
    #if LA_SIZE >= 64
    set_debug_reg2(LogicAnalyzer_read(0));
    if (LogicAnalyzer_read(0) != 0xAAAAAAAA)
        set_debug_reg1(0xbE);
    else 
        set_debug_reg1(0xbB);
    #endif

    #if LA_SIZE >= 128
    set_debug_reg2(LogicAnalyzer_read(2));
    if (LogicAnalyzer_read(2) != 0xAAAAAAAA)
        set_debug_reg1(0xcE);
    else 
        set_debug_reg1(0xcB);    
    #endif

    
    set_debug_reg2(0xFF);
    
    dummyDelay(100000000);
    
}
