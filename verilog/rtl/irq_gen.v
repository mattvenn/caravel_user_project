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
 * IRQ demo
            la_data_in[16] : load data to counter
 *
 *-------------------------------------------------------------
 */

module irq_gen (
`ifdef USE_POWER_PINS
    inout vdda1,	// User area 1 3.3V supply
    inout vdda2,	// User area 2 3.3V supply
    inout vssa1,	// User area 1 analog ground
    inout vssa2,	// User area 2 analog ground
    inout vccd1,	// User area 1 1.8V supply
    inout vccd2,	// User area 2 1.8v supply
    inout vssd1,	// User area 1 digital ground
    inout vssd2,	// User area 2 digital ground
`endif
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

    // Logic Analyzer Signals
    input  [127:0] la_data_in,
    output [127:0] la_data_out,
    input  [127:0] la_oenb,

    // IOs
    input  [`MPRJ_IO_PADS-1:0] io_in,
    output [`MPRJ_IO_PADS-1:0] io_out,
    output [`MPRJ_IO_PADS-1:0] io_oeb,

    // IRQ
    output [2:0] irq
);

    reg [15:0] counter;
    wire clk = wb_clk_i;
    wire reset = wb_rst_i;
    reg interrupt;
    assign irq[0] = interrupt;

    localparam state_wait  = 0;
    localparam state_count = 1;
    localparam state_irq   = 2;

    reg [2:0] state = state_wait;

    always @(posedge clk) begin
        if(reset) begin
            counter <= 0;
            interrupt <= 0;
            state <= state_wait;
        end else begin
            // load data
            case(state)
                state_wait: begin
                    interrupt <= 0;
                    if(la_data_in[16]) begin
                        counter <= la_data_in[15:0];
                        state <= state_count;
                    end
                 end
                state_count: begin
                    counter <= counter - 1'b1; 
                    if(counter == 1'b1)
                        state <= state_irq;
                end

                state_irq: begin
                    interrupt <= 1'b1;
                    state <= state_wait;
                end

            endcase;
        end
    end
endmodule
`default_nettype wire
