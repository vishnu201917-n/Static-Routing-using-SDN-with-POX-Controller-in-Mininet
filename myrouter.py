from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()


def _handle_PacketIn(event):
    packet = event.parsed

    if not packet.parsed:
        return

    dpid = event.connection.dpid
    in_port = event.port

    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)

    # SWITCH 1 (s1)
    if dpid == 1:
        out_port = 2 if in_port == 1 else 1

    # SWITCH 2 (s2) – FLOODING (FULL CONNECTIVITY)
    elif dpid == 2:
        if in_port == 1:
            out_port = of.OFPP_FLOOD
        elif in_port == 2:
            out_port = of.OFPP_FLOOD
        elif in_port == 3:
            out_port = of.OFPP_FLOOD
        else:
            return

    # SWITCH 3 (s3)
    elif dpid == 3:
        out_port = 2 if in_port == 1 else 1

    else:
        return

    log.info("SWITCH %s: in=%s out=%s", dpid, in_port, out_port)

    msg.actions.append(of.ofp_action_output(port=out_port))
    msg.data = event.ofp

    event.connection.send(msg)


def launch():
    log.info("MyRouter Started")
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)