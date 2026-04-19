from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet.ethernet import ethernet

log = core.getLogger()


def _handle_PacketIn(event):
    packet = event.parsed

    if not packet.parsed:
        return

    eth = packet.find('ethernet')

    # Ignore IPv6 (reduces errors)
    if eth.type == 0x86DD:
        return

    dpid = event.connection.dpid
    in_port = event.port

    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)

    # STATIC ROUTING + BLOCKING

    # SWITCH 1 (s1)
    if dpid == 1:
        if in_port == 1:
            out_port = 2
        elif in_port == 2:
            out_port = 1
        else:
            return

    # SWITCH 2 (s2)
    elif dpid == 2:
        if in_port == 2:        # from s1 → to h2
            out_port = 1
        elif in_port == 1:      # from h2 → to s1
            out_port = 2
        elif in_port == 3:      # from s3 → BLOCK
            log.info("Blocked traffic from s3")
            return
        else:
            return

    # SWITCH 3 (s3) → FULL BLOCK
    elif dpid == 3:
        log.info("Blocking all traffic at s3")
        return

    else:
        return

    log.info("SWITCH %s: in=%s out=%s", dpid, in_port, out_port)

    msg.actions.append(of.ofp_action_output(port=out_port))
    msg.data = event.ofp

    event.connection.send(msg)


def launch():
    log.info("Static Routing (Blocked Version) Started")
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
