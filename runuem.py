#!/usr/bin/env python3
# coding=utf-8
import logging
import dns

def main():
    logging.basicConfig(
        format='[%(levelname)s]%(threadName)s %(message)s',
        level=logging.INFO)
    uemNS = dns.NameServer('uem.br', 3, '127.0.0.1', 10002)
    uemNS.add_record('www.uem.br', '127.0.0.1:10003')
    uemNS.add_record('din.uem.br', '127.0.0.1:10004')
    uemNS.run()

if __name__ == '__main__':
    main()
