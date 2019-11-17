from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3, ether, inet, ofproto_v1_3_parser
from ryu.lib.packet import packet, ethernet, arp, ipv4, tcp, udp, icmp

class Switch(app_manager.RyuApp):
	OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

	def __init__(self, *args, **kwargs):
		super(Switch, self).__init__(*args, **kwargs)
		self.mac_to_port = {}
		self.counter = 0
		self.out_ports = [2,3,4]
		# self.arp_table['10.0.0.1']='00:00:00:00:00:01'
		# self.arp_table['10.0.0.2']='00:00:00:00:00:02'

	@set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
	def switch_features_handler(self,ev):
		msg = ev.msg
		dp = msg.datapath
		ofproto = dp.ofproto
		ofp_parser = dp.ofproto_parser
		match = ofp_parser.OFPMatch()
		actions = [ofp_parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,ofproto.OFPCML_NO_BUFFER)]
		self.add_flow(dp, 0, match, actions)

	def add_flow(self, datapath, priority,match, actions):
		ofproto = datapath.ofproto
		parser = datapath.ofproto_parser
		inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
		mod = parser.OFPFlowMod(datapath = datapath,
								priority = priority,
								match = match,
								instructions = inst)
		datapath.send_msg(mod)

	@set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
	def packet_in_handler(self, ev):
		msg = ev.msg
		dp = msg.datapath
		ofp = dp.ofproto
		ofp_parser = dp.ofproto_parser
		dpid = datapath.id
		self.mac_to_port.setdefault(dpid,{})
		in_port = msg.match['in_port']

		pkt = packet.Packet(msg.data)

		tcp_pkt = pkt.get_protocol(tcp.tcp)
		src_tcp = tcp_pkt.src_port
		dst_tcp = tcp_pkt.dst_port

		ether_pkt = pkt.get_protocol(ethernet.ethernet)
		src_mac = ether_pkt.src
		dst_mac = ether_pkt.dst
		mac_to_port[dpid][src_mac] = in_port

		ipv4_pkt = pkt.get_protocol(ipv4.ipv4)
		src_ipv4 = ipv4_pkt.src
		dst_ipv4 = ipv4_pkt.dst
		'''
		handle packet in.
		if source is h1, set out port to 2 to go to s1
		set priotiy as 1
		'''
		if tcp_pkt:
			self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port)
			# If src_mac is for h1 or h2, then we're at the edge switches.
			# but for core switches, the macs are from the edge switches.
			# so instead, we'll look into the tcp packet
			# self.counter += 1
			# out_port_index = self.counter%3
			# out_port = self.out_ports[out_port_index]
			if src_mac == '00:00:00:00:00:01':
				out_port_index = self.count%3
				# Setting Both Flows simultaneously
				in_port, out_port = 1, self.out_ports[out_port_index]
				flow_write(dp,in_port,out_port,msg.data)
				in_port, out_port = out_port, in_port
				flow_write(dp,in_port,out_port,msg.data)
				self.counter += 1

			elif src_mac == '00:00:00:00:00:02':
				out_port_index = self.count%3
				# Setting Both Flows simultaneously
				in_port, out_port = 1, self.out_ports[out_port_index]
				flow_write(dp,in_port,out_port,msg.data)
				in_port, out_port = out_port, in_port
				flow_write(dp,in_port,out_port,msg.data)
				self.counter += 1

			# look into ip packet if src isn't a host
			elif src_tcp == '10.0.0.1':
				# Setting Both Flows simultaneously
				in_port, out_port = 1, 2
				flow_write(dp,in_port,out_port,msg.data)
				in_port, out_port = out_port, in_port
				flow_write(dp,in_port,out_port,msg.data)
				# counter += 1

			# NOT SURE IF THIS IS NEEDED
			# elif src_tcp == '10.0.0.2':
			# 	# Setting Both Flows simultaneously
			# 	in_port, out_port = 2,1
			# 	flow_write(dp,in_port,out_port,msg.data)
			# 	in_port, out_port = out_port, in_port
			# 	flow_write(dp,in_port,out_port,msg.data)
			# 	counter += 1
			# dp.send_msg(out)

		def flow_write(datapath, in_port, out_port, data):
			actions = [parset.OFPActionOutput(port=out_port)]
			self.add_flow(datapath, priority = 1, action = actions)
			out = parser.OFPPacketOut(datapath = datapath,
										buffer_id = ofproto.OFPCML_NO_BUFFER,
										in_port = in_port, actions = actions,
										data = data)
			datapath.send_msg(out)
		'''
		OFPActionOutput class is used with a packet_out message to specify
		the swithc port that you want to send the packet out of.
		Use match to get the physical in_port of the switch. src and dst obtained from the ethernet.
		'''
		# actions = [xr.OFPActionOutput(out_port)]
		# out = ofp_parser.OFPPacketOut(datapath = dp, buffer_id =  msg.buffer_id, in_port = in_port, actions=actions)
		# dp.send_msg(out)
