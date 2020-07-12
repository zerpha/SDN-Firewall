# Final Skeleton
#
# Henry Nguyen
# hnguye87
# 
# Skeleton Code provided by teacher, only edited
# do_final function
#
# Hints/Reminders from Lab 4:
# 
# To send an OpenFlow Message telling a switch to send packets out a
# port, do the following, replacing <PORT> with the port number the 
# switch should send the packets out:
#
#    msg = of.ofp_flow_mod()
#    msg.match = of.ofp_match.from_packet(packet)
#    msg.idle_timeout = 30
#    msg.hard_timeout = 30
#
#    msg.actions.append(of.ofp_action_output(port = <PORT>))
#    msg.data = packet_in
#    self.connection.send(msg)
#
# To drop packets, simply omit the action.
#

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Final (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_final (self, packet, packet_in, port_on_switch, switch_id):
    # This is where you'll put your code. The following modifications have 
    # been made from Lab 4:
    #   - port_on_switch represents the port that the packet was received on.
    #   - switch_id represents the id of the switch that received the packet
    #      (for example, s1 would have switch_id == 1, s2 would have switch_id == 2, etc...) 

    #end system IPs
    h1 = '10.0.1.10'
    h2 = '10.0.2.20'
    h3 = '10.0.3.30'
    h4 = '10.0.4.40'
    h5 = '10.0.5.50'
    h6 = '10.0.6.60'
    h7 = '10.0.7.70'
    h8 = '10.0.8.80'
    untrusted = '172.16.10.100'
    server = '10.0.9.10'

    # numbers corresponding to switches
    # f1s1 = 1, f1s2 = 2, f2s1 = 3, f2s2 = 4, datacenter = 5, core = 6    

    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)
    msg.idle_timeout = 20
    msg.hard_timeout = 50
    
    # Firewall Rules: untrusted host cant send TCP to server 1
    # untrusted cant send ICMP at all to anyone

    # flags to see if packets are valid under firewall rules
    icmpFlag = ((packet.find('icmp')is not None) and (packet.find('ipv4').srcip != untrusted))
    tcpFlag = ((packet.find('tcp')is not None) and (packet.find('ipv4').srcip == untrusted and packet.find('ipv4').dstip == server )is False)
    
    if(packet.find('ipv4')is None): #not IP packet
	print('non-IP packet')
	msg.data = packet_in
        flood = of.ofp_action_output(port = of.OFPP_FLOOD)
	msg.actions.append(flood) #flood traffic out all ports
	self.connection.send(msg)
    else:
      # IP packet, TCP or ICMP type packet
      if(icmpFlag == True or tcpFlag == True): # check if packet is valid under rules
        print('valid IP packet')
        print('  Source IP: {}'.format(packet.find('ipv4').srcip))
        print('  Destination IP: {}'.format(packet.find('ipv4').dstip))
        if(packet.find('icmp')is not None):
          print('  Type: ICMP packet')
        if(packet.find('tcp')is not None):
          print('  Type: TCP packet')

	msg.data = packet_in
        if(switch_id == 1): # floor1 switch1
          if(packet.find('ipv4').dstip == h1):
	    msg.actions.append(of.ofp_action_output(port = 1))
          elif(packet.find('ipv4').dstip == h2):
	    msg.actions.append(of.ofp_action_output(port = 2))
	  else:
	    msg.actions.append(of.ofp_action_output(port = 3))
        elif(switch_id == 2): # floor1 switch2
          if(packet.find('ipv4').dstip == h3):
            msg.actions.append(of.ofp_action_output(port = 1))
          elif(packet.find('ipv4').dstip == h4):
            msg.actions.append(of.ofp_action_output(port = 2))
          else:
            msg.actions.append(of.ofp_action_output(port = 3))
        elif(switch_id == 3): # floor2 switch1
          if(packet.find('ipv4').dstip == h5):
            msg.actions.append(of.ofp_action_output(port = 1))
          elif(packet.find('ipv4').dstip == h6):
            msg.actions.append(of.ofp_action_output(port = 2))
          else:
            msg.actions.append(of.ofp_action_output(port = 3))
        elif(switch_id == 4): # floor2 switch2
          if(packet.find('ipv4').dstip == h7):
            msg.actions.append(of.ofp_action_output(port = 1))
          elif(packet.find('ipv4').dstip == h8):
            msg.actions.append(of.ofp_action_output(port = 2))
          else:
            msg.actions.append(of.ofp_action_output(port = 3))
        elif(switch_id == 5): # data center
          if(packet.find('ipv4').dstip == server):
            msg.actions.append(of.ofp_action_output(port = 1))
          else:
            msg.actions.append(of.ofp_action_output(port = 3))
        else: #core
          if(packet.find('ipv4').dstip == h1 or packet.find('ipv4').dstip == h2):
            msg.actions.append(of.ofp_action_output(port = 1))
          elif(packet.find('ipv4').dstip == h3 or packet.find('ipv4').dstip == h4):
            msg.actions.append(of.ofp_action_output(port = 2))
          elif(packet.find('ipv4').dstip == h5 or packet.find('ipv4').dstip == h6):
            msg.actions.append(of.ofp_action_output(port = 3))
          elif(packet.find('ipv4').dstip == h7 or packet.find('ipv4').dstip == h8):
            msg.actions.append(of.ofp_action_output(port = 4))
	  elif(packet.find('ipv4').dstip == untrusted):
            print('To untrusted')
            msg.actions.append(of.ofp_action_output(port = 5))
          elif(packet.find('ipv4').dstip == server):
            msg.actions.append(of.ofp_action_output(port = 6))
          else: 
	    print('Should not be able to get here as all cases are covered for')

        self.connection.send(msg)	    

      else:
        #dropped packet if invalid under firewall rules
        print('Dropped Packet')
        print('  Source IP: {}'.format(packet.find('ipv4').srcip))
        print('  Destination IP: {}'.format(packet.find('ipv4').dstip))
        if(packet.find('icmp')is not None):
	  print('  Type: ICMP packet')
        if(packet.find('tcp')is not None):
	  print('  Type: TCP packet')
        self.connection.send(msg)

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_final(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
