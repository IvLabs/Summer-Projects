`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 30.10.2025 19:03:10
// Design Name: 
// Module Name: filter1
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


module contrast(
    input wire [0:4]switch,
    input wire [0:3]r,
    input wire [0:3]g,
    input wire [0:3]b,
    output wire [0:3]R,
    output wire [0:3]G,
    output wire [0:3]B
    );
    RGB rgb1(.switch_r(switch[2]),.switch_g(switch[3]),.switch_b(switch[4]),.switch(switch[0:1]),.r(r),.g(g),.b(b),.R(R),.G(G),.B(B));
endmodule
