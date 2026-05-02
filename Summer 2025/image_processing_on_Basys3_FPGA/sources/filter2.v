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


module grayscale(
    input [0:1]switch,
    input [0:3]r,
    input [0:3]g,
    input [0:3]b,
    output reg [0:3]R,
    output reg [0:3]G,
    output reg [0:3]B 
    );
    integer gray;
    wire [0:3]R3,G3,B3,R4,G4,B4;
    assign R3=r;
    assign G3=g;
    assign B3=b;
    inversion i1(.switch(switch[1]),.r(R3),.g(G3),.b(B3),.R(R4),.G(G4),.B(B4));
    always @(*)begin
            gray=(R4+G4+B4)/3;
            R =(switch[0] ? gray : R4);  // if switch is on use filtered RGB values else the raw ones
            G =(switch[0] ? gray : G4);
            B =(switch[0] ? gray: B4);
    end
endmodule
