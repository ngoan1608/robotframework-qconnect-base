#  Copyright 2020-2022 Robert Bosch Car Multimedia GmbH
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# *******************************************************************************
#
# File: raw_tcp.py
#
# Initially created by Cuong Nguyen (RBVH/ECM11) / May 2021.
# Based on lib/TCP/Base/CSimpleSocket.py in TML Framework.
#
# Description:
#   Provide the class for Raw TCP client and server connection.
#
# History:
#
# 12.05.2021 / V 0.1 / Cuong Nguyen
# - Initialize
#
# *******************************************************************************
from __future__ import with_statement
from QConnectBase.tcp.tcp_base import BrokenConnError, TCPBase, TCPBaseServer, TCPBaseClient


class RawTCPBase(TCPBase):
   """
   Base class for a raw tcp connection.
   """
   def _read(self):
      """
      Actual method to read message from a tcp connection.
      
      Returns:
         Empty string.
      """
      data = ''
      while 1:
         data = data + self.conn.recv(1).decode(self.config.encoding, 'ignore')

         # Simple socket expects \r\n for terminating a message
         if data[-2:] == "\r\n":
            break

         if data == '':
            raise BrokenConnError("socket connection broken")

      # remove \r\n
      data = data[:-2]
      return data

   def _send(self, msg, cr):
      """
      Actual method to send message to a tcp connection.
      
      Args:
         msg: Message to be sent.
         cr: Determine if it's necessary to add newline character at the end of command.

      Returns:
         None
      """
      sent = 0
      with self._send_lock:
         while sent < len(msg):
            sent += self.conn.send(msg[sent:])
         if cr and msg != "":
            self.conn.send("\r\n")


class RawTCPServer(RawTCPBase, TCPBaseServer):
   """
   Class for a raw tcp connection server.
   """
   _CONNECTION_TYPE = "TCPIPServer"

   def __init__(self, mode=None, config=None):
      """
      Constructor of RawTCPServer class.
      
      Args:
         address: Address of TCP server.
         port: Port number.
      """
      super(RawTCPServer, self).__init__(mode, config)
      self._bind()


class RawTCPClient(RawTCPBase, TCPBaseClient):
   """
   Class for a raw tcp connection client.
   """
   _CONNECTION_TYPE = "TCPIPClient"

   def __init__(self, mode=None, config=None):
      """
      Constructor of RawTCPClient class.
      
      Args:
         address: Address of TCP server.
         port: Port number.
      """
      super(RawTCPClient, self).__init__(mode, config)
