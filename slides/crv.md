% Constrained Random Vector Generation
% Vijayvithal Jahagirdar
% October 5 2022

# What are constraints

* Constraints are limits on what values a given variable can take.
* Mostly defined in protocol/architecture/design specification.
* May also be defined in testplan to hit specific goals.

# Example Specification: Ethernet packet

* A packet consists of header and payload.
* Header may or may not contain vlan tag.
* Headers with vlan tag have size of 16 bytes otherwise 14 bytes 
* Packets have different ethertype min ethertype is 0x800 max can go upto 0xffff
* Packets with ethertype 0x806 have a size of 64
* packet length is between 64 and 1500 bytes
* ...

# Generation using plain randomization

* Will require use of for loops, random.randint etc.
* Difficult to specilize with special test specific constraints from outsize the class.

# Generation from constraint class

* Looks similar to specification
