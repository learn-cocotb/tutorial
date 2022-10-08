% Cocotb Learning Journey
% Vijayvithal Jahagirdar
% October 5 2022

# What is cocotb

* cocotb is a COroutine based COsimulation TestBench environment for verifying VHDL and SystemVerilog RTL using Python.
* cocotb is completely free, open source (under the BSD License) and hosted on GitHub.

Translation: Cocotb is a Python based verification framework for simulating RTL written using Verilog/VHDL or SV.

# Learning Journey

* Hello world. OR Gate.
* Interfaces
* Randomization
* Drivers
* Monitors
* Scoreboards
* Coverage
	* Functional coverage
		* Bins and cross coverage 
	* CRV
* BFM's: AXI, APB, Wishbone, Avalon, PCIe, Ethernet, UART, SPI, I2C...

# Getting started

* https://docs.cocotb.org/en/stable/
* [Github Classroom](https://classroom.github.com/classrooms/115061083-learn-cocotb-classroom)

# Example "or Gate"

A 2 input OR Gate is represented by the truth table

| a  | b  | y  |
| -- | -- | -- |
| 0  | 0  | 0  |
| 0  | 1  | 1  |
| 1  | 0  | 1  |
| 1  | 1  | 1  |

Where a and b are inputs to the gate and y is the output.

# Assignment: "XOR gate verification"

* [XOR gate verification](https://classroom.github.com/a/D3N4nEj7)

# Interfaces: Simple RDY/EN protocol specification.

When data is transferred from one module to another, we need to ensure that

* Destination module is ready to accept data.
* Source module is ready to send data.

Data transfer takes place iff source and destination are both ready.

EN is asserted to indicate to the source and destination that the transfer has taken place

# Protocol Verification

Based on the protocol description we have the following truth table

| Data       | En | Rdy | Description |
| --         | -- | --  | --          |
| dont care  | 0  | 0   | Idle        |
| valid data | 0  | 1   | Ready       |
| valid data | 1  | 1   | Transaction |

* The case where En is 1 and Rdy is 0 cannot occur.
* Once Rdy goes high data cannot change until transaction completes. En goes high.
* We need to verify all state transition
 
# State transition verification

| Previous State | Current State |
| ---            | ---           |
| Idle           | Idle          |
| Idle           | Ready         |
| Idle           | Transaction   |
| Ready          | Idle          |
| Ready          | Ready         |
| Ready          | Transaction   |
| Transaction    | Idle          |
| Transaction    | Ready         |
| Transaction    | Transaction   |

# Cross Verification

| A State     | B State     |
| ---         | ---         |
| Idle        | Idle        |
| Idle        | Ready       |
| Idle        | Transaction |
| Ready       | Idle        |
| Ready       | Ready       |
| Ready       | Transaction |
| Transaction | Idle        |
| Transaction | Ready       |
| Transaction | Transaction |

# Assignment FIFO interface verification

FIFO interface has a similar protocol to the EN/RDY protocol.

* Data source signals are 
	* not_empty, dout, dequeue
* Data sink signals are
	* not_full, din, enqueue

A transaction takes place when:

* Source is not empty and
* Sink is not full,

 The corresponding sink.enqueue and source.dequeue signals are asserted when the transfer takes place.

# Backup Slides

# Development and verification with Cocotb is fast

While the actual simulation speed might be slower than a simulation on a commercial simulation with native support for SV+UVM, Overall verification with cocotb is fast because of the following factors.

* Fast development
	* In my experience we can get a basic cocotb based test env up within hours.
* Fast regression.
	* Commercial simulator licenses are expensive, regressions parallism will be limited by available licenses.
	* With cocotb + Icarus We can fire all out testcases at the same time resulting in lesser overall regression time.
* Agile workflow
	* With commercial simulator, the number of regressions that can be fired by a team/week is restricted due to cost factor. Typically developers have to wait for the weekly regression to get feedback on their checkins.
	* With cocotb + icarus we can fire regression on every checkin resulting in continous and quick feedback loop.

