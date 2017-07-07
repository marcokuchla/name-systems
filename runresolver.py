#!/usr/bin/env python3
# coding=utf-8
"""Executa o resolvedor de nomes."""
import logging
import dns

def main():
    logging.basicConfig(
        format='[%(levelname)s] %(message)s',
        level=logging.INFO)
    resolver = dns.ResolverIter()
    address = resolver.name_lookup('din.uem.br')
    print('Endereço:', address)
    print()
    address = resolver.name_lookup('din.uem.br')
    print('Endereço:', address)
    print()
    address = resolver.name_lookup('deq.uem.br')
    print('Endereço:', address)
    print()
    address = resolver.name_lookup('mail.uem.br')
    print('Endereço:', address)
    print()

if __name__ == '__main__':
    main()
