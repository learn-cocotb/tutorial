# Packet: Fields Has VLAN, Type, HDRLength, PayloadLength, PacketLength
import constraint
p = constraint.Problem()
p.addVariable('length', range(64, 1500))
p.addVariable('hdrlength', [14, 16])
p.addVariable('payloadlength', range(50, 1486))
p.addVariable('type', range(0x800, 0x807))
p.addVariable('hasVLAN', [True, False])
p.addConstraint(lambda hdr, payload, length: length == hdr +
                payload, ['hdrlength', 'payloadlength', 'length'])
p.addConstraint(lambda vlan, hdrlen: hdrlen ==
                16 if vlan else hdrlen == 14, ['hasVLAN', 'hdrlength'])
p.addConstraint(lambda type, length: length == 64 if type ==
                0x806 else True, ['type', 'length'])
print(f"{p.getSolutions()}")
