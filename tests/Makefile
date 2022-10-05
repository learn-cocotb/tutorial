SIM ?= icarus
TOPLEVEL_LANG ?= verilog
VERILOG_SOURCES += $(PWD)/../hdl/or_gate.v
VERILOG_SOURCES += $(PWD)/wrappers/or_test.v
or:
	$(MAKE) sim MODULE=or_test TOPLEVEL=or_test
include $(shell cocotb-config --makefiles)/Makefile.sim
