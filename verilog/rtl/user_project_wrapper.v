// SPDX-FileCopyrightText: 2020 Efabless Corporation
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// SPDX-License-Identifier: Apache-2.0

`default_nettype none
/*
 *-------------------------------------------------------------
 *
 * user_project_wrapper
 *
 * This wrapper enumerates all of the pins available to the
 * user for the user project.
 *
 * An example user project is provided in this wrapper.  The
 * example should be removed and replaced with the actual
 * user project.
 *
 *-------------------------------------------------------------
 */

module user_project_wrapper #(
    parameter BITS = 32
)(
`ifdef USE_POWER_PINS
    `ifdef sky130
    inout vdda1,	// User area 1 3.3V supply
    inout vdda2,	// User area 2 3.3V supply
    inout vssa1,	// User area 1 analog ground
    inout vssa2,	// User area 2 analog ground
    inout vccd1,	// User area 1 1.8V supply
    inout vccd2,	// User area 2 1.8v supply
    inout vssd1,	// User area 1 digital ground
    inout vssd2,	// User area 2 digital ground
    `elsif gf180 // sky130
    inout vdd,	
    inout vss,	
    `endif //sky130
`endif
    `ifndef AHB
    // Wishbone Slave ports (WB MI A)
    input wb_clk_i,
    input wb_rst_i,
    input wbs_stb_i,
    input wbs_cyc_i,
    input wbs_we_i,
    input [3:0] wbs_sel_i,
    input [31:0] wbs_dat_i,
    input [31:0] wbs_adr_i,
    output wbs_ack_o,
    output [31:0] wbs_dat_o,
    `else // not AHB
    input  wire            HCLK,
    input  wire            HRESETn,
    input  wire            HSEL,
    input  wire [31:0]     HADDR,
    input  wire [31:0]     HWDATA,
    input  wire            HREADY,
    input  wire            HWRITE,
    input  wire [1:0]      HTRANS,
    input  wire [2:0]      HSIZE,
    output wire [31:0]     HRDATA,
    output wire            HREADYOUT,
    `endif // not AHB
    // Logic Analyzer Signals
    input  [127:0] la_data_in,
    output [127:0] la_data_out,
    input  [127:0] la_oenb,

    // IOs
    input  [`MPRJ_IO_PADS-1:0] io_in,
    output [`MPRJ_IO_PADS-1:0] io_out,
    output [`MPRJ_IO_PADS-1:0] io_oeb,

    // Analog (direct connection to GPIO pad---use with caution)
    // Note that analog I/O is not available on the 7 lowest-numbered
    // GPIO pads, and so the analog_io indexing is offset from the
    // GPIO indexing by 7 (also upper 2 GPIOs do not have analog_io).
    inout [`MPRJ_IO_PADS-10:0] analog_io,

    // Independent clock (on independent integer divider)
    input   user_clock2,

    // User maskable interrupt signals
    output [2:0] user_irq
);

wire irq0;
wire irq1;
wire irq2;

assign user_irq[0] = irq0;
assign user_irq[1] = irq1;
assign user_irq[2] = irq2;

wire io_out0; 
assign io_out[0] = io_out0;
wire io_out1; 
assign io_out[1] = io_out1;
wire io_out2; 
assign io_out[2] = io_out2;
wire io_out3; 
assign io_out[3] = io_out3;
wire io_out4; 
assign io_out[4] = io_out4;
wire io_out5; 
assign io_out[5] = io_out5;
wire io_out6; 
assign io_out[6] = io_out6;
wire io_out7; 
assign io_out[7] = io_out7;
wire io_out8;
assign io_out[8] = io_out8;
wire io_out9;
assign io_out[9] = io_out9;
wire io_out10;
assign io_out[10] = io_out10;
wire io_out11;
assign io_out[11] = io_out11;
wire io_out12;
assign io_out[12] = io_out12;
wire io_out13;
assign io_out[13] = io_out13;
wire io_out14;
assign io_out[14] = io_out14;
wire io_out15;
assign io_out[15] = io_out15;
wire io_out16;
assign io_out[16] = io_out16;
wire io_out17;
assign io_out[17] = io_out17;
wire io_out18;
assign io_out[18] = io_out18;
wire io_out19;
assign io_out[19] = io_out19;
wire io_out20;
assign io_out[20] = io_out20;
wire io_out21;
assign io_out[21] = io_out21;
wire io_out22;
assign io_out[22] = io_out22;
wire io_out23;
assign io_out[23] = io_out23;
wire io_out24;
assign io_out[24] = io_out24;
wire io_out25;
assign io_out[25] = io_out25;
wire io_out26;
assign io_out[26] = io_out26;
wire io_out27;
assign io_out[27] = io_out27;
wire io_out28;
assign io_out[28] = io_out28;
wire io_out29;
assign io_out[29] = io_out29;
wire io_out30;
assign io_out[30] = io_out30;
wire io_out31;
assign io_out[31] = io_out31;
wire io_out32;
assign io_out[32] = io_out32;
wire io_out33;
assign io_out[33] = io_out33;
wire io_out34;
assign io_out[34] = io_out34;
wire io_out35;
assign io_out[35] = io_out35;
wire io_out36;
assign io_out[36] = io_out36;
wire io_out37;
assign io_out[37] = io_out37;

wire io_oeb0;
assign io_oeb[0] = io_oeb0;
wire io_oeb1;
assign io_oeb[1] = io_oeb1;
wire io_oeb2;
assign io_oeb[2] = io_oeb2;
wire io_oeb3;
assign io_oeb[3] = io_oeb3;
wire io_oeb4;
assign io_oeb[4] = io_oeb4;
wire io_oeb5;
assign io_oeb[5] = io_oeb5;
wire io_oeb6;
assign io_oeb[6] = io_oeb6;
wire io_oeb7;
assign io_oeb[7] = io_oeb7;
wire io_oeb8;
assign io_oeb[8] = io_oeb8;
wire io_oeb9;
assign io_oeb[9] = io_oeb9;
wire io_oeb10;
assign io_oeb[10] = io_oeb10;
wire io_oeb11;
assign io_oeb[11] = io_oeb11;
wire io_oeb12;
assign io_oeb[12] = io_oeb12;
wire io_oeb13;
assign io_oeb[13] = io_oeb13;
wire io_oeb14;
assign io_oeb[14] = io_oeb14;
wire io_oeb15;
assign io_oeb[15] = io_oeb15;
wire io_oeb16;
assign io_oeb[16] = io_oeb16;
wire io_oeb17;
assign io_oeb[17] = io_oeb17;
wire io_oeb18;
assign io_oeb[18] = io_oeb18;
wire io_oeb19;
assign io_oeb[19] = io_oeb19;
wire io_oeb20;
assign io_oeb[20] = io_oeb20;
wire io_oeb21;
assign io_oeb[21] = io_oeb21;
wire io_oeb22;
assign io_oeb[22] = io_oeb22;
wire io_oeb23;
assign io_oeb[23] = io_oeb23;
wire io_oeb24;
assign io_oeb[24] = io_oeb24;
wire io_oeb25;
assign io_oeb[25] = io_oeb25;
wire io_oeb26;
assign io_oeb[26] = io_oeb26;
wire io_oeb27;
assign io_oeb[27] = io_oeb27;
wire io_oeb28;
assign io_oeb[28] = io_oeb28;
wire io_oeb29;
assign io_oeb[29] = io_oeb29;
wire io_oeb30;
assign io_oeb[30] = io_oeb30;
wire io_oeb31;
assign io_oeb[31] = io_oeb31;
wire io_oeb32;
assign io_oeb[32] = io_oeb32;
wire io_oeb33;
assign io_oeb[33] = io_oeb33;
wire io_oeb34;
assign io_oeb[34] = io_oeb34;
wire io_oeb35;
assign io_oeb[35] = io_oeb35;
wire io_oeb36;
assign io_oeb[36] = io_oeb36;
wire io_oeb37;
assign io_oeb[37] = io_oeb37;


endmodule	// user_project_wrapper
