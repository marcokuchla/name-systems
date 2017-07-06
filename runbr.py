#!/usr/bin/env python3
# coding=utf-8
import logging
import dns

def main():
    logging.basicConfig(
        format='[%(levelname)s]%(threadName)s %(message)s',
        level=logging.INFO)
    brNS = dns.NameServer('.br', 2, '127.0.0.1', 10001)
    brNS.add_record('uem.br', '127.0.0.1:10002')
    brNS.run()

if __name__ == '__main__':
    main()
