#!/usr/bin/env python3
# coding=utf-8
import logging
import dns

def main():
    logging.basicConfig(
        format='[%(levelname)s]%(threadName)s %(message)s',
        level=logging.INFO)
    rootNS = dns.NameServer('Root', 1, '127.0.0.1', 10000)
    rootNS.add_record('br', '127.0.0.1:10001')
    rootNS.run()

if __name__ == '__main__':
    main()
