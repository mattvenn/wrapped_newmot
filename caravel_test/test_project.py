import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles, with_timeout

@cocotb.test()
async def test_start(dut):
    clock = Clock(dut.clk, 25, units="ns") # 40M
    cocotb.fork(clock.start())
    
    dut.RSTB <= 0
    dut.power1 <= 0;
    dut.power2 <= 0;
    dut.power3 <= 0;
    dut.power4 <= 0;

    await ClockCycles(dut.clk, 8)
    dut.power1 <= 1;
    await ClockCycles(dut.clk, 8)
    dut.power2 <= 1;
    await ClockCycles(dut.clk, 8)
    dut.power3 <= 1;
    await ClockCycles(dut.clk, 8)
    dut.power4 <= 1;

    await ClockCycles(dut.clk, 80)
    dut.RSTB <= 1

    # wait with a timeout for the project to become active
    await with_timeout(RisingEdge(dut.uut.mprj.wrapped_newmot.active), 150, 'us')
    dut._log.info("Project active")

    # wait start of motion
    await with_timeout(FallingEdge(dut.uut.mprj.wrapped_newmot.newmot.main_motiongeneratoraxis_done), 1000, 'us')

    # wait end of motion
    await with_timeout(RisingEdge(dut.uut.mprj.wrapped_newmot.newmot.main_motiongeneratoraxis_done), 200, 'us')
    dut._log.info("Motion done")
