/*
 * Copyright (c) 2026 Mohit Dhawane
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

// uart_tx: 8N1 UART transmitter.
//
// Accepts a byte when tx_valid && tx_ready, then shifts out one start bit
// (0), eight data bits LSB first and one stop bit (1), each held for
// CLKS_PER_BIT clock cycles. tx idles high. tx_ready is high only when idle.
module uart_tx #(
    parameter integer CLKS_PER_BIT = 868   // 100 MHz / 115200 baud
) (
    input  wire       clk,
    input  wire       rst_n,
    input  wire [7:0] tx_data,
    input  wire       tx_valid,
    output reg        tx,
    output wire       tx_ready
);
    localparam integer CW = $clog2(CLKS_PER_BIT);

    reg [CW-1:0] baud_count;
    reg [3:0]    bit_index;   // 0 = start, 1..8 = data, 9 = stop
    reg [7:0]    shift;
    reg          busy;

    assign tx_ready = !busy;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            tx         <= 1'b1;
            busy       <= 1'b0;
            baud_count <= {CW{1'b0}};
            bit_index  <= 4'd0;
            shift      <= 8'd0;
        end else if (!busy) begin
            tx <= 1'b1;
            if (tx_valid) begin
                busy       <= 1'b1;
                shift      <= tx_data;
                bit_index  <= 4'd0;
                baud_count <= {CW{1'b0}};
                tx         <= 1'b0;                 // start bit
            end
        end else if (baud_count == CLKS_PER_BIT - 1) begin
            baud_count <= {CW{1'b0}};
            if (bit_index == 4'd9) begin
                busy <= 1'b0;                       // stop bit done
                tx   <= 1'b1;
            end else begin
                bit_index <= bit_index + 4'd1;
                if (bit_index == 4'd8) begin
                    tx <= 1'b1;                     // stop bit
                end else begin
                    tx    <= shift[0];              // data, LSB first
                    shift <= {1'b0, shift[7:1]};
                end
            end
        end else begin
            baud_count <= baud_count + {{(CW-1){1'b0}}, 1'b1};
        end
    end
endmodule
