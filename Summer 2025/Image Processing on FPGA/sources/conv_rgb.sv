`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 05.11.2025 17:56:07
// Design Name: 
// Module Name: conv_rgb
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module conv_rgb #(parameter M=320,N=240,
    // kernel
    parameter K00 = -1, K01 = -1, K02 = -1,
    parameter K10 = -1, K11 = 8, K12 = -1,
    parameter K20 = -1, K21 = -1, K22 = -1,
    parameter D=1
)(
    input wire clk,
    input wire switch,
    input wire rst,
    input wire [9:0]x,
    input wire [9:0]y,
    input wire [3:0]r,
    input wire [3:0]g,
    input wire [3:0]b,
    output wire [3:0]R,
    output wire [3:0]G,
    output wire [3:0]B
);
    wire [11:0]pix_in;
    wire [11:0]pix_out;
    assign pix_in[11:8]=r;
    assign R=pix_out[11:8];
    assign pix_in[7:4]=g;
    assign G=pix_out[7:4];
    assign pix_in[3:0]=b;
    assign B=pix_out[3:0];
    convolution #(.M(M),.N(N),.K00(K00),.K01(K01),.K02(K02),.K10(K10),.K11(K11),.K12(K12),.K20(K20),.K21(K21),.K22(K22),.D(D))
                    conv(.clk(clk),.switch(switch),.rst(rst),.x(x),.y(y),.pixel_in(pix_in),.pixel_out(pix_out));
endmodule
