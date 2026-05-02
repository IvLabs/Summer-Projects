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


module inversion(
    input switch,
    input [0:3]r,
    input [0:3]g,
    input [0:3]b,
    output reg [0:3]R,
    output reg [0:3]G,
    output reg [0:3]B
    );
    always @(*)begin
            R =(switch ? 15-r : r);  // if switch is on use filtered RGB values else the raw ones
            G =(switch ? 15-g : g);
            B =(switch ? 15-b : b);
    end
endmodule
