import cocotb
from cocotb.triggers import Timer, FallingEdge, RisingEdge, ReadOnly, NextTimeStep
from cocotb_bus.drivers import BusDriver
from cocotb_bus.monitors import BusMonitor
from cocotb_coverage.coverage import CoverCross, CoverPoint, coverage_db
import os


def sb_fn(actual_value):
    global expected_value
    assert actual_value == expected_value.pop(0), "Scoreboard Matching Failed"


@CoverPoint("top.a",  # noqa F405
            xf=lambda a, b: a,
            bins=[0, 1],
            bins_labels=['True', 'False']
            )
@CoverPoint("top.b",  # noqa F405
            xf=lambda a, b: b,
            bins=[0, 1],
            bins_labels=['True', 'False']
            )
@CoverCross("top.cross.ab",
            items=["top.b",
                   "top.a"
                   ]
            )
def cover(a, b):
    cocotb.log.info(f"AB={a} {b}")
    pass


@cocotb.test()
async def ifc_test(dut):
    global expected_value
    a = (0, 0, 1, 1)
    b = (0, 1, 0, 1)
    expected_value = [0, 1, 1, 1]
    dut.RST_N.value = 1
    await Timer(1, 'ns')
    dut.RST_N.value = 0
    await Timer(1, 'ns')
    await RisingEdge(dut.CLK)
    dut.RST_N.value = 1
    adrv = InputDriver(dut, 'a', dut.CLK)
    InputMonitor(dut, 'a', dut.CLK, callback=a_cover)
    bdrv = InputDriver(dut, 'b', dut.CLK)
    OutputDriver(dut, 'y', dut.CLK, sb_fn)

    for i in range(4):
        adrv.append(a[i])
        bdrv.append(b[i])
        cover(a[i], b[i])
    while len(expected_value) > 0:
        await Timer(2, 'ns')
    coverage_db.report_coverage(cocotb.log.info, bins=True)
    coverage_file = os.path.join(
        os.getenv('RESULT_PATH', "./"), 'coverage.xml')
    coverage_db.export_to_xml(filename=coverage_file)


class InputDriver(BusDriver):
    _signals = ['rdy', 'en', 'data']

    def __init__(self, dut, name, clk):
        BusDriver.__init__(self, dut, name, clk)
        self.bus.en.value = 0
        self.clk = clk

    async def _driver_send(self, value, sync=True):
        if self.bus.rdy.value != 1:
            await RisingEdge(self.bus.rdy)
        self.bus.en.value = 1
        self.bus.data.value = value
        await ReadOnly()
        await RisingEdge(self.clk)
        self.bus.en.value = 0
        await NextTimeStep()


class OutputDriver(BusDriver):
    _signals = ['rdy', 'en', 'data']

    def __init__(self, dut, name, clk, sb_callback):
        BusDriver.__init__(self, dut, name, clk)
        self.bus.en.value = 0
        self.clk = clk
        self.callback = sb_callback
        self.append(0)

    async def _driver_send(self, value, sync=True):
        while True:
            if self.bus.rdy.value != 1:
                await RisingEdge(self.bus.rdy)
            self.bus.en.value = 1
            await ReadOnly()
            self.callback(self.bus.data.value)
            await RisingEdge(self.clk)
            await NextTimeStep()
            self.bus.en.value = 0


class InputMonitor(BusMonitor):
    _signals = ['rdy', 'en', 'data']

    async def _monitor_recv(self):
        fallingedge = FallingEdge(self.clock)
        rdonly = ReadOnly()
        prev_state = 'Idle'
        state = {
            0: 'Idle',
            1: 'RDY',
            2: 'Error',
            3: "Txn"
        }
        while True:
            await fallingedge
            await rdonly
            s = state[self.bus.rdy.value | (self.bus.en.value << 1)]
            self._recv({'current': s, 'previous': prev_state})
            prev_state = s


@CoverPoint(f"top.a.ifc_state",  # noqa F405
            xf=lambda x: x['current'],
            bins=['Idle', 'RDY', 'Txn'],
            )
@CoverPoint(f"top.a.previfc_state",  # noqa F405
            xf=lambda x: x['previous'],
            bins=['Idle', 'RDY', 'Txn'],
            )
@CoverCross("top.cross.ifc.a",
            items=[
                "top.a.previfc_state", "top.a.ifc_state"
            ]
            )
def a_cover(state):
    cocotb.log.warning(f"state={state}")
    pass
