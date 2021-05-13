module user_project_wrapper (user_clock2,
    wb_clk_i,
    wb_rst_i,
    wbs_ack_o,
    wbs_cyc_i,
    wbs_stb_i,
    wbs_we_i,
    vccd1,
    vssd1,
    vccd2,
    vssd2,
    vdda1,
    vssa1,
    vdda2,
    vssa2,
    analog_io,
    io_in,
    io_oeb,
    io_out,
    la_data_in,
    la_data_out,
    la_oenb,
    user_irq,
    wbs_adr_i,
    wbs_dat_i,
    wbs_dat_o,
    wbs_sel_i);
 input user_clock2;
 input wb_clk_i;
 input wb_rst_i;
 output wbs_ack_o;
 input wbs_cyc_i;
 input wbs_stb_i;
 input wbs_we_i;
 input vccd1;
 input vssd1;
 input vccd2;
 input vssd2;
 input vdda1;
 input vssa1;
 input vdda2;
 input vssa2;
 inout [28:0] analog_io;
 input [37:0] io_in;
 output [37:0] io_oeb;
 output [37:0] io_out;
 input [127:0] la_data_in;
 output [127:0] la_data_out;
 input [127:0] la_oenb;
 output [2:0] user_irq;
 input [31:0] wbs_adr_i;
 input [31:0] wbs_dat_i;
 output [31:0] wbs_dat_o;
 input [3:0] wbs_sel_i;

 rgb_mixer rgb_mixer (.clk(wb_clk_i),
    .enc0_a(io_in[8]),
    .enc0_b(io_in[9]),
    .enc1_a(io_in[10]),
    .enc1_b(io_in[11]),
    .enc2_a(io_in[12]),
    .enc2_b(io_in[13]),
    .out_en_b0(io_oeb[14]),
    .out_en_b1(io_oeb[15]),
    .out_en_b2(io_oeb[16]),
    .pwm0_out(io_out[14]),
    .pwm1_out(io_out[15]),
    .pwm2_out(io_out[16]),
    .reset(la_data_in[0]),
    .vccd1(vccd1),
    .vssd1(vssd1),
    .vccd2(vccd2),
    .vssd2(vssd2),
    .vdda1(vdda1),
    .vssa1(vssa1),
    .vdda2(vdda2),
    .vssa2(vssa2));
endmodule
