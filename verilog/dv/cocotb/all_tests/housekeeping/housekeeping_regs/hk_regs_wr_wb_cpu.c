#include <firmware_apis.h>



// access all housekeeping registers that can be access through firmware and change it's value
void main(){
    enable_debug();
    enableHkSpi(0);
    // store RO value regs 
    int old_reg_hkspi_status = reg_hkspi_status;
    int old_reg_hkspi_chip_id = reg_hkspi_chip_id;
    int old_reg_hkspi_user_id = reg_hkspi_user_id;
    #if TRAP_SUP
    int old_reg_hkspi_trap = reg_hkspi_trap;
    #endif
    int old_reg_hkspi_irq = reg_hkspi_irq;
    unsigned int data_in = 0x55555555;
    // write 10 ones to all registers
    wr_all_gpio_ctrl_regs(data_in);
    // house keeping 
    reg_hkspi_status     = data_in;   
    reg_hkspi_chip_id    = data_in;   
    reg_hkspi_user_id    = data_in;    
    #if PLL_SUP
    reg_hkspi_pll_ena    = data_in;   
    reg_hkspi_pll_bypass = data_in; 
    #endif //pll sup
    reg_hkspi_irq 	     = data_in; 
    // reg_hkspi_reset   = data_in;   can't write 1 to it cpu would be reset
    #if TRAP_SUP
    reg_hkspi_trap 	     = data_in; 
    #endif
    reg_hkspi_pll_trim   = data_in; 
    reg_hkspi_pll_source = data_in;  
    reg_hkspi_pll_divider= data_in;
    // sys 
    reg_clk_out_dest     =  data_in;
    reg_hkspi_disable    =  data_in; 

    // read ones that has been written
    check_all_gpio_ctrl_regs(data_in);
    // housekeeping
    if (reg_hkspi_status!= old_reg_hkspi_status) // RO
        set_debug_reg1(0x27);
    if (reg_hkspi_chip_id!= old_reg_hkspi_chip_id) // RO
        set_debug_reg1(0x28);
    if (reg_hkspi_user_id!= old_reg_hkspi_user_id) // RO
        set_debug_reg1(0x29);
    #if PLL_SUP
    if (reg_hkspi_pll_ena!= 0x1)  // size =2
        set_debug_reg1(0x2a);
    if (reg_hkspi_pll_bypass != 0x1) // size = 1
        set_debug_reg1(0x2b);
    #endif //pll sup
    if (reg_hkspi_irq!= old_reg_hkspi_irq)  // RO
        set_debug_reg1(0x2c);
    #if TRAP_SUP
    if (reg_hkspi_trap!= old_reg_hkspi_trap)  // RO
        set_debug_reg1(0x2d);
    #endif
    if (reg_hkspi_pll_trim!= 0x1555555) // size 26
        set_debug_reg1(0x2f);
    if (reg_hkspi_pll_source!= 0x15) // size 6 bits 0-2 = phase 0 divider, bits 3-5 = phase 90 divider
        set_debug_reg1(0x2f);
    if (reg_hkspi_pll_divider!= 0x15) // size 5 -> PLL output divider, PLL output divider2 , PLL feedback divider
        set_debug_reg1(0x30);
    if (reg_hkspi_disable!= 0x1) // size 1
        set_debug_reg1(0x31);
    if (reg_clk_out_dest!= 0x5) // trap and clocks redirect
        set_debug_reg1(0x32);
    // // write 01 to all registers
    data_in = 0xAAAAAAAA;
    wr_all_gpio_ctrl_regs(data_in);
    // house keeping 
    reg_hkspi_status     = data_in;   
    reg_hkspi_chip_id    = data_in;   
    reg_hkspi_user_id    = data_in;    
    #if PLL_SUP
    reg_hkspi_pll_ena    = data_in;   
    reg_hkspi_pll_bypass = data_in; 
    #endif // pll sup
    reg_hkspi_irq 	     = data_in; 
    reg_hkspi_reset      = data_in;  
    #if TRAP_SUP
    reg_hkspi_trap 	     = data_in; 
    #endif // TRAP_SUP
    reg_hkspi_pll_trim   = data_in; 
    reg_hkspi_pll_source = data_in;  
    reg_hkspi_pll_divider= data_in;
    // sys 
    reg_clk_out_dest     = data_in; 
    reg_hkspi_disable    = data_in; 

    // // read zeros that has been written
    check_all_gpio_ctrl_regs(data_in);
    
    
        // housekeeping
    if (reg_hkspi_status!= old_reg_hkspi_status) // RO
        set_debug_reg2(0x27);
    if (reg_hkspi_chip_id!= old_reg_hkspi_chip_id) // RO
        set_debug_reg2(0x28);
    if (reg_hkspi_user_id!= old_reg_hkspi_user_id) // RO
        set_debug_reg2(0x29);
    #if PLL_SUP
    if (reg_hkspi_pll_ena!= 0x2)  // size =2
        set_debug_reg2(0x2a);
    if (reg_hkspi_pll_bypass != 0x0) // size = 1
        set_debug_reg2(0x2b);
    if (reg_hkspi_irq!= old_reg_hkspi_irq)  // RO
        set_debug_reg2(0x2c);
    #endif // pll sup
    #if TRAP_SUP
    if (reg_hkspi_trap!= old_reg_hkspi_trap)  // RO
        set_debug_reg2(0x2d);
    #endif
    if (reg_hkspi_pll_trim!= 0x2AAAAAA) // size 26
        set_debug_reg2(0x2f);
    if (reg_hkspi_pll_source!= 0x2A) // size 6 bits 0-2 = phase 0 divider, bits 3-5 = phase 90 divider
        set_debug_reg2(0x2f);
    if (reg_hkspi_pll_divider!= 0xA)// size 5 -> PLL output divider, PLL output divider2 , PLL feedback divider
        set_debug_reg2(0x30);
    if (reg_hkspi_disable!= 0x0) // size 1
        set_debug_reg2(0x31);
    if (reg_clk_out_dest!= 0x2) // trap and clocks redirect
        set_debug_reg2(0x32);

    set_debug_reg2(0xFF);
}

