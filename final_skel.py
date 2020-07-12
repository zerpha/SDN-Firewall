#!/usr/bin/python

# Henry Nguyen
# hnguye87
# skeleton code provided by teacher, edited the class final_topo(Topo)

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class final_topo(Topo):
  def build(self):
    
    # Examples!
    # Create a host with a default route of the ethernet interface. You'll need to set the
    # default gateway like this for every host you make on this assignment to make sure all 
    # packets are sent out that port. Make sure to change the h# in the defaultRoute area
    # and the MAC address when you add more hosts!
    h1 = self.addHost('h10',mac='00:00:00:00:00:01',ip='10.0.1.10', defaultRoute="h10-eth0")
    h2 = self.addHost('h20',mac='00:00:00:00:00:02',ip='10.0.2.20', defaultRoute="h20-eth0")
    h3 = self.addHost('h30',mac='00:00:00:00:00:03',ip='10.0.3.30', defaultRoute="h30-eth0")
    h4 = self.addHost('h40',mac='00:00:00:00:00:04',ip='10.0.4.40', defaultRoute="h40-eth0")
    h5 = self.addHost('h50',mac='00:00:00:00:00:05',ip='10.0.5.50', defaultRoute="h50-eth0")
    h6 = self.addHost('h60',mac='00:00:00:00:00:06',ip='10.0.6.60', defaultRoute="h60-eth0")
    h7 = self.addHost('h70',mac='00:00:00:00:00:07',ip='10.0.7.70', defaultRoute="h70-eth0")
    h8 = self.addHost('h80',mac='00:00:00:00:00:08',ip='10.0.8.80', defaultRoute="h80-eth0")
    h9 = self.addHost('server',mac='00:00:00:00:00:09',ip='10.0.9.10', defaultRoute="server-eth0")
    h10 = self.addHost('untrusted',mac='00:00:00:00:00:10',ip='172.16.10.100/24', defaultRoute="untrusted-eth0")

    # Create a switch. No changes here from Lab 1.
    # must use convention switch names s#
    s1 = self.addSwitch('s1') #floor 1 switch 1
    s2 = self.addSwitch('s2') #floor 1 switch 2
    s3 = self.addSwitch('s3') #floor 2 switch 1
    s4 = self.addSwitch('s4') #floor 2 switch 2
    s5 = self.addSwitch('s5') #data center switch 
    s6 = self.addSwitch('s6') #core
    
    # Connect Port 8 on the Switch to Port 0 on Host 1 and Port 9 on the Switch to Port 0 on 
    # Host 2. This is representing the physical port on the switch or host that you are 
    # connecting to.
    
    #links h1,h2,s1 to core
    self.addLink(h1,s1,port1=0, port2=1)
    self.addLink(h2,s1,port1=0, port2=2)
    self.addLink(s6,s1,port1=1, port2=3)
    #links h3,h4,s2 to core    
    self.addLink(h3,s2,port1=0, port2=1)
    self.addLink(h4,s2,port1=0, port2=2)
    self.addLink(s6,s2,port1=2, port2=3)
    #links h5,h6,s3 to core
    self.addLink(h5,s3,port1=0, port2=1)
    self.addLink(h6,s3,port1=0, port2=2)
    self.addLink(s6,s3,port1=3, port2=3)
    #links h7,h8,s4 to core
    self.addLink(h7,s4,port1=0, port2=1)
    self.addLink(h8,s4,port1=0, port2=2)
    self.addLink(s6,s4,port1=4, port2=3)
    #links server->data center-> core
    self.addLink(h9,s5,port1=0, port2=1)
    self.addLink(s6,s5,port1=6, port2=3)
    #links untrusted-> core
    self.addLink(h10,s6,port1=0, port2=5)
    print('Topology made')

def configure():
  topo = final_topo()
  #net = Mininet(topo=topo)
  net = Mininet(topo=topo, controller=RemoteController)
  net.start()

  CLI(net)
  
  net.stop()


if __name__ == '__main__':
  configure()
