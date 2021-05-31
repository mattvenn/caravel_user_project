`default_nettype none
`timescale 1ns/1ps
module edge_detect (
    input wire              clk,
    input wire              signal,
    output wire             leading_edge_detect
    );

    reg q0, q1, q2;                 // metastability on input and a delay to detect edges

    always @(posedge clk) begin
        q0 <= signal;
        q1 <= q0;
        q2 <= q1;
    end

    assign leading_edge_detect = q1 & (q2 != q1);

endmodule
