`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 28.07.2025 15:30:26
// Design Name: 
// Module Name: image_filter_8bit
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


module convolution #(parameter M=320,N=240,
    // kernel
    parameter K00 = -1, K01 = -1, K02 = -1,
    parameter K10 = -1, K11 = 8, K12 = -1,
    parameter K20 = -1, K21 = -1, K22 = -1,
    parameter D=1
)(
    input clk,
    input switch,
    input rst,
    input [9:0]x,
    input [9:0]y,
    input [11:0] pixel_in,
    output reg [11:0] pixel_out
);
    
    (* ram_style = "block" *) reg [11:0]  temp_y[0:2][0:M-1];
    integer temp_r=0,temp_g=0,temp_b=0,sum_r,sum_g,sum_b,temp_r1,temp_g1,temp_b1;
    reg [11:0]pixel;
//    reg [3:0] y=0, x=0;

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            temp_r <= 0;
            temp_g <= 0;
            temp_b <= 0;
//            y <= 0;
//            x <= 0;
        end else if (switch) begin
            temp_y[0][x] <= temp_y[1][x];
            temp_y[1][x] <= temp_y[2][x];
            temp_y[2][x] <= pixel_in;
            
            if (y >= 2 && x >= 2) begin
                sum_r <= 0;
                sum_g <= 0;
                sum_b <= 0;
                sum_r <=temp_y[0][x-2][11:8]*K00 + temp_y[0][x-1][11:8]*K01 + temp_y[0][x][11:8]*K02 +
                        temp_y[1][x-2][11:8]*K10 + temp_y[1][x-1][11:8]*K11 + temp_y[1][x][11:8]*K12 +
                        temp_y[2][x-2][11:8]*K20 + temp_y[2][x-1][11:8]*K21 + temp_y[2][x][11:8]*K22;
                sum_g <=temp_y[0][x-2][7:4]*K00 + temp_y[0][x-1][7:4]*K01 + temp_y[0][x][7:4]*K02 +
                        temp_y[1][x-2][7:4]*K10 + temp_y[1][x-1][7:4]*K11 + temp_y[1][x][7:4]*K12 +
                        temp_y[2][x-2][7:4]*K20 + temp_y[2][x-1][7:4]*K21 + temp_y[2][x][7:4]*K22;
                sum_b <=temp_y[0][x-2][3:0]*K00 + temp_y[0][x-1][3:0]*K01 + temp_y[0][x][3:0]*K02 +
                        temp_y[1][x-2][3:0]*K10 + temp_y[1][x-1][3:0]*K11 + temp_y[1][x][3:0]*K12 +
                        temp_y[2][x-2][3:0]*K20 + temp_y[2][x-1][3:0]*K21 + temp_y[2][x][3:0]*K22;
                temp_r1<= sum_r/D;
                temp_r<= (temp_r1<16 ? temp_r1:15);
                temp_r<= (temp_r1<0 ? 0:temp_r1);
                temp_g1<= sum_g/D;
                temp_g<= (temp_g1<16 ? temp_g1:15);
                temp_g<= (temp_g1<0 ? 0:temp_g1);
                temp_b1<= sum_b/D;
                temp_b<= (temp_b1<16 ? temp_b1:15);
                temp_b<= (temp_b1<0 ? 0:temp_b1);
                pixel[11:8]<=temp_r;
                pixel[7:4]<=temp_g;
                pixel[3:0]<=temp_b;
            end
            else begin
               pixel<=pixel_in;
            end
        end
    end
    assign pixel_out=(switch ? pixel : pixel_in);
endmodule
