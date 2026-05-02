`timescale 1ns / 1ps
module UART_Rx #(
    parameter CLKS_PER_BIT = 868 // 115200 @ 100MHz ~868
)(
    input  wire       clk,
    input  wire       RsRx,
    output wire       o_RX_DV,
    output wire [7:0] RxByte
);
  localparam S0 = 3'b000; //IDLE
  localparam S1 = 3'b001; //START
  localparam S2 = 3'b010; //DATA
  localparam S3 = 3'b011; //STOP
  localparam S4 = 3'b100; //CLEAN

  reg tempdata1 = 1'b1;
  reg tempdata  = 1'b1;

  reg [15:0] clockcounter = 0;
  reg [2:0]  index = 0;
  reg [7:0]  tempRx = 0;
  reg [2:0]  state = S0;
  reg        r_RX_DV = 0;

  always @(posedge clk) begin
    tempdata1 <= RsRx;
    tempdata  <= tempdata1;
  end

  always @(posedge clk) begin
    case (state)
      S0: begin
        r_RX_DV <= 1'b0;
        clockcounter <= 0;
        index <= 0;
        if (tempdata == 1'b0) state <= S1;
        else state <= S0;
      end
      S1: begin
        if (clockcounter == (CLKS_PER_BIT-1)/2) begin
          if (tempdata == 1'b0) begin
            clockcounter <= 0;
            state <= S2;
          end else state <= S0;
        end else begin
          clockcounter <= clockcounter + 1;
          state <= S1;
        end
      end
      S2: begin
        if (clockcounter < CLKS_PER_BIT-1) begin
          clockcounter <= clockcounter + 1;
          state <= S2;
        end else begin
          clockcounter <= 0;
          tempRx[index] <= tempdata;
          if (index < 7) begin
            index <= index + 1;
            state <= S2;
          end else begin
            index <= 0;
            state <= S3;
          end
        end
      end
      S3: begin
        if (clockcounter < CLKS_PER_BIT-1) begin
          clockcounter <= clockcounter + 1;
          state <= S3;
        end else begin
          clockcounter <= 0;
          state <= S4;
          r_RX_DV <= 1'b1;
        end
      end
      S4: begin
        state <= S0;
        r_RX_DV <= 1'b0;
      end
      default: state <= S0;
    endcase
  end

  assign o_RX_DV = r_RX_DV;
  assign RxByte  = tempRx;
endmodule
