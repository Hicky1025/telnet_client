#server user:campUser pass:SecCamp2022?
import sys, socket
import readchar
import threading

# Telnetのオプションを定義
IAC  = bytes([255]) # "Interpret As Command"
DONT = bytes([254])
DO   = bytes([253])
WONT = bytes([252])
WILL = bytes([251])

SE  = bytes([240])  # Subnegotiation End
NOP = bytes([241])  # No Operation
DM  = bytes([242])  # Data Mark
BRK = bytes([243])  # Break
IP  = bytes([244])  # Interrupt process
AO  = bytes([245])  # Abort output
AYT = bytes([246])  # Are You There
EC  = bytes([247])  # Erase Character
EL  = bytes([248])  # Erase Line
GA  = bytes([249])  # Go AIAC
SB =  bytes([250])  # Subnegotiation Begin

BINARY = bytes([0]) # 8-bit data path
ECHO = bytes([1]) # echo
RCP = bytes([2]) # prepare to reconnect
SGA = bytes([3]) # suppress go ahead
NAMS = bytes([4]) # approximate message size
STATUS = bytes([5]) # give status
TM = bytes([6]) # timing mark
RCTE = bytes([7]) # remote controlled transmission and echo
NAOL = bytes([8]) # negotiate about output line width
NAOP = bytes([9]) # negotiate about output page size
NAOCRD = bytes([10]) # negotiate about CR disposition
NAOHTS = bytes([11]) # negotiate about horizontal tabstops
NAOHTD = bytes([12]) # negotiate about horizontal tab disposition
NAOFFD = bytes([13]) # negotiate about formfeed disposition
NAOVTS = bytes([14]) # negotiate about vertical tab stops
NAOVTD = bytes([15]) # negotiate about vertical tab disposition
NAOLFD = bytes([16]) # negotiate about output LF disposition
XASCII = bytes([17]) # extended ascii character set
LOGOUT = bytes([18]) # force logout
BM = bytes([19]) # byte macro
DET = bytes([20]) # data entry terminal
SUPDUP = bytes([21]) # supdup protocol
SUPDUPOUTPUT = bytes([22]) # supdup output
SNDLOC = bytes([23]) # send location
TTYPE = bytes([24]) # terminal type
EOR = bytes([25]) # end or record
TUID = bytes([26]) # TACACS user identification
OUTMRK = bytes([27]) # output marking
TTYLOC = bytes([28]) # terminal location number
VT3270REGIME = bytes([29]) # 3270 regime
X3PAD = bytes([30]) # X.3 PAD
NAWS = bytes([31]) # window size
TSPEED = bytes([32]) # terminal speed
LFLOW = bytes([33]) # remote flow control
LINEMODE = bytes([34]) # Linemode option
XDISPLOC = bytes([35]) # X Display Location
OLD_ENVIRON = bytes([36]) # Old - Environment variables
AUTHENTICATION = bytes([37]) # Authenticate
ENCRYPT = bytes([38]) # Encryption option
NEW_ENVIRON = bytes([39]) # New - Environment variables

TN3270E = bytes([40]) # TN3270E
XAUTH = bytes([41]) # XAUTH
CHARSET = bytes([42]) # CHARSET
RSP = bytes([43]) # Telnet Remote Serial Port
COM_PORT_OPTION = bytes([44]) # Com Port Control Option
SUPPRESS_LOCAL_ECHO = bytes([45]) # Telnet Suppress Local Echo
TLS = bytes([46]) # Telnet Start TLS
KERMIT = bytes([47]) # KERMIT
SEND_URL = bytes([48]) # SEND-URL
FORWARD_X = bytes([49]) # FORWARD_X
PRAGMA_LOGON = bytes([138]) # TELOPT PRAGMA LOGON
SSPI_LOGON = bytes([139]) # TELOPT SSPI LOGON
PRAGMA_HEARTBEAT = bytes([140]) # TELOPT PRAGMA HEARTBEAT

# set telnet packet
first_packet = IAC + DONT + AUTHENTICATION + \
              IAC + DONT + SGA + \
              IAC + WILL + TTYPE + \
              IAC + DONT + NAWS + \
              IAC + WILL + TSPEED + \
              IAC + DONT + LFLOW + \
              IAC + DONT + LINEMODE + \
              IAC + DONT + NEW_ENVIRON + \
              IAC + DONT + STATUS

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 受信パケットのデータの最大サイズ
data_size = 1024

def recv():
  while True:
    packet = b''
    recv_packet = sock.recv(data_size)
    
    if IAC + DO + XDISPLOC in recv_packet:
      packet = packet + IAC + WONT + XDISPLOC
    if IAC + DO + NEW_ENVIRON in recv_packet:
      packet = packet + IAC + WONT + NEW_ENVIRON
    if IAC + DO + SGA in recv_packet:
      packet = packet + IAC + WONT + SGA
    if IAC + WILL + SGA in recv_packet:
      packet = packet + IAC + DONT + SGA
    if IAC + DO + ECHO in recv_packet:
      packet = packet + IAC + WONT + ECHO
    if IAC + DO + NAWS in recv_packet:
      packet = packet + IAC + WONT + NAWS
    if IAC + WILL + STATUS in recv_packet:
      packet = packet + IAC + DONT + STATUS
    if IAC + DO + LFLOW in recv_packet:
      packet = packet + IAC + WONT + LFLOW
    if IAC + SB + TSPEED in recv_packet:
      packet = packet + IAC + SB + TSPEED + b'9600,9600' + IAC + SE
    if IAC + SB + TTYPE in recv_packet:
      packet = packet + IAC + SB + TTYPE + b'\x00' + b'XTERM-256COLOR' + IAC + SE
    if IAC not in recv_packet and packet == b'':
      sys.stdout.buffer.write(recv_packet)
    else:
      sock.sendall(packet)
  
def input():
  while True:
    try:
      string = readchar.readkey()
      if string == '\n':
        sock.sendall(b'\r\n')
        continue
      sock.sendall(string.encode())
    except KeyboardInterrupt:
      sys.exit()

def main():
  # if(len(sys.argv) < 3) :
  #   print('command is 'python3 telnet.py [ip adder] [connection port]'')
  #   sys.exit
  # ip_add = sys.argv[1]
  # tel_port = int(sys.argv[2])

  ip_add = '20.194.222.82'
  tel_port = 23

  # Socketを用いたTCPセッションの確立
  sock.settimeout(5)

  try :
    sock.connect((ip_add, int(tel_port)))
  except :
    # 接続失敗メッセージの出力　確立
    print('sock session timeout error...')
    sys.exit()

  # 接続成功メッセージの出力
  print('Connected to remote host!!\n')

  sock.sendall(first_packet)

  t1 = threading.Thread(target=recv)
  t1.start()

  t2 = threading.Thread(target=input)
  t2.start()

if __name__ == '__main__':
  main()