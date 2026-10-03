/*
 * Copyright (c) 2026 Mohit Dhawane
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

// UART transmitter: sends the byte on ui_in as 8N1 serial on uo_out[0]
// each time uio_in[0] rises. 115200 baud from the 50 MHz project clock.
module tt_um_mohitdhawane_uart_tx (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  localparam integer CLOCK_HZ = 50_000_000;
  localparam integer BAUD     = 115_200;

  // The send button is asynchronous to clk: synchronise it, then act on
  // its rising edge so holding it down sends one byte, not a stream.
  reg [2:0] send_sync;
  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) send_sync <= 3'b000;
    else        send_sync <= {send_sync[1:0], uio_in[0]};
  end
  wire send_pulse = send_sync[1] & ~send_sync[2];

  wire tx;
  wire tx_ready;

  uart_tx #(
      .CLKS_PER_BIT((CLOCK_HZ + BAUD / 2) / BAUD)
  ) u_uart_tx (
      .clk     (clk),
      .rst_n   (rst_n),
      .tx_data (ui_in),
      .tx_valid(send_pulse),
      .tx      (tx),
      .tx_ready(tx_ready)
  );

  assign uo_out  = {6'b0, tx_ready, tx};
  assign uio_out = 8'b0;
  assign uio_oe  = 8'b0;

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, uio_in[7:1], 1'b0};

endmodule
