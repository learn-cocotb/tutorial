% Cocotb Learning Journey: Verification Theory
% Vijayvithal Jahagirdar
% October 10 2022

# Complete verification is not possible

* The verification effort till now was to cover every row of the truth table for a 2 input logic.

* A 64 input logic  requires a truth table of $2^{64}$ rows.
* Testing at one row per cycle, the simulation requires 18,446,744,073,709,551,616 cycles i.e 18Exa-Ops i.e 18,00,000 trillion Operations
* The best in class server requires for 100+ years for verifying this
* Solution:
	* *Directed Tests*: Select a subset of vectors most likely to catch a bug(Min,Max,walking one, walking zero,alternate ones and zeroes etc.)
	* *Random Test*: Select a random subset of vectors to increase the likelyhood of hitting unexpected scenario.

# Directed vs random

| Parameter                                | Directed tests                   | Random tests |
| ---                                      | ----                             | ----         |
| Effort for test environment              | Less.                            | More         |
| Effort for testcases                     | More.                            | Less         |
| Simulation time                          | Less                             | More         |
| Hits known corner cases                  | Yes                              | No           |
| Hits unknown corner cases                | May not                          | Yes          |

# Approach

* Directed for initial bringup
* Randomization for regression testing
* Code and Functional coverage for signoff

# Metric for completion of verification

* Code Coverage: Measured by simulator
	* Statement/ line/ block coverage
	* Branch coverage
	* Toggle coverage
* Functional Coverage: Defined by test env writer
	* Bins
	* Cross Coverage

