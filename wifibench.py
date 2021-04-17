#!/usr/bin/env python3
import sys, socket, random, time, threading
import os, signal, argparse

class Client:
   def __init__(self, server, port=3050, size=1024):
      self.port=port
      self.server=server
      self.packetsize = size
      self.counter=0
      self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
      self.do_run=True

   def start(self):
      print('Client mode started')
      try:
         self.thread = threading.Thread(target=self.status).start()
         self.socket.connect( (self.server, self.port) )
         while self.do_run:
            recv = self.socket.recv(self.packetsize*1024)
            self.counter += len(recv)
      except TypeError:
         self.do_run=False
         return

   def status(self):
      while True:
         x=self.counter
         self.wait(5)
         if not self.do_run: break
         x2=(self.counter-x) / 5
         unit='b'
         if x2 >= 1048576:
            x2 = round(x2 / 1048576, 2)
            unit='Mb'
         elif x2 >= 1024:
            x2 = round(x2 /1024, 2)
            unit='Kb'
         bit=x2*8
         print(f'{x2} {unit}yte/s - {bit}{unit}it/s')
         
   def wait(self, s):
      start=time.time()
      while time.time() - start < s:
         if not self.do_run: break
         time.sleep(0.5)
      



class Server:
   def __init__(self, port=3050, size=512):
      self.port=port
      self.datasize = size
      self.do_run=True
      self.rand_data=os.urandom(self.datasize * 1024)

   def send(self, c, addr):
      print('New connection from', addr[0])
      try:
         while self.do_run:
            c.send(self.rand_data)
         c.close()
         self.stop()
      except ConnectionResetError:
         print('Connection closed')

   def socket_setup(self):
      self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
      self.socket.bind( ('', self.port) )
      self.socket.settimeout(0.5)
      self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

   def start(self):
      print('Server mode started')
      self.socket_setup()
      self.start_server()

   def start_server(self):
      while self.do_run:
         try:
            self.socket.listen(1)
            c, addr = self.socket.accept()
         except socket.timeout:
            continue
         self.send(c, addr)
      self.stop()

   def stop(self):
      try:
         self.socket.shutdown(1)
         self.socket.close()
      except Exception as e:
         print('server shutdown failed: '+e)
      sys.exit(0)

def get_args():
   parser = argparse.ArgumentParser()
   group = parser.add_mutually_exclusive_group()
   group.add_argument('-s', '--server', help='Server mode', action='store_true')
   group.add_argument('-c', '--client', help='Client mode', metavar='<server address>')
   parser.add_argument('-p', '--port', help='Port number', default='3050', type=int)
   return vars(parser.parse_args())

def main():
   global mode   
   signal.signal(signal.SIGTERM, shutdown)
   signal.signal(signal.SIGINT, shutdown)

   args = get_args()

   if args['server']:
      mode = Server(size=512, port=args['port'])
   if not args['client'] == None:
      mode = Client(args['client'], size=512, port=args['port'])
   mode.start()

def shutdown(a, b):
   global mode
   print('Shutdown')
   mode.do_run=False

def wbhelp():
   print (f'usage: {sys.argv[0]} -m <client|server> -h <host> -p <port>')

main()
