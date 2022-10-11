% Cocotb Learning Journey: Testplan
% Vijayvithal Jahagirdar
% October 10 2022

# Complete verification is not possible.

* Our verification effort till now was to cover every row of the truth table for a 2 input logic.

* For a 64 input logic we have $2^64$ rows in our truth table,
* Even if we test one row per cycle, the simulation will run for 100+ years
* Solution:
	* *Directed Tests* Select a subset of vectors most likely to catch a bug(Min,Max,walking one, walking zero,alternate ones and zeroes etc.)
	* *Random Test* Select a random subset of vectors to increase the likelyhood of hitting unexpected scenario.

# Directed vs Random
| Directed tests                    | Random tests                         |
| ----                              | ----                                 |
| More development time.            | Less development time                |
| Less simulation time              | more simulation time                 |
| hits all known corner cases       | May not cover all known corner cases |
| will not hit unknown corner cases | May not hit unknown corner cases     |

# Approach

* Directed for initial bringup
* Randomization for regression testing
* Functional coverage to ensure all known cases are covered.

# Links for FC
Bins & crosses