void wr_all_gpio_ctrl_regs(unsigned int data_in){
    reg_mprj_io_0   = data_in;
    reg_mprj_io_1   = data_in;
    reg_mprj_io_2   = data_in;
    reg_mprj_io_3   = data_in;
    reg_mprj_io_4   = data_in;
    reg_mprj_io_5   = data_in;
    reg_mprj_io_6   = data_in;
    reg_mprj_io_7   = data_in;
    reg_mprj_io_8   = data_in;
    reg_mprj_io_9   = data_in;
    reg_mprj_io_10  = data_in;
    reg_mprj_io_11  = data_in;
    reg_mprj_io_12  = data_in;
    reg_mprj_io_13  = data_in;
    reg_mprj_io_14  = data_in;
    reg_mprj_io_15  = data_in;
    reg_mprj_io_16  = data_in;
    reg_mprj_io_17  = data_in;
    reg_mprj_io_18  = data_in;
    reg_mprj_io_19  = data_in;
    reg_mprj_io_20  = data_in;
    reg_mprj_io_21  = data_in;
    reg_mprj_io_22  = data_in;
    reg_mprj_io_23  = data_in;
    reg_mprj_io_24  = data_in;
    reg_mprj_io_25  = data_in;
    reg_mprj_io_26  = data_in;
    reg_mprj_io_27  = data_in;
    reg_mprj_io_28  = data_in;
    reg_mprj_io_29  = data_in;
    reg_mprj_io_30  = data_in;
    reg_mprj_io_31  = data_in;
    reg_mprj_io_32  = data_in;
    reg_mprj_io_33  = data_in;
    reg_mprj_io_34  = data_in;
    reg_mprj_io_35  = data_in;
    reg_mprj_io_36  = data_in;
    reg_mprj_io_37  = data_in;
}
void check_all_gpio_ctrl_regs(unsigned int data_in){
    unsigned int mask = 0;
    for (int i = 0; i < CTRL_BITS_SIZE; i++){
        mask = mask << 1;
        mask = mask | 0x1;
    }
    unsigned int data_exp = data_in & mask;
    if (reg_mprj_io_0 != data_exp)
        set_debug_reg1(0x1);
    if (reg_mprj_io_1 != data_exp)
        set_debug_reg1(0x2);
    if (reg_mprj_io_2 != data_exp)
        set_debug_reg1(0x3);
    if (reg_mprj_io_3 != data_exp)
        set_debug_reg1(0x4);
    if (reg_mprj_io_4 != data_exp)
        set_debug_reg1(0x5);
    if (reg_mprj_io_5 != data_exp)
        set_debug_reg1(0x6);
    if (reg_mprj_io_6 != data_exp)
        set_debug_reg1(0x7);
    if (reg_mprj_io_7 != data_exp)
        set_debug_reg1(0x8);
    if (reg_mprj_io_8 != data_exp)
        set_debug_reg1(0x9);
    if (reg_mprj_io_9 != data_exp)
        set_debug_reg1(0xa);
    if (reg_mprj_io_10!= data_exp)
        set_debug_reg1(0xb);
    if (reg_mprj_io_11!= data_exp)
        set_debug_reg1(0xc);
    if (reg_mprj_io_12!= data_exp)
        set_debug_reg1(0xd);
    if (reg_mprj_io_13!= data_exp)
        set_debug_reg1(0xe);
    if (reg_mprj_io_14!= data_exp)
        set_debug_reg1(0xf);
    if (reg_mprj_io_15!= data_exp)
        set_debug_reg1(0x10);
    if (reg_mprj_io_16!= data_exp)
        set_debug_reg1(0x11);
    if (reg_mprj_io_17!= data_exp)
        set_debug_reg1(0x12);
    if (reg_mprj_io_18!= data_exp)
        set_debug_reg1(0x13);
    if (reg_mprj_io_19!= data_exp)
        set_debug_reg1(0x14);
    if (reg_mprj_io_20!= data_exp)
        set_debug_reg1(0x15);
    if (reg_mprj_io_21!= data_exp)
        set_debug_reg1(0x16);
    if (reg_mprj_io_22!= data_exp)
        set_debug_reg1(0x17);
    if (reg_mprj_io_23!= data_exp)
        set_debug_reg1(0x18);
    if (reg_mprj_io_24!= data_exp)
        set_debug_reg1(0x19);
    if (reg_mprj_io_25!= data_exp)
        set_debug_reg1(0x1a);
    if (reg_mprj_io_26!= data_exp)
        set_debug_reg1(0x1b);
    if (reg_mprj_io_27!= data_exp)
        set_debug_reg1(0x1c);
    if (reg_mprj_io_28!= data_exp)
        set_debug_reg1(0x1d);
    if (reg_mprj_io_29!= data_exp)
        set_debug_reg1(0x1e);
    if (reg_mprj_io_30!= data_exp)
        set_debug_reg1(0x1f);
    if (reg_mprj_io_31!= data_exp)
        set_debug_reg1(0x20);
    if (reg_mprj_io_32!= data_exp)
        set_debug_reg1(0x21);
    if (reg_mprj_io_33!= data_exp)
        set_debug_reg1(0x22);
    if (reg_mprj_io_34!= data_exp)
        set_debug_reg1(0x23);
    if (reg_mprj_io_35!= data_exp)
        set_debug_reg1(0x24);
    if (reg_mprj_io_36!= data_exp)
        set_debug_reg1(0x25);
    if (reg_mprj_io_37!= data_exp)
        set_debug_reg1(0x26);
}