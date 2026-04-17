from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

drop_mode = False  # CHANGE THIS

def _handle_PacketIn(event):
    packet = event.parsed

    # Drop ICMP packets (simulate delay/loss)
    if drop_mode and packet.find('icmp'):
        log.info("Dropping ICMP packet")
        return

    # Normal forwarding
    msg = of.ofp_packet_out()
    msg.data = event.ofp
    msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
    event.connection.send(msg)

def launch():
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    log.info("Custom Latency Controller Running")
