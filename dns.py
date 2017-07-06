#!/usr/bin/env python3
"""
    Implementação de um sistema de nomeação similar ao DNS
    Cada objeto NameServer representaria um servidor real

    Implementação do lookup iterativo
"""
import json
import socket
import threading
from typing import List

class NameServer(threading.Thread):
    """
    Descreve um domínio, que pode conter subdomínios
    """
    def __init__(self, name: str, host: str, port: int):
        super(NameServer, self).__init__()
        self.name = name
        self.address = '{}:{}'.format(host, port)
        self._host = host
        self._port = port
        self._lut = {} # lookup table para os registros DNS

    def add_record(self, domain: str, address: str):
        """Adiciona um novo subdomínio a este domínio"""
        self._lut[domain] = address

    def name_lookup(self, lookupname: str) -> (bool, str, str):
        """
        #TODO: DOCUMENTAR
        """
        try:
            address = self._lut[lookupname]
            return (True, lookupname, address)
        except KeyError:
            pass
        splitted = lookupname.rsplit('.', 1)
        try:
            address = self._lut[splitted[-1]]
            return (True, splitted[-1], address)
        except KeyError:
            return (False, None, None)

    def handler(self, conn):
        lookupname = conn.recv(1024)
        lookupname = lookupname.decode('utf-8')
        found, nsname, addr = self.name_lookup(lookupname)
        response_content = {
            'found': found,
            'nsname': nsname,
            'addr': addr
        }
        response = json.dumps(response_content)
        conn.sendall(response.encode('utf-8'))

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self._host, self._port))
        sock.listen(4)
        print("Listening on '{}'".format(self.address))
        while True:
            (conn, addrinfo) = sock.accept()
            print('Connected by', addrinfo)
            threading.Thread(target=self.handler, args=(conn,)).start()

class ResolverIter(object):
    """docstring for ResolverIter."""
    def __init__(self):
        super(ResolverIter, self).__init__()
        self._cache = {
            '.': '127.0.0.1:10000'
        }

    def name_lookup(self, lookupname: str) -> str:
        def dolookup(address):
            (host, port) = address.split(':')
            port = int(port)
            with socket.create_connection((host, port)) as conn:
                conn.sendall(lookupname.encode('utf-8'))
                response = conn.recv(1024)
                response = response.decode('utf-8')
            print(response)
            response_content = json.loads(response)
            return response_content
        try:
            address = self._cache[lookupname]
            return address
        except KeyError:
            pass
        rootaddr = self._cache['.']
        response_content = dolookup(rootaddr)
        if not response_content['found']:
            return 'Not found!'
        while response_content['nsname'] != lookupname:
            response_content = dolookup(response_content['addr'])
            if not response_content['found']:
                return 'Not found!'
        # caching
        self._cache[response_content['nsname']] = response_content['addr']
        return response_content['addr']

def main():
    rootNS = NameServer('Root', '127.0.0.1', 10000)
    brNS = NameServer('.br', '127.0.0.1', 10001)
    uemNS = NameServer('uem.br', '127.0.0.1', 10002)
    rootNS.add_record('br', brNS.address)
    brNS.add_record('uem', uemNS.address)
    uemNS.add_record('din', '127.0.0.1:10003')
    rootNS.start()
    brNS.start()
    uemNS.start()
    resolver = ResolverIter()
    print(resolver.name_lookup('din.uem.br'))

if __name__ == '__main__':
    main()
