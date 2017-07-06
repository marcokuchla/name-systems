ARQUIVO <dnsserver.py>
    * Contém um simulador de DNS implementado com a dnslib
    * Não contém uma implementação interna dos algoritmos de resolução de nome
    * Compatível com buscas pelo programa `dig`
    * FONTE: https://gist.github.com/samuelcolvin/ca8b429504c96ee738d62a798172b046

    COMO UTILIZAR:
    Em terminais distintos:
        $ python3 dnsserver.py
        $ dig example.com

ARQUIVOS <dns_server_iter.py> e <dns_server_recur.py>
    * Contém uma implementação "naive" da resolução de nomes iterativa e recursiva
    * Executar qualquer um deles irá imprimir a resolução dos nomes de acordo com cada algorítmo

ARQUIVOS <dns.py>, <runbr.py>, <runresolver.py>, <runroot.py>, <runuem.py>
    * Implementam uma resolução de nomes distribuída e iterativa
    * Cada arquivo <run*.py> é um servidor separado
    * <dns.py> é uma biblioteca
    
    COMO UTILIZAR:
    * Primeiro, executar os programas <runbr.py>, <runuem.py> e <runroot.py> em terminais separados
    * Depois executar <runresolver.py> em um quarto terminal
    * Cada terminal irá imprimir sua interação com os outros terminais enquanto runresolver.py requisita a resolução de múltiplos nomes
