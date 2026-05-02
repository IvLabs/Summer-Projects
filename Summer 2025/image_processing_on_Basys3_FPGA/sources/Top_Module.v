`timescale 1ns / 1ps
// TOP MODULE also serves as address_generator and VGA_Driver and Filter
// Overall Flow: UART_Rx receives data --Pixel_Compiler makes 12 bit pixel data--image_memory stores this in BRAM at address given by top_module--VGA_Controller activates only when when display is on 
// VGA_Controller provides syncs right away---top_module provides final rgb vga signals and also applies filter
module top_image_vga(
    input wire clk_100MHz,
    input wire  reset,
    input wire display_switch,
//    input wire up,
//    input wire down,
    input wire RsRx,
    input [0:11]filter_switch,
    output [3:0] vgaRed,
    output [3:0] vgaGreen,
    output [3:0] vgaBlue,
    output hsync,
    output vsync,
    output led_recv,
    output led_stored
);

    localparam WIDTH  = 320;
    localparam HEIGHT = 240;
    localparam MEM_SIZE = WIDTH * HEIGHT;

    localparam ADDR_WIDTH = $clog2(MEM_SIZE);

    // UART + Pixel compiler
    wire [7:0] uart_byte;
    wire uart_dv;
    wire [11:0] pixel_data;
    wire pixel_compiled;
    wire [17:0]a1,a2;

    UART_Rx #(.CLKS_PER_BIT(868)) uart_rx_inst (
        .clk(clk_100MHz),
        .RsRx(RsRx),
        .o_RX_DV(uart_dv),
        .RxByte(uart_byte)
    );

    Pixel_Compiler pixel_comp_inst (
        .clk_100MHz(clk_100MHz),
        .reset(reset),
        .o_RX_DV(uart_dv),
        .RxByte(uart_byte),
        .pixel_data(pixel_data),
        .pixel_compiled(pixel_compiled)
    );

    //  address generator
    reg [ADDR_WIDTH-1:0] write_addr = 0;
    reg frame_stored = 0;

    always @(posedge clk_100MHz or posedge reset) begin
        if (reset) begin
            write_addr <= 0;
            frame_stored <= 0;
        end else if (!display_switch && pixel_compiled) begin
            write_addr <= write_addr + 1;  // if display-switch on and the pixel byte has been compiled generate memory-address for it , to be used for storing in BRAM
            if (write_addr == MEM_SIZE-1)
                frame_stored <= 1'b1; // light led to show image stored successfully
        end
    end

    // VGA Controller
    wire video_on, p_tick;
    wire [9:0] vga_x, vga_y;

    vga_controller_320x240 vga_ctrl (
        .clk_100MHz(clk_100MHz),
        .reset(reset),
        .hsync(hsync),
        .vsync(vsync),
        .video_on(video_on),
        .p_tick(p_tick),
        .x(vga_x),
        .y(vga_y),
        .display_switch(display_switch)
    );

    // two memory address are created one for storing purpose and the other for VGA diplay purpose
    wire [ADDR_WIDTH-1:0] mem_addr =
        display_switch ?
            ((vga_x < WIDTH*2 && vga_y < HEIGHT*2) ?
                ((vga_y/2) * WIDTH+ (vga_x/2)) :
                0) :
            write_addr;  // if display_switch(read mode of BRAM) on use address generated through VGA x and y , else(write mode of BRAM) use write addr

    // Memory block output (raw)
    wire [11:0] pixel_raw;

    image_memory #(
        .WIDTH(WIDTH),
        .HEIGHT(HEIGHT)
    ) mem_inst (
        .clk_100MHz(clk_100MHz),
        .display(display_switch),
        .addr(mem_addr),
        .pixel_in(pixel_data),
        .pixel_out(pixel_raw)
    );

    // Black background for QVGA, image apperas on top left corner of VGA Monitor
//    wire [11:0] pixel_out_black =
//        (vga_x < WIDTH*2 && vga_y < HEIGHT*2) ? pixel_raw : 12'h000;

    // VGA output registers temporary
    reg [3:0] r, g, b;
    always @(posedge clk_100MHz) begin
        if (p_tick) begin
            {r, g, b} <= pixel_raw; 
          
        end
    end
    wire [3:0] R[0:8],G[0:8],B[0:8];
    wire [9:0]x,y;
    assign x=vga_x/2;
    assign y=vga_y/2;
    assign R[0]=r;
    assign G[0]=g;
    assign B[0]=b;
    contrast c1(.switch(filter_switch[0:4]),.r(R[0]),.g(G[0]),.b(B[0]),.R(R[1]),.G(G[1]),.B(B[1]));
//    conv_rgb #(.M(WIDTH),.N(HEIGHT),.K00(1),.K01(1),.K02(1),.K10(1),.K11(1),.K12(1),.K20(1),.K21(1),.K22(1),.D(9))
//         conv1 (.clk(p_tick),.switch(filter_switch[5]),.rst(reset),.x(x),.y(y),
//         .r(R[1]),.g(G[1]),.b(B[1]),.R(R[2]),.G(G[2]),.B(B[2]));
    conv_rgb #(.M(WIDTH),.N(HEIGHT),.K00(-3),.K01(-10),.K02(-3),.K10(0),.K11(0),.K12(0),.K20(3),.K21(10),.K22(3),.D(1))
         conv2 (.clk(p_tick),.switch(filter_switch[5]),.rst(reset),.x(x),.y(y),
         .r(R[1]),.g(G[1]),.b(B[1]),.R(R[3]),.G(G[3]),.B(B[3]));
    conv_rgb #(.M(WIDTH),.N(HEIGHT),.K00(-3),.K01(0),.K02(3),.K10(-10),.K11(0),.K12(10),.K20(-3),.K21(0),.K22(3),.D(1))
         conv3 (.clk(p_tick),.switch(filter_switch[6]),.rst(reset),.x(x),.y(y),
         .r(R[3]),.g(G[3]),.b(B[3]),.R(R[4]),.G(G[4]),.B(B[4]));
//    conv_rgb #(.M(WIDTH),.N(HEIGHT),.K00(-1),.K01(0),.K02(1),.K10(-2),.K11(0),.K12(2),.K20(-1),.K21(0),.K22(1),.D(1))
//         conv4 (.clk(p_tick),.switch(filter_switch[8]),.rst(reset),.x(x),.y(y),
//         .r(R[4]),.g(G[4]),.b(B[4]),.R(R[5]),.G(G[5]),.B(B[5]));
//    conv_rgb #(.M(WIDTH),.N(HEIGHT),.K00(-1),.K01(2),.K02(-1),.K10(0),.K11(0),.K12(0),.K20(1),.K21(2),.K22(1),.D(1))
//         conv5 (.clk(p_tick),.switch(filter_switch[9]),.rst(reset),.x(x),.y(y),
//         .r(R[5]),.g(G[5]),.b(B[5]),.R(R[6]),.G(G[6]),.B(B[6]));
//    conv_rgb #(.M(WIDTH),.N(HEIGHT),.K00(0),.K01(1),.K02(0),.K10(1),.K11(-4),.K12(1),.K20(0),.K21(1),.K22(0),.D(1))
//         conv6 (.clk(p_tick),.switch(filter_switch[10]),.rst(reset),.x(x),.y(y),
//         .r(R[4]),.g(G[4]),.b(B[4]),.R(R[7]),.G(G[7]),.B(B[7]));
//    conv_rgb #(.M(WIDTH),.N(HEIGHT),.K00(-2),.K01(-1),.K02(0),.K10(-1),.K11(1),.K12(1),.K20(0),.K21(1),.K22(2),.D(1))
//         conv7 (.clk(p_tick),.switch(filter_switch[11]),.rst(reset),.x(x),.y(y),
//         .r(R[4]),.g(G[4]),.b(B[4]),.R(R[8]),.G(G[8]),.B(B[8]));
//   VGA Driver

    assign vgaRed   = (video_on ? R[4] : 4'b0000);  // if outside visible area display black ; not required in QVGA
    assign vgaGreen = (video_on ? G[4] : 4'b0000);
    assign vgaBlue  = (video_on ? B[4] : 4'b0000);

    assign led_recv   = pixel_compiled; // blinks so fast remains undetected to human eye
    assign led_stored = frame_stored; // on implies image stored ,now display and filter switch can be used
    
    

endmodule
