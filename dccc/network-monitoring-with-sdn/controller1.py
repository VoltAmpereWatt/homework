from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3, ether, inet
from ryu.lib.packet import packet, ethernet, arp, ipv4, tcp, udp
import csv
from operator import attrgetter
from ryu.lib import hub
# from ryu.app import simple_switch_13

class simple_switch_13(app_manager.RyuApp):
	OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

	def __init__(self, *args,**kwargs):
		super(simple_switch_13, self).__init__(*args, **kwargs)
		self.arp_table = {}
		self.arp_table['10.0.0.1'] = '00:00:00:00:00:01'
		self.arp_table['10.0.0.2'] = '00:00:00:00:00:02'
		self.arp_table['10.0.0.3'] = '00:00:00:00:00:03'
		self.datapaths = {}
		self.monitor_thread = hub.spawn(self._monitor)

	@set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
	def switch_features_handler(self, ev):
		datapath = ev.msg.datapath
		ofproto = datapath.ofproto
		parser = datapath.ofproto_parser

		# Insert Static rule
		match = parser.OFPMatch()
		actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
		self.add_flow(datapath, 0, match, actions)
		# Installing static rules to process TCP/UDP and ICMP and ACL
		dpid = datapath.id  # classifying the switch ID

		if dpid == 3: # switch S3
			# UDP forwarding
			#self.L4PktHandler(datapath, inet.IPPROTO_UDP, '10.0.0.1', 10, 1)
			self.L4PktHandler(datapath, inet.IPPROTO_UDP, ipv4_dst = '10.0.0.1', priority = 10, fwd_port = 1)
			self.L4PktHandler(datapath, inet.IPPROTO_UDP, ipv4_dst = '10.0.0.2', priority = 10, fwd_port = 2)
			self.L4PktHandler(datapath, inet.IPPROTO_UDP, ipv4_dst = '10.0.0.3', priority = 10, fwd_port = 2)

		# implement ACL rules
		# this rule drops the UDP traffic directed to h1
			# match = parser.OFPMatch(eth_type = ether.ETH_TYPE_IP,ipv4_dst = '10.0.0.1',ip_proto = inet.IPPROTO_UDP)
			# actions = [parser.OFPActionOutput()]
			# self.add_flow(datapath, 30, match, actions)  #add a flow to controller

		elif dpid == 4: # switch S4
			### implement udp fwding
			self.L4PktHandler(datapath, inet.IPPROTO_UDP, ipv4_dst = '10.0.0.1', priority = 10, fwd_port = 2)
			self.L4PktHandler(datapath, inet.IPPROTO_UDP, ipv4_dst = '10.0.0.2', priority = 10, fwd_port = 1)
			self.L4PktHandler(datapath, inet.IPPROTO_UDP, ipv4_dst = '10.0.0.3', priority = 10, fwd_port = 2)


		elif dpid == 5: # switch S5
			### implement udp fwding
			self.L4PktHandler(datapath, inet.IPPROTO_UDP, ipv4_dst = '10.0.0.1', priority = 10, fwd_port = 2)
			self.L4PktHandler(datapath, inet.IPPROTO_UDP, ipv4_dst = '10.0.0.2', priority = 10, fwd_port = 2)
			self.L4PktHandler(datapath, inet.IPPROTO_UDP, ipv4_dst = '10.0.0.3', priority = 10, fwd_port = 1)


		elif dpid == 1: # switch S1
			### implement udp fwding
			self.L4PktHandler(datapath, inet.IPPROTO_UDP, ipv4_dst = '10.0.0.1', priority = 10, fwd_port = 1)
			self.L4PktHandler(datapath, inet.IPPROTO_UDP, ipv4_dst = '10.0.0.2', priority = 10, fwd_port = 2)
			self.L4PktHandler(datapath, inet.IPPROTO_UDP, ipv4_dst = '10.0.0.3', priority = 10, fwd_port = 3)
			# implement ACL rules
			# directs the HTTP packets to h2 to the controller

	def L4PktHandler(self, datapath, ip_proto, ipv4_dst = None, priority = 1, fwd_port = None):
		parser = datapath.ofproto_parser
		actions = [parser.OFPActionOutput(fwd_port)]
		match = parser.OFPMatch(eth_type = ether.ETH_TYPE_IP,ip_proto = ip_proto,ipv4_dst = ipv4_dst)
		self.add_flow(datapath, priority, match, actions)

	def add_flow(self, datapath, priority, match, actions):
		ofproto = datapath.ofproto
		parser = datapath.ofproto_parser
		inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
		mod = parser.OFPFlowMod(datapath=datapath, priority=priority,match=match, instructions=inst)
		datapath.send_msg(mod)

	@set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
	def packet_in_handler(self, ev):
		msg = ev.msg
		datapath = msg.datapath
		ofproto = datapath.ofproto
		parser = datapath.ofproto_parser

		in_port = msg.match['in_port']
		pkt = packet.Packet(msg.data)
		eth = pkt.get_protocol(ethernet.ethernet)
		ethertype = eth.ethertype
		self.logger.info(datapath.id)

	def _monitor(self):
		while True:
			for dp in self.datapaths.values():
				self.request_stats(dp)
			hub.sleep(10)

	def _request_stats(self,datapath):
		self.logger.debug('send data stats rquest:%016x',datapath.id)
		ofproto = datapath.ofproto
		parser = datapath.ofproto_parser

		req = parser.OFPFlowStatsRequest(datapath)
		datapath.send_msg(req)

		req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
		datapath.send_msg(req)

	@set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
	def _flow_stats_reply_handler(self, ev):
		body = ev.msg.body
		for stat in sorted([flow for flow in body], key=lambda flow:(flow.match['in_port'], flow.match['eth_dst'])):
			with open('flowstats.csv',mode='w') as flows_file:
				flow_writer = csv.writer(flows_file, delimiter=',', quotechar = '""',quoting=csv.QUOTE_MINIMAL)
				flow_writer.writerow([ev.msg.datapath.id, stats.match['in_port'],stats.match['eth_dst'],
									stat.instructions[0].actions[0].port,
									stat.packet_count,stat.byte_count])

	@set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
	def _port_starts_reply_handler(self, ev):
		body = ev.msg.body
		for stat in sorted(body, key= attrgetter('port_no')):
			with open('portstats.csv',mode='w') as ports_file:
				flow_write.writerow([ev.msg.datapath.id, stat.port_no,
									stat.rx_packets,stat.rx_bytes,stat.rx_errors,
									stat.tx_packets,stat.tx_bytes,stat.tx_erpors])
