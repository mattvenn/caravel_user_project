// module that has registers used for debug
module debug_regs (    
    input wb_clk_i,
    input wb_rst_i,
    input wbs_stb_i,
    input wbs_cyc_i,
    input wbs_we_i,
    input [3:0] wbs_sel_i,
    input [31:0] wbs_dat_i,
    input [31:0] wbs_adr_i,
    output reg wbs_ack_o,
    output reg [31:0] wbs_dat_o);

    reg [31:0] debug_reg_1;
    reg [31:0] debug_reg_2;

    // write
    always @(posedge wb_clk_i or posedge wb_rst_i) begin
        if (wb_rst_i) begin
            debug_reg_1 <=0;
            debug_reg_2 <=0;
            wbs_dat_o   <=0;
            wbs_ack_o   <=0;
        end else if (wbs_cyc_i && wbs_stb_i && wbs_we_i && !wbs_ack_o && (wbs_adr_i[3:0]==4'hC||wbs_adr_i[3:0]==4'h8))begin // write
            // write to reg1
            debug_reg_1[7:0]    <= ((wbs_adr_i[3:0]==4'h8) && wbs_sel_i[0])?  wbs_dat_i[7:0]   :debug_reg_1[7:0];
            debug_reg_1[15:8]   <= ((wbs_adr_i[3:0]==4'h8) && wbs_sel_i[1])?  wbs_dat_i[15:8]  :debug_reg_1[15:8];
            debug_reg_1[23:16]  <= ((wbs_adr_i[3:0]==4'h8) && wbs_sel_i[2])?  wbs_dat_i[23:16] :debug_reg_1[23:16];
            debug_reg_1[31:24]  <= ((wbs_adr_i[3:0]==4'h8) && wbs_sel_i[3])?  wbs_dat_i[31:24] :debug_reg_1[31:24];
            // write to reg2
            debug_reg_2[7:0]    <= ((wbs_adr_i[3:0]==4'hC) && wbs_sel_i[0])?  wbs_dat_i[7:0]   :debug_reg_2[7:0];
            debug_reg_2[15:8]   <= ((wbs_adr_i[3:0]==4'hC) && wbs_sel_i[1])?  wbs_dat_i[15:8]  :debug_reg_2[15:8];
            debug_reg_2[23:16]  <= ((wbs_adr_i[3:0]==4'hC) && wbs_sel_i[2])?  wbs_dat_i[23:16] :debug_reg_2[23:16];
            debug_reg_2[31:24]  <= ((wbs_adr_i[3:0]==4'hC) && wbs_sel_i[3])?  wbs_dat_i[31:24] :debug_reg_2[31:24];
            wbs_ack_o <= 1;
        end else if (wbs_cyc_i && wbs_stb_i && !wbs_we_i && !wbs_ack_o && (wbs_adr_i[3:0]==4'hC||wbs_adr_i[3:0]==4'h8)) begin // read 
            wbs_dat_o <= ((wbs_adr_i[3:0]==4'hC)) ? debug_reg_2 : debug_reg_1; 
            wbs_ack_o <= 1;
        end else begin 
            wbs_ack_o <= 0;
            wbs_dat_o <= 0;
        end
    end
endmodule

// model used for ARM AHB interface only
`ifdef AHB 
module AHB_DEBUG_REGS ( 
    input   wire            HCLK,
    input   wire            HRESETn,
    input   wire            HSEL,
    input   wire [31:0]     HADDR,
    input   wire [1:0]      HTRANS,
    input   wire [31:0]     HWDATA,
    input   wire            HWRITE,
    input   wire            HREADY,
    output  wire [31:0]     HRDATA);
    
    // regs offset
    localparam [23:0]       DEBUG_REG1_OFF      = 24'hFFFFFC,
                            DEBUG_REG2_OFF      = 24'hFFFFF8;

    `AHB_SLAVE_EPILOGUE()

    // AHB Register
    `define AHB_DEBUG_REG(name, size, offset, init, prefix)   \
        reg [size-1:0] name; \
        wire ``name``_sel = wr_enable & (last_HADDR[23:0] == offset); \
        always @(posedge HCLK or negedge HRESETn) \
            if (~HRESETn) \
                ``name`` <= 'h``init``; \
            else if (``name``_sel) \
                ``name`` <= ``prefix``HWDATA[``size``-1:0];\

    `define AHB_DEBUG_REG_READ(name, offset) (last_HADDR[23:0] == offset) ? name : 

    // AHB_REG(name, size, offset, init, prefix);
    `AHB_DEBUG_REG(debug_reg_1, 32, DEBUG_REG1_OFF, 0, )
    `AHB_DEBUG_REG(debug_reg_2, 32, DEBUG_REG2_OFF, 0, )

    // assign HREADYOUT = 1'b1;

    assign HRDATA[31:0] =   `AHB_DEBUG_REG_READ(debug_reg_1, DEBUG_REG1_OFF) 
                            `AHB_DEBUG_REG_READ(debug_reg_2, DEBUG_REG2_OFF) 
                            32'h0 ;
endmodule

`endif
`default_nettype wire