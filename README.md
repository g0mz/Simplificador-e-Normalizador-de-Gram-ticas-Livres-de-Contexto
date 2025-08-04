# Simplificador e Normalizador de Gramáticas Livres de Contexto

## Descrição

Este projeto implementa um simplificador e normalizador de gramáticas livres de contexto (GLC) em Python. O programa recebe uma gramática no formato textual, realiza a simplificação e normalização da gramática, aplicando transformações como remoção de símbolos inalcançáveis, inúteis, produções vazias (ε), e unitárias. Além disso, a gramática é convertida para as formas normais de Chomsky e Greibach, com a possibilidade de realizar melhorias como fatoração à esquerda e remoção de recursão à esquerda.

## Funcionamento

1. **Entrada da Gramática**: A gramática é fornecida em um arquivo `gramatica.txt`, onde cada produção é representada no formato `S -> aAa | bBv`, com as produções separadas por `|`.
   
2. **Transformações**:
    - **Remoção de símbolos inalcançáveis**: Elimina os símbolos que não podem ser alcançados a partir do símbolo inicial.
    - **Remoção de símbolos inúteis**: Remove os símbolos que não geram nenhuma string terminal.
    - **Remoção de produções vazias (ε)**: Elimina produções que geram a string vazia.
    - **Remoção de produções unitárias**: Substitui produções unitárias (do tipo `A -> B`).
    - **Forma Normal de Chomsky (CNF)**: Converte a gramática para a forma normal de Chomsky, onde cada produção tem no máximo dois símbolos no lado direito.
    - **Forma Normal de Greibach (GNF)**: Converte a gramática para a forma normal de Greibach, onde as produções começam com um terminal seguido de um não-terminal.
    - **Fatoração à esquerda**: Aplica a fatoração à esquerda nas produções da gramática.
    - **Remoção de recursão à esquerda**: Elimina recursões à esquerda, transformando-as em recursões à direita.

3. **Saída**: O programa gera um arquivo `saida.txt` contendo a gramática original e a gramática após cada transformação.

## Exemplo de Uso

### Exemplo de Arquivo de Entrada (gramatica.txt)

```txt
S -> aAa | bBv
A -> a | aA
B -> A | ε
```
### Execução
Execute o programa com o seguinte comando:

```
 python algoritmo.py
```

### Exemplo de Saída (saida.txt)

```
Gramática Original:
S -> aAa | bBv
A -> a | aA
B -> A | ε

Após remoção de símbolos inalcançáveis:
S -> aAa | bBv
A -> a | aA
B -> A | ε

Após remoção de símbolos inúteis:
S -> aAa
A -> a | aA
B -> A | ε

Após remoção de produções vazias (ε):
S -> aAa
A -> a | aA

Após remoção de produções unitárias:
S -> aAa
A -> a | aA
```

## Conclusão

Este projeto tem como objetivo fornecer uma ferramenta para simplificar e normalizar gramáticas livres de contexto, facilitando a análise e manipulação de gramáticas em Teoria da Computação.
