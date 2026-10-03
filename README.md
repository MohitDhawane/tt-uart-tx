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

## Tiny Tapeout checks (GitHub Actions, 2026-10-03)

Run on [MohitDhawane/tt-uart-tx](https://github.com/MohitDhawane/tt-uart-tx/actions)
with the official `ttsky26d` actions:

| Job | Result |
|---|---|
| `gds`: LibreLane 3.0.14 hardening into the 1×1 tile | pass |
| `precheck`: Tiny Tapeout DRC, pin, power and layer checks | pass |
| `gl_test`: cocotb tests on the hardened gate-level netlist | pass |
| `test`: cocotb RTL tests | pass |
| `docs`: datasheet | pass |
| `viewer`: 3D preview on GitHub Pages | needs Pages enabled (Settings → Pages → Source: GitHub Actions) |

## Submit it

1. Done: the project is in https://github.com/MohitDhawane/tt-uart-tx and its
   checks are green.
2. Optional: enable Pages (Settings → Pages → Source: GitHub Actions) and
   re-run the `gds` workflow for the preview.
3. Submit the repository at <https://app.tinytapeout.com> for the open
   Sky130 shuttle.

## Licence

Apache-2.0, as Tiny Tapeout requires for submitted designs; their source and
GDS are published. This applies only to the files in this directory, not to
the rest of AI-EDA Studio.
