import cocotb
from cocotb.triggers import Timer, RisingEdge, ReadOnly, NextTimeStep, Lock
from cocotb_bus.drivers import BusDriver


def fn_callback(value):
    global scoreboard
    assert value == scoreboard.pop(0)


@cocotb.test()
async def or_test(dut):
    a = (0, 0, 1, 1)
    b = (0, 1, 0, 1)
    y = (0, 1, 1, 1)
    dut.y_en.value = 0
    dut.RST_N.value = 1
    await Timer(1, 'ns')
    dut.RST_N.value = 0
    await Timer(1, 'ns')
    await RisingEdge(dut.CLK)
    dut.RST_N.value = 1
    global scoreboard
    scoreboard = []
    a_driver = EnRdyInDriver(dut, 'a', dut.CLK)
    b_driver = EnRdyInDriver(dut, 'b', dut.CLK)
    y_driver = EnRdyOutDriver(dut, 'y', dut.CLK, fn_callback)
    y_driver.append(0)

    for i in range(4):
        a_driver.append(a[i])
        b_driver.append(b[i])
        scoreboard.append(y[i])
    while len(scoreboard) != 0:
        await Timer(1, "ns")


class EnRdyInDriver(BusDriver):
    _signals = ['en', 'rdy', 'data']

    def __init__(self, dut, name, clk):
        BusDriver.__init__(self, dut, name, clk)
        self.bus_lock = Lock("%s_txn" % name)
        self.bus.en.value = 0
        self.clk = clk

    async def _driver_send(self, value, sync=True):
        await self.bus_lock.acquire()
        if self.bus.rdy.value != 1:
            await RisingEdge(self.bus.rdy)
        self.bus.data.value = value
        self.bus.en.value = 1
        await ReadOnly()
        await RisingEdge(self.clk)
        await ReadOnly()
        await NextTimeStep()
        self.bus.en.value = 0
        self.bus_lock.release()


class EnRdyOutDriver(BusDriver):
    _signals = ['en', 'rdy', 'data']

    def __init__(self, dut, name, clk, callback):
        BusDriver.__init__(self, dut, name, clk)
        self.bus_lock = Lock("%s_txn" % name)
        self.bus.en.value = 0
        self.clk = clk
        self.callback = callback

    async def _driver_send(self, value, sync=True):
        await self.bus_lock.acquire()
        while True:
            if self.bus.rdy.value != 1:
                await RisingEdge(self.bus.rdy)
            self.bus.en.value = 1
            await ReadOnly()
            self.callback(self.bus.data.value)
            await RisingEdge(self.clk)
            await ReadOnly()
            await NextTimeStep()
            self.bus.en.value = 0
        self.bus_lock.release()
