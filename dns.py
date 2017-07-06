#!/usr/bin/env python3
# coding=utf-8
"""
    Implementação de um sistema de nomeação similar ao DNS
    Cada objeto NameServer representaria um servidor real

    Implementação do lookup iterativo
"""
import json
import logging
import socket
import threading

class NameServer(object):
    """
    Descreve um domínio, que pode conter subdomínios
    """
    def __init__(self, name: str, level: int, host: str, port: int):
        super(NameServer, self).__init__()
        self.name = name
        self.daemon = True
        self.address = '{}:{}'.format(host, port)
        self._level = level
        self._host = host
        self._port = port
        self._lut = {} # lookup table para os registros DNS

    def add_record(self, domain: str, address: str):
        """Adiciona um novo subdomínio a este domínio"""
        self._lut[domain] = address

    def name_lookup(self, lookupname: str) -> (bool, str, str):
        """Faz o lookup do nome requerido.

        Dado o lookupname verifica se o endereço do nome requerido está
        na tabela de lookup. Se o endereço não for encontrado, verifica
        qual servidor de nome responde pelo domínio requerido e encaminha
        o endereço do mesmo. Se não encontrar um servidor de nomes que
        responda pelo domínio, retorna que o nome não foi encontrado.
        A estrutura de retorno é uma tripla, sendo o primeiro campo uma
        flag para indicar se encontrou algum registro que responda pelo
        endereço, o segundo é nome do domínio e o terceiro é o endereço.
        """
        try:
            address = self._lut[lookupname]
            return (True, lookupname, address)
        except KeyError:
            pass
        splitted = lookupname.split('.')
        domain = '.'.join(splitted[-self._level:])
        try:
            address = self._lut[domain]
            return (True, domain, address)
        except KeyError:
            return (False, None, None)

    def handler(self, conn):
        """ Executa uma Thread de resolução de nomes.

        Quando uma requisição de resolver um nome é feita, uma nova Thread é criada e 
        esta irá buscar pela resolução do nome requisitado.
        """
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
        """ Executa o servidor

        Função principal do servidor, mantém o servidor ativo até que uma interrupção de teclado ocorra
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((self._host, self._port))
            sock.listen(4)
            logging.info("Listening on '%s'", self.address)
            try:
                while True:
                    (conn, addrinfo) = sock.accept()
                    logging.info("Connected by '%s'", addrinfo)
                    threading.Thread(target=self.handler, args=(conn,)).start()
            except KeyboardInterrupt:
                pass

class ResolverIter(object):
    """Classe que representa um processo de resolução de nomes pelo método iterativo"""
    def __init__(self):
        super(ResolverIter, self).__init__()
        self._cache = {
            '.': '127.0.0.1:10000'
        }

    def name_lookup(self, lookupname: str) -> str:
        """ Resolve um nome e retorna um objeto JSON com sua resolução """

        def dolookup(address):
            """ Solicita uma resolução com o servidor no endereço address no formato ip:porta
            
            Retorna o valor respondido pela conexão """
            (host, port) = address.split(':')
            port = int(port)
            with socket.create_connection((host, port)) as conn:
                conn.sendall(lookupname.encode('utf-8'))
                response = conn.recv(1024)
                response = response.decode('utf-8')
            logging.info('Response: %s', response)
            response_content = json.loads(response)
            return response_content

        logging.info("Resolvendo '%s'", lookupname)
        try:
            address = self._cache[lookupname]
            logging.info("Endereço encontrado em cache '%s'", address)
            return address
        except KeyError:
            pass
        rootaddr = self._cache['.']
        response_content = dolookup(rootaddr)
        if not response_content['found']:
            logging.info("Endereço não encontrado!")
            return 'Não encontrado!'
        while response_content['nsname'] != lookupname:
            response_content = dolookup(response_content['addr'])
            if not response_content['found']:
                logging.info("Endereço não encontrado!")
                return 'Não encontrado!'
        logging.info("Endereço encontrado '%s'", response_content['addr'])
        # caching
        self._cache[response_content['nsname']] = response_content['addr']
        return response_content['addr']
