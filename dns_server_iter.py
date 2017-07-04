#!/usr/bin/env python3
#-*- coding: utf8 -*-
'''
    Implementação de um sistema de nomeação similar ao DNS
    Cada objeto NameServer representaria um servidor real

    Implementação do lookup iterativo
'''

from typing import List


class NameServer:
    '''
    Descreve um domínio, que pode conter subdomínios
    '''
    _name = ''
    _subdomains = []

    def __init__(self, name: str, subdomains: List['NameServer'] = []):
        self._name = name
        self._subdomains = subdomains

    def get_name(self) -> str:
        return self._name

    def add_sub_domain(self, subdomain: 'NameServer'):
        '''Adiciona um novo subdomínio a este domínio'''
        self._subdomains.append(subdomain)

    def name_lookup(self, lookupname: str) -> (str, List['NameServer'], bool):
        '''
        nome da forma a.b.c.d._name retorna como a.b.c.d
        nome da forma a.b.c.d.e retorna como nulo, ie. o nome não é valido para este domínio

        Se o retorno for válido, também retorna os subdomínios para o próximo lookup

        O terceiro parâmetro de retorno determina se o retorno foi ou não válido,
            isto é, se o lookup foi consumido corretamente
        '''
        splitname = lookupname.split('.')
        if splitname[-1] == self._name:
            return '.'.join(splitname[:-1]), self._subdomains, True

        return '', [], False


# Cada Objeto representa uma instância de um servidor
DIN = NameServer('din')
DAA = NameServer('daa')
UEM = NameServer('uem', [DAA, DIN])
UOL = NameServer('uol')
BRASIL = NameServer('br', [UEM, UOL])


def lookup_names(url: str, root: NameServer, level: int = 0) -> bool:
    print('  ' * level + '-' * 20)
    print('  ' * level + 'Nome atual: ' + url)
    print('  ' * level + 'Domínio: ' + root.get_name())

    new_url, subdomains, found = root.name_lookup(url)
    print('  ' * level + ('Encontrado. Novo Nome: ' + new_url
                          if found else 'Não encontrado'))
    print('  ' * level + '-' * 20)

    if new_url != '':
        for domain in subdomains:
            if lookup_names(new_url, domain, level + 1):
                break

    return found


URL = 'din.uem.br'

print('=' * 20)
print('Name Server Iterativo')
print('=' * 20)
print()
lookup_names(URL, BRASIL)
