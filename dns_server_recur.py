#!/usr/bin/env python3
#-*- coding: utf8 -*-
'''
    Implementação de um sistema de nomeação similar ao DNS
    Cada objeto NameServer representaria um servidor real

    Implementação do lookup recursivo
'''

from typing import List


class NameServer:
    '''
    Descreve um domínio, que pode conter subdomínios
    '''
    _name: str = ''
    _subdomains: List['NameServer'] = []

    def __init__(self, name: str, subdomains: List['NameServer'] = []):
        self._name = name
        self._subdomains = subdomains

    def get_name(self) -> str:
        return self._name

    def add_sub_domain(self, subdomain: 'NameServer'):
        '''Adiciona um novo subdomínio a este domínio'''
        self._subdomains.append(subdomain)

    def name_lookup(self, lookupname: str, level: int = 1) -> bool:
        '''
        retorna True se o nome for encontrado dentro de algum subdominio, False se não

        Em uma implementação real, poderia retornar a identidade da Entidade, ou chamar um callback
        '''
        if lookupname == self._name:
            return True

        splitname = lookupname.split('.')
        if splitname[-1] == self._name:
            for domain in self._subdomains:
                print('  ' * level + 'Domínio: ' + domain.get_name())
                print('  ' * level + 'Nome a buscar: ' +
                      '.'.join(splitname[:-1]))
                ret = domain.name_lookup('.'.join(splitname[:-1]), level + 1)
                if ret:
                    print('  ' * level + 'Encontrado.')
                    return True

        print('  ' * level + 'Não encontrado.')
        return False


# Cada Objeto representa uma instância de um servidor
DIN = NameServer('din')
DAA = NameServer('daa')
UEM = NameServer('uem', [DAA, DIN])
UOL = NameServer('uol')
BRASIL = NameServer('br', [UOL, UEM])

URL = 'din.uem.br'

print('=' * 20)
print('Name Server Recursivo')
print('=' * 20)
print()
print('Servidor Raíz: ' + BRASIL.get_name())
print('Nome a buscar: ' + URL)
BRASIL.name_lookup(URL)
