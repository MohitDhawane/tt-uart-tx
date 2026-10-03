# SPDX-FileCopyrightText: © 2026 Mohit Dhawane
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge, Timer

CLOCK_HZ = 50_000_000
BAUD = 115_200
CLKS_PER_BIT = (CLOCK_HZ + BAUD // 2) // BAUD  # 434
CLOCK_PERIOD_NS = 20


def tx(dut):
    return int(dut.uo_out.value) & 1


def ready(dut):
    return (int(dut.uo_out.value) >> 1) & 1


async def reset(dut):
    clock = Clock(dut.clk, CLOCK_PERIOD_NS, unit="ns")
    cocotb.start_soon(clock.start())
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 5)


async def receive_byte(dut):
    """Decode one 8N1 frame from uo_out[0], sampling at mid-bit."""
    while tx(dut) == 1:
        await FallingEdge(dut.clk)
    await ClockCycles(dut.clk, CLKS_PER_BIT // 2)
    assert tx(dut) == 0, "start bit not held low at mid-bit"
    value = 0
    for bit in range(8):
        await ClockCycles(dut.clk, CLKS_PER_BIT)
        value |= tx(dut) << bit
    await ClockCycles(dut.clk, CLKS_PER_BIT)
    assert tx(dut) == 1, "stop bit is not high"
    return value


async def press_send(dut, value, hold_cycles=4):
    dut.ui_in.value = value
    dut.uio_in.value = 1
    await ClockCycles(dut.clk, hold_cycles)
    dut.uio_in.value = 0


@cocotb.test()
async def test_idle_state(dut):
    await reset(dut)
    assert tx(dut) == 1, "TX must idle high"
    assert ready(dut) == 1, "READY must be high when idle"
    assert int(dut.uio_oe.value) == 0, "all bidirectional pins are inputs"


@cocotb.test()
async def test_sends_bytes(dut):
    await reset(dut)
    for value in (0x55, 0xA5, 0x00, 0xFF, 0x81, 0x3C):
        receiver = cocotb.start_soon(receive_byte(dut))
        await press_send(dut, value)
        await ClockCycles(dut.clk, 3)
        assert ready(dut) == 0, "READY must drop while sending"
        got = await receiver
        assert got == value, f"sent {value:#04x}, received {got:#04x}"
        # receive_byte returns at mid stop bit; READY rises when it ends.
        assert ready(dut) == 0, "READY must stay low through the stop bit"
        await ClockCycles(dut.clk, CLKS_PER_BIT // 2 + 2)
        assert ready(dut) == 1, "READY must return after the stop bit"
        dut._log.info(f"byte {value:#04x} OK")


@cocotb.test()
async def test_baud_rate(dut):
    await reset(dut)
    await press_send(dut, 0x00)
    while tx(dut) == 1:
        await FallingEdge(dut.clk)
    start = cocotb.utils.get_sim_time(unit="ns")
    # 0x00: start bit plus 8 zero data bits = 9 bit times low.
    while tx(dut) == 0:
        await FallingEdge(dut.clk)
    low_ns = cocotb.utils.get_sim_time(unit="ns") - start
    expected_ns = 9 * CLKS_PER_BIT * CLOCK_PERIOD_NS
    assert abs(low_ns - expected_ns) <= 2 * CLOCK_PERIOD_NS, (
        f"9 bit times took {low_ns} ns, expected {expected_ns} ns"
    )
    baud = 9e9 / low_ns
    assert abs(baud - BAUD) / BAUD < 0.01, f"baud {baud:.0f} is off by more than 1%"


@cocotb.test()
async def test_held_button_sends_once(dut):
    await reset(dut)
    receiver = cocotb.start_soon(receive_byte(dut))
    dut.ui_in.value = 0x42
    dut.uio_in.value = 1  # hold through the whole frame and beyond
    got = await receiver
    assert got == 0x42
    await ClockCycles(dut.clk, 3 * CLKS_PER_BIT)
    assert tx(dut) == 1 and ready(dut) == 1, "held button must not resend"
    dut.uio_in.value = 0
    await Timer(1, unit="us")
