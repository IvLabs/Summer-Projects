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


module RGB(
    input switch_r,
    input switch_g,
    input switch_b,
    input [0:1]switch,
    input [0:3]r,
    input [0:3]g,
    input [0:3]b,
    output reg [0:3]R,
    output reg [0:3]G,
    output reg [0:3]B
    );
    wire [0:3]R2,G2,B2,R3,G3,B3,R4,G4,B4;
    assign R2=r;
    assign G2=g;
    assign B2=b;
    grayscale g1(.switch(switch[0:1]),.r(R3),.g(G3),.b(B3),.R(R4),.G(G4),.B(B4));

    assign R3 =(switch_r ? 0: R2);  // if switch is on use filtered RGB values else the raw ones
    assign G3 =(switch_g ? 0: G2);
    assign B3 =(switch_b ? 0: B2);
    
    always @(*)begin
        R =R4;  // if switch is on use filtered RGB values else the raw ones
        G =G4;
        B =B4;
    end
endmodule
