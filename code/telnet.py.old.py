#server user:campUser pass:SecCamp2022?
#from . import tests
from pickle import decode_long
import socket, sys
from struct import pack
from turtle import st

binary_transmission                 = b'\x00'
echo                                = b'\x01'
reconnection                        = b'\x02'
suppress_go_ahead                   = b'\x03'
approx_message_size_negotiation     = b'\x04'
status                              = b'\x05'
timing_mark                         = b'\x06'
remote_controlled_trans_and_echo    = b'\x07'
output_line_width                   = b'\x08'
output_page_size                    = b'\x09'
output_carriage_return_disposition  = b'\x0a'
output_horizontal_tab_stops         = b'\x0b'
output_horizontal_tab_disposition   = b'\x0c'
output_formfeed_disposition         = b'\x0d'
output_vertical_tabstops            = b'\x0e'
output_vertical_tab_disposition     = b'\x0f'
output_linefeed_disposition         = b'\x10'
extended_ascii                      = b'\x11'
logout                              = b'\x12'
byte_macro                          = b'\x13'
data_entry_terminal                 = b'\x14'
supdup                              = b'\x15'
supdup_output                       = b'\x16'
send_location                       = b'\x17'
terminal_type                       = b'\x18'
end_of_record                       = b'\x19'
tacacs_user_identification          = b'\x1a'
output_marking                      = b'\x1b'
terminal_location_number            = b'\x1c'
telnet_3270_regime                  = b'\x1d'
x3_pad                              = b'\x1e'
negotiate_about_window_size         = b'\x1f'
terminal_speed                      = b'\x20'
remote_flow_control                 = b'\x21'
linemode                            = b'\x22'
x_display_location                  = b'\x23'
environment_option                  = b'\x24'
authentication_option               = b'\x25'
encryption_option                   = b'\x26'
new_environment_option              = b'\x27'
tn3270e                             = b'\x28'
xauth                               = b'\x29'
charset                             = b'\x2a'
telnet_remote_serial_port           = b'\x2b'
com_port_control_option             = b'\x2c'
telnet_suppress_local_echo          = b'\x2d'
telnet_start_tls                    = b'\x2e'
kermit                              = b'\x2f'
send_url                            = b'\x30'
forward_x                           = b'\x31'
telopt_pragma_logon                 = b'\x8a'
telopt_sspi_logon                   = b'\x8b'
telopt_pragma_heartbeat             = b'\x8c'

subpotion                           = b'\xfa'
will                                = b'\xfb'
wont                                = b'\xfc'
do                                  = b'\xfd'
dont                                = b'\xfe'

head                                = b'\xff'

suboption_end                       = b'\xff\xf0'
#define argv
if(len(sys.argv) < 3) :
  print('command is "python3 telnet.py [ip adder] [connection port]"')
  sys.exit()

host = sys.argv[1]
port = int(sys.argv[2])

#define socket 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(10)

#connect server
try :
  sock.connect((host, port))
except :
  print('sock session error')
  sys.exit()

print('Connected to remote host \n')

#Packet size allowed to receive
rcv = 1024

#telnet session optioon
packet = head + dont + authentication_option + \
        head + do + suppress_go_ahead + \
        head + will + terminal_type + \
        head + will + negotiate_about_window_size + \
        head + will + terminal_speed + \
        head + dont + remote_flow_control + \
        head + will + linemode + \
        head + dont + new_environment_option + \
        head + dont + status
sock.sendall(packet)
msg = sock.recv(rcv)

packet = head + wont + x_display_location + \
        head + wont + new_environment_option
sock.sendall(packet)
msg = sock.recv(rcv)

#telnet session suboption
sock.sendall(packet)
msg = sock.recv(rcv)

terminal_speed_data = b'\x20\x00\x39\x36\x30\x30\x2c\x39\x36\x30\x30' #9600,9600
terminal_type_data = b'\x18\x00\x58\x54\x45\x52\x4d\x2d\x32\x35\x36\x43\x4f\x4c\x4f\x52' #XTERM-256COLOR

packet = head + subpotion + terminal_speed_data + suboption_end + \
        head + subpotion + terminal_type_data + suboption_end
sock.sendall(packet)
msg = sock.recv(rcv)

packet = head + wont + echo + \
        head + dont + status + \
        head + wont + remote_flow_control
sock.sendall(packet)
msg = sock.recv(rcv)

packet = head + do + echo
sock.sendall(packet)

while True:
  msg = sock.recv(rcv)
  msg_ln = list(msg)
  sys.stdout.buffer.write(msg)
  if msg_ln[-1] == "10":
    continue
  data = input()
  data = data + "\r"
  bdata = data.encode()
  sock.sendall(bdata)