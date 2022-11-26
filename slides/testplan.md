% Cocotb Learning Journey: Testplan
% Vijayvithal Jahagirdar
% October 10 2022

# Components of a verification plan

* Logistics: machine, regression farm, bugtracking, cloud, software, licenses etc.
* Environment: Unit Level, Subsystem, Chip Top, Back2Back Chips etc. and the verification component(Driver, BFM, Monitor, Generator, Assertions etc.) used for each.
* Testcases: Specify Testcase detail and which Environment it is run on.
* Goals: Code Coverage, Functional Coverage
* Schedule: Resource allocation and assignment

# Design specification

* Implements a 2 input OR Gate
* Interface: Simple RDY/EN protocol.
	* Producers assert RDY when they have data to offer and keep it asserted until EN is asserted
	* Consumers assert RDY when they can consume data and keep it asserted until EN is asserted
	* EN is asserted when both Producer.RDY and COnsumer.RDY are asserted.
* Can take 0-20 cycles to produce/consume data.


# Verification plan: Logistics:

* Machine: 1 Laptop.
* Repository: Github (url ....)
* Regression: Github Actions
* Issue tracking: Github Issues (url ....)
* Software : Python >3.6, iverilog, xcelium/vcs/questasim, cocotb, cocotb-bus, cocotb-coverage
* Licenses: Simulator License.
* BFM: None

# Verification plan: Environment:

* Unit Level, Subsystem, Chip Top, Back2Back Chips etc. and the verification component(Driver, BFM, Monitor, Generator, Assertions etc.) used for each.

# Verification plan: Testcases: TC1

*TC1*

* *Feature*: OR Gate Datapath test.
* Description: Give inputs to the a and b pins of the DUT and check whether the expected value matches the output of the DUT
	* Scenario: Directed Truth table test
	* Given: Unit Test Environment
	* When: Input is ((0,0),(0,1),(1,0),(1,1))
	* Then: Output is (0, 1, 1, 1)
	* Coverage: ...

# Verification plan: Testcases: TC1

*TC2*

* *Feature*: OR Gate Datapath Randomize test.
* Description: Give random inputs to the a and b pins of the DUT and check whether the expected value matches the output of the DUT
	* Scenario: Random test
	* Given: Unit Test Environment
	* When: Input A is 10 samples of random.randint(0,1)
	* AND: Input B is 10 samples of random.randint(0,1)
	* Then: Output is  A | B
	* Coverage: ...

# Verification plan: Goals: Code Coverage, Functional Coverage

* 100 % Code, Branch and Toggle Coverage
* 100 % Functional coverage

# Verification plan: Schedule:

| Resource | Testcase | Environment | Start Date | End Date   | Status  |
| ----     | --       | --          | --         | --         | --      |
| Vijay    | TC1      | Unit_OR     | 1 Oct 2022 | 2 Oct 2022 | Done    |
| Vijay    | TC2      | Unit_OR     | ...        | ...        | Pending |
| Vijay    | TC3      | Chip        | ...        | ...        | Pending |
# Verification: datapath

* Bins
	* A: [0,1] 
	* B: [0,1] 
	* Y: [0,1] 
* Cross
	* A x B

# Verification : protocol

States:

| Data       | En | Rdy | Description |
| --         | -- | --  | --          |
| dont care  | 0  | 0   | Idle        |
| valid data | 0  | 1   | Ready       |
| valid data | 1  | 1   | Transaction |

* The case where En is 1 and Rdy is 0 cannot occur.
* Once Rdy goes high data cannot change until transaction completes.i.e En goes high.
* We need to verify all state transition


 
# Verification : protocol: State transition verification

| Previous State | Current State |
| ---            | ---           |
| Idle           | Idle          |
| Idle           | Ready         |
| Idle           | Transaction   |
| ...            | ...           |

# Verification: protocol: Bins and crosses

* Bins
	* Current State = [Idle, Ready, Transaction]
	* Previous State = [Idle, Ready, Transaction]
* Cross
	* Current State x Previous State

# Verification: Delay

* Bins
	* Delay= [Min, Max, Low, High] # 0, 20, 1-10, 11-19
