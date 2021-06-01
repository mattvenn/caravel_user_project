`timescale 1 ns / 1 ps

//
// Simple SPI simulation model
//
// This model is roughly supposed to mimic a Digilent MIC3 PMOD
// board.  It samples a value when CSB goes low, and outputs a
// 12-bit value on 16 clock cycles, with SDO always zero on the
// last four clocks.
//
// Note that sdi is unused.

module spi_test (
	input  csb,
	input  clk,
	input  sdi,
	output sdo
);
	integer bitcount = 0;
	integer bytecount = 0;

	reg [7:0] spi_out;

	reg sdo_oe = 0;
	reg sdo_dout = 0;

	reg [15:0] value;

	assign #1 sdo = sdo_oe ? sdo_dout : 1'bz;

	initial begin
		value <= 0;
	end

	always @(csb) begin
		if (csb) begin
			bitcount = 0;
			bytecount = 0;
			sdo_oe = 0;
		end else begin
			sdo_oe = 1;
		end
	end

	always @(csb, clk) begin
		if (!csb && !clk) begin
			sdo_dout = value[15];
		end
	end

	always @(posedge clk) begin
		if (!csb) begin
			value = {value[14:0], value[15]};
			bitcount = bitcount + 1;
			if (bitcount == 8) begin
				bitcount = 0;
				bytecount = bytecount + 1;
				if (bytecount == 2) begin
					value <= value + 3;
					bytecount = 0;
				end
			end
		end
	end
endmodule
