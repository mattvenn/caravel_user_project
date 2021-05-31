`default_nettype none
`timescale 1ns/1ps
module frequency_counter #(
    // see calculations.py
    parameter UPDATE_PERIOD = 1200 - 1,
    parameter BITS = 12
)(
    input wire              clk,
    input wire              reset,
    input wire              signal,

    input wire [BITS-1:0]   period,
    input wire              period_load,

    output wire [6:0]       segments,
    output wire             digit
    );

    reg [BITS-1:0] update_period;   // measure incoming signal edges for this period

    reg [6:0] edge_counter;         // how many edges have arrived in the counting period, max can show is 99, so limit to 7 bits
    reg [BITS-1:0] clk_counter;     // keep track of clocks in the counting period

    reg [3:0] ten_count, unit_count;
    reg update_digits;

    wire leading_edge_detect;

    edge_detect edge_detect0 (.clk(clk), .signal(signal), .leading_edge_detect(leading_edge_detect));

    always @(posedge clk) begin
        if(reset)
            update_period   <= UPDATE_PERIOD;
        else if(period_load)
            update_period   <= period;
    end

    localparam STATE_COUNT  = 0;
    localparam STATE_TENS   = 1;
    localparam STATE_UNITS  = 2;

    reg [2:0] state;

    always @(posedge clk) begin
        if(reset) begin

            clk_counter     <= 0;
            edge_counter    <= 0;
            state           <= STATE_COUNT;
            ten_count       <= 0;
            unit_count      <= 0;
            update_digits   <= 0;

        end else begin
            case(state)
                STATE_COUNT: begin
                    update_digits   <= 0;
                    clk_counter <= clk_counter + 1'b1;

                    if(leading_edge_detect)
                        edge_counter <= edge_counter + 1'b1;

                    if(clk_counter >= update_period) begin
                        clk_counter <= 0;
                        ten_count   <= 0;
                        unit_count  <= 0;
                        state       <= STATE_TENS;
                    end
                end

                STATE_TENS: begin
                    if(edge_counter < 7'd10)
                        state <= STATE_UNITS;
                    else begin
                        edge_counter <= edge_counter - 7'd10;
                        ten_count   <= ten_count + 1;
                    end
                end

                STATE_UNITS: begin
                    unit_count      <= edge_counter;
                    update_digits   <= 1'b1;
                    edge_counter    <= 0;
                    state           <= STATE_COUNT;
                end

                default:
                    state           <= STATE_COUNT;

            endcase
        end
    end

    seven_segment seven_segment0 (.clk(clk), .reset(reset), .load(update_digits), .ten_count(ten_count), .unit_count(unit_count), .segments(segments), .digit(digit));

endmodule
