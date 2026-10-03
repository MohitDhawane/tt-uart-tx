## How it works

A UART transmitter. Set a byte on the eight input pins (`ui[7:0]`) and press
SEND (`uio[0]`). The chip sends the byte on TX (`uo[0]`) as 8N1 serial: a
start bit (0), the eight data bits least-significant first, then a stop bit
(1), at 115200 baud from the 50 MHz project clock (434 clocks per bit).

SEND passes through a two-flop synchroniser and a rising-edge detector, so
one press sends exactly one byte however long the button is held. READY
(`uo[1]`) is high while the transmitter is idle and low during a frame;
presses while READY is low are ignored. TX idles high.

## How to test

1. Set the clock to 50 MHz and reset the design.
2. Connect a USB-UART adapter's RX to `uo[0]` (TX) and its ground to the
   board ground. Open a terminal at 115200 baud, 8 data bits, no parity,
   1 stop bit.
3. Set `ui[7:0]` to an ASCII code, for example `0x41` for `A`, and press
   SEND (`uio[0]` high, then low). The character appears in the terminal.
4. Wait for READY (`uo[1]`) to go high before the next press.

## External hardware

A USB-UART adapter (3.3 V logic), or a PMOD USBUART on the output PMOD.
DIP switches for the data byte and a push button for SEND.
