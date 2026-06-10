`timescale 1ns / 1ps
// This modules expects pixel data from UART in format PPPP0000
// Takes three consecutive RxBytes' useful half , combines them to form one 12 bit pixel to be stored in BRAM
module Pixel_Compiler (
    input  wire       clk_100MHz,
    input  wire       reset,
    input  wire       o_RX_DV,       // pulse when UART byte ready
    input  wire [7:0] RxByte,        // incoming byte
    output reg  [11:0] pixel_data,   // {R[11:8], G[7:4], B[3:0]}
    output reg        pixel_compiled // 1-cycle pulse when pixel ready
);

    reg [1:0] state; // 0->R,1->G,2->B
    reg [3:0] r4, g4, b4;

    always @(posedge clk_100MHz or posedge reset) begin
        if (reset) begin
            state <= 0;
            r4 <= 0; g4 <= 0; b4 <= 0;
            pixel_data <= 12'b0;
            pixel_compiled <= 1'b0;
        end else begin
            pixel_compiled <= 1'b0; // default
            if (o_RX_DV) begin
                case (state)
                    2'd0: begin
                        r4 <= RxByte[7:4];
                        state <= 2'd1;
                    end
                    2'd1: begin
                        g4 <= RxByte[7:4];
                        state <= 2'd2;
                    end
                    2'd2: begin
                        b4 <= RxByte[7:4];
                        pixel_data <= {r4, g4, b4};
                        pixel_compiled <= 1'b1;
                        state <= 2'd0;
                    end
                    default: state <= 2'd0;
                endcase
            end
        end
    end
endmodule
