#!/usr/bin/env python3
# coding=utf-8
"""
    Implementação de um sistema de nomeação similar ao DNS
    Cada objeto NameServer representaria um servidor de nomes real.

    Implementação do lookup iterativo.
"""
import json
import logging
import socket
import threading

class NameServer(object):
    """
    Descreve um domínio, que pode conter subdomínios.

    Argumentos:
    name -- Nome do servidor.
    level -- Valor que representa o nível hierárquico desse servidor.
        A raiz tem level 1, os filhos do servidor raiz tem level 2, os filhos
        dos filhos level 3, e assim por diante.
    host -- Endereço IP do servidor.
    port -- Porta do servidor.
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
        """Adiciona um novo registro de subdomínio a este domínio.

        Os registros são compostos de um nome de domínio, que é a chave
        para a lookup table (lut) e um endereço no formato 'IP:PORT'.
        """
        self._lut[domain] = address

    def name_lookup(self, lookupname: str) -> (bool, str, str):
        """Faz o lookup do nome requerido.

        Dado o lookupname verifica se o endereço do nome requerido está
        na tabela de lookup. Se o endereço não for encontrado, verifica
        qual servidor de nome pode responder o endereço requerido e
        encaminha o endereço do mesmo. Se não encontrar um servidor de
        nomes que responda pelo domínio, retorna que o nome não foi
        encontrado. A estrutura de retorno é uma tripla, sendo o primeiro
        campo uma flag para indicar se encontrou algum registro que
        responde pelo endereço, o segundo é nome do domínio e o terceiro
        é o endereço correspondente ao domínio.
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
        """Trata uma requisição do cliente.

        Quando um resolvedor conecta no servidor, uma nova Thread é
        criada para gerenciar a conexão estabelecida, e tratar a
        as requisições de resolução de nomes.
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
        """Executa o servidor

        Função principal do servidor, mantém o servidor ativo aguardando
        conexões ou para quando ocorre uma interrupção de teclado.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((self._host, self._port))
            sock.listen(4) # aceita até 4 conexões simultâneas
            logging.info("Listening on '%s'", self.address)
            try:
                while True:
                    (conn, addrinfo) = sock.accept()
                    logging.info("Connected by '%s'", addrinfo)
                    threading.Thread(target=self.handler, args=(conn,)).start()
            except KeyboardInterrupt:
                pass

class ResolverIter(object):
    """Resolvedor de nomes pelo método iterativo."""
    def __init__(self):
        super(ResolverIter, self).__init__()
        self._cache = {
            '.': '127.0.0.1:10000'
        }

    def name_lookup(self, lookupname: str) -> str:
        """Resolve um nome e retorna um objeto JSON com sua resolução."""

        def dolookup(address):
            """Solicita uma resolução com o servidor de nomes no endereço
            address no formato ip:porta.

            Retorna o valor respondido pela conexão."""
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
            # Procura primeiramente na cache e se encontrar retorna.
            address = self._cache[lookupname]
            logging.info("Endereço encontrado em cache '%s'", address)
            return address
        except KeyError:
            pass
        # inicia a resolução pelo servidor de nomes raiz
        rootaddr = self._cache['.']
        response_content = dolookup(rootaddr)
        if not response_content['found']:
            # Nome não encontrado retorna erro!
            logging.info("Endereço não encontrado!")
            return 'Não encontrado!'
        # verifica se endereço encontrado é o requerido
        while response_content['nsname'] != lookupname:
            # se não for procura iterativamente pela árvore de servidores.
            response_content = dolookup(response_content['addr'])
            if not response_content['found']:
                logging.info("Endereço não encontrado!")
                return 'Não encontrado!'
        logging.info("Endereço encontrado '%s'", response_content['addr'])
        # Atualiza endereço na cache
        self._cache[response_content['nsname']] = response_content['addr']
        # Retorna  o endereço encontrado
        return response_content['addr']
