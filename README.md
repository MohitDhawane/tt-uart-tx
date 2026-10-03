# Tiny Tapeout project: UART transmitter

`tt_um_mohitdhawane_uart_tx` sends the byte on `ui[7:0]` as 8N1 serial at
115200 baud on `uo[0]` each time `uio[0]` rises. See [docs/info.md](docs/info.md).

This directory is a complete Tiny Tapeout project, built from the official
[ttsky-verilog-template](https://github.com/TinyTapeout/ttsky-verilog-template)
for the current Sky130 shuttle (`ttsky26d` actions). It is meant to become
its own public GitHub repository, because Tiny Tapeout builds and checks each
submission from a repository.

## Verified so far

| Check | Where | Result |
|---|---|---|
| RTL tests (cocotb: idle, 6 bytes, baud rate within 1%, held button sends once) | `test/`, Icarus | 4/4 pass |
| Synthesis / P&R / signoff of this exact top module | AI-EDA Studio flow, Sky130 | 78 cells, 63 µm die |
| DRC | Magic; KLayout `sky130A_mr` (236 rules) | 0 / 0 |
| LVS | Netgen | Circuits match uniquely |
| Timing (post-route RCX) | ss setup / ff hold | +5.21 ns / +0.05 ns |
| Gate-level tests (same cocotb tests on the routed Sky130 netlist) | Icarus + PDK cell models | 4/4 pass |

## Not yet verified

Tiny Tapeout's own GitHub Actions: LibreLane hardening into the 1×1 tile,
the Tiny Tapeout precheck, and their gate-level test. These could not run in
the build environment (its network blocks the LibreLane container image).
They run automatically on every push once this is its own repository.

## Submit it

1. Create a new public GitHub repository (for example `tt-uart-tx`) and copy
   the contents of this directory to its root, including `.github/`.
2. In the repository settings, enable GitHub Actions and set Pages to deploy
   from GitHub Actions.
3. Push. Check that the `gds`, `test` and `docs` workflows go green.
4. Submit the repository at <https://app.tinytapeout.com> for the open
   Sky130 shuttle.

## Licence

Apache-2.0, as Tiny Tapeout requires for submitted designs; their source and
GDS are published. This applies only to the files in this directory, not to
the rest of AI-EDA Studio.
