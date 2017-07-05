'''
    Implementação de um sistema de nomeação similar ao DNS
    Cada objeto NameServer representaria um servidor real

    Implementação do lookup iterativo
'''
from typing import List

class NameServer(object):
    '''
    Descreve um domínio, que pode conter subdomínios
    '''
    def __init__(self, name: str):
        super(NameServer, self).__init__()
        self.name = name
        self._lut = {} # lookup table para os registros DNS

    def add_record(self, domain: str, address: str):
        '''Adiciona um novo subdomínio a este domínio'''
        self._lut[domain] = address

    def name_lookup(self, lookupname: str) -> (bool, str, str):
        '''
        nome da forma a.b.c.d._name retorna como a.b.c.d
        nome da forma a.b.c.d.e retorna como nulo, ie. o nome não é valido
        para este domínio

        Se o retorno for válido, também retorna os subdomínios para o próximo lookup

        O terceiro parâmetro de retorno determina se o retorno foi ou não válido,
            isto é, se o lookup foi consumido corretamente
        '''
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
            return (False, None)

class ResolverIter(object):
    """docstring for ResolverIter."""
    def __init__(self):
        super(ResolverIter, self).__init__()
        self._cache = {}

    def name_lookup(self, lookupname: str) -> str:
        pass
