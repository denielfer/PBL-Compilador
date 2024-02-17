# Analisador Léxico
Referente a resolução do Problema 1 - O Caos no Reino das Palavras Perdidas, para a disciplina MI - Processamento de Linguagem de Programação(EXA869) da Universidade Estadual de Feira de Santana. Desenvolvido em python versão: 3.10.4. Testes feitos em Windowns 11, versão 22H2 ( Compilação do Sistema Operacional 22621.2134 ) e ubuntu 22.04.

# Analisador Sintatico
Referente a resolução do Problema 3 - Analisador Sintático, para a disciplina MI - Processamento de Linguagem de Programação(EXA869) da Universidade Estadual de Feira de Santana. Desenvolvido em python versão: 3.10.4. Testes feitos em Windowns 11, versão versão 22H2 ( Compilação do Sistema Operacional 22621.2715 ) e ubuntu 22.04.

# Analisador Semantico

Referente a resolução do Problema 3 - Analisador Semantico, para a disciplina MI - Processamento de Linguagem de Programação(EXA869) da Universidade Estadual de Feira de Santana. Desenvolvido em python versão: 3.10.12. Testes feitos em Windowns 11, versão versão 22H2 ( Compilação do Sistema Operacional 22621.3155 ) e ubuntu 22.04.

Nota: Para o extends foi implementado usando copia dos dados da classe mae, no qual os dados da classe mae são copiada para a classe filha.

## Grupo formado por
- Daniel Fernandes Campos
- João Pedro Rios Carvalho

## Execução do código
Para executar o código do problema basta utilizar o comando abaixo na pasta raíz:
`python main.py`
caso não funcione, tente:
`python3 main.py`

Este arquivo fará a leitura de todos os arquivos .txt presentes na pasta *files*,excluindo os com terminação '-saida.txt'. Após isso, serão gerados arquivos de saídas para cada um deles e armazenado os logs de execução do analisador lexico em no arquivo 'log_execução_lexico.txt' e os logs de execução do analisador sintatico em 'log_execução_sintatico.txt', ambos na pasta raíz.

é nescessario que a pasta *files* exista.