`timescale 1ns / 1ps
// This is a single port BRAM , memory read mode when display on; memory write mode when display off
// on which address to store pixel received via UART and from which address to fetch stored pixel data to display via VGA is expected from another module , top_module
module image_memory #(
    parameter WIDTH  = 320,
    parameter HEIGHT = 240
)(
    input  wire clk_100MHz,
    input  wire display,  // display_switch , 0 = write mode, 1 = read mode
    input  wire [$clog2(WIDTH*HEIGHT)-1:0] addr, //$clog2 adjusts size required as per the parameters
    input  wire [11:0] pixel_in, // the pixel data to write in memory
    output reg  [11:0] pixel_out // pixel data in memory to be displayed
);

    // BRAM
    (* ram_style = "block" *) reg [11:0] image [0:WIDTH*HEIGHT-1]; // tells vivado to use BRAM instead of LUTS otherwise implementtion might fail 

    always @(posedge clk_100MHz) begin
        if (!display) begin
            image[addr] <= pixel_in; // write when display_switch off
        end
        pixel_out <= image[addr]; //  read when display_switch on
    end

endmodule
