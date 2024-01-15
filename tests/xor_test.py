import cocotb
from cocotb.triggers import Timer


@cocotb.test()
async def dut_test(dut):
    a = (0,0,1,1,);
    b = (0,1,0,1);
    y = (0,1,1,0);
    for i in range(4):
        dut.a.value  = a[i]
        dut.b.value  = a[i]
        await Timer(1,'ns')
        assert dut.y.value == y[i], "Error at iteration {i} {a[i]} {b[i]} {y[i]}"