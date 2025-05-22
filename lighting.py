from stupidArtnet import StupidArtnet

target_ip = "192.168.0.59"
universe = 0
packet_size = 255
artnet_instance = StupidArtnet(target_ip, universe, packet_size, 30, True, True, port=6455)


def set_single_value(dmx_ch, value):
    artnet_instance.set_single_value(dmx_ch, value)
    artnet_instance.show()
