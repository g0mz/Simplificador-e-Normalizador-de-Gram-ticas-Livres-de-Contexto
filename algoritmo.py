import re
from collections import defaultdict

def ler_gramatica(arquivo):
    gramatica = defaultdict(list)
    with open(arquivo, 'r', encoding='utf-8') as f:
        for linha in f:
            linha = linha.strip()
            if '->' in linha:
                esquerda, direita = linha.split('->')
                esquerda = esquerda.strip()
                producoes = [p.strip() for p in direita.split('|')]
                gramatica[esquerda].extend(producoes)
    return dict(gramatica)

def escrever_gramatica(gramatica, titulo, arquivo):
    with open(arquivo, 'a', encoding='utf-8') as f:
        f.write(f"{titulo}:\n")
        for nt, prods in gramatica.items():
            f.write(f"{nt} -> {' | '.join(prods)}\n")
        f.write("\n")

def simbolos_alcancaveis(gramatica, inicial='S'):
    alc = set([inicial])
    mudou = True
    while mudou:
        mudou = False
        for s in list(alc):
            for prod in gramatica.get(s, []):
                for c in prod:
                    if c.isupper() and c not in alc:
                        alc.add(c)
                        mudou = True
    return alc

def remover_inalcancaveis(gramatica, inicial='S'):
    alc = simbolos_alcancaveis(gramatica, inicial)
    return {nt: [p for p in prods if all(c not in gramatica or c in alc for c in p)]
            for nt, prods in gramatica.items() if nt in alc}

def simbolos_uteis(gramatica):
    uteis = set()
    mudou = True
    while mudou:
        mudou = False
        for nt, prods in gramatica.items():
            for p in prods:
                if all(c.islower() or c in uteis for c in p):
                    if nt not in uteis:
                        uteis.add(nt)
                        mudou = True
    return uteis

def remover_inuteis(gramatica):
    uteis = simbolos_uteis(gramatica)
    return {nt: [p for p in prods if all(c.islower() or c in uteis for c in p)]
            for nt, prods in gramatica.items() if nt in uteis}

def encontrar_anulaveis(gramatica):
    anulaveis = set()
    mudou = True
    while mudou:
        mudou = False
        for nt, prods in gramatica.items():
            for p in prods:
                if p == 'ε' or all(c in anulaveis for c in p):
                    if nt not in anulaveis:
                        anulaveis.add(nt)
                        mudou = True
    return anulaveis

def remover_producoes_vazias(gramatica):
    anulaveis = encontrar_anulaveis(gramatica)
    nova = defaultdict(set)
    for nt, prods in gramatica.items():
        for p in prods:
            alternativas = set([''])
            for c in p:
                if c in anulaveis:
                    alternativas = {a + '' + b for a in alternativas for b in [c, '']}
                else:
                    alternativas = {a + c for a in alternativas}
            alternativas = {alt if alt else 'ε' for alt in alternativas}
            nova[nt].update(alternativas)
    for nt in nova:
        if 'ε' in nova[nt] and any(p != 'ε' for p in nova[nt]):
            nova[nt].remove('ε')
    return {k: list(v) for k, v in nova.items()}

def remover_unitarias(gramatica):
    unitarias = defaultdict(set)
    for nt in gramatica:
        unitarias[nt].add(nt)
    mudou = True
    while mudou:
        mudou = False
        for nt, prods in gramatica.items():
            for p in prods:
                if p.isupper():
                    if p not in unitarias[nt]:
                        unitarias[nt].add(p)
                        mudou = True
    nova = defaultdict(list)
    for nt in gramatica:
        for u in unitarias[nt]:
            for p in gramatica.get(u, []):
                if not (p.isupper() and len(p) == 1):
                    nova[nt].append(p)
    return dict(nova)

def chomsky_normal_form(gramatica):
    novas_regras = {}
    term_map = {}
    contador = 1
    for nt, prods in gramatica.items():
        novas_prods = []
        for p in prods:
            if len(p) == 1 and p.islower():
                novas_prods.append(p)
            else:
                nova = ''
                for c in p:
                    if c.islower():
                        if c not in term_map:
                            novo_nt = f"T{contador}"
                            term_map[c] = novo_nt
                            novas_regras[novo_nt] = [c]
                            contador += 1
                        nova += term_map[c]
                    else:
                        nova += c
                while len(nova) > 2:
                    novo_nt = f"X{contador}"
                    novas_regras[novo_nt] = [nova[:2]]
                    nova = novo_nt + nova[2:]
                    contador += 1
                novas_prods.append(nova)
        novas_regras[nt] = novas_prods
    return novas_regras

def greibach_normal_form(gramatica):
    novas = defaultdict(list)
    for nt, prods in gramatica.items():
        for p in prods:
            if p[0].islower():
                novas[nt].append(p)
            else:
                novas[nt].append("a" + p)
    return dict(novas)

def fatorar_esquerda(gramatica):
    fatorada = {}
    for nt, prods in gramatica.items():
        prefixos = defaultdict(list)
        for p in prods:
            if len(p) > 0:
                prefixos[p[0]].append(p)
        if all(len(v) == 1 for v in prefixos.values()):
            fatorada[nt] = prods
        else:
            fatorada[nt] = []
            for k, lista in prefixos.items():
                if len(lista) == 1:
                    fatorada[nt].append(lista[0])
                else:
                    novo = nt + "'"
                    fatorada[nt].append(k + novo)
                    fatorada[novo] = [p[1:] or 'ε' for p in lista]
    return fatorada

def remover_recursao_esquerda(gramatica):
    novas = {}
    for nt, prods in gramatica.items():
        rec = [p[1:] for p in prods if p.startswith(nt)]
        nao_rec = [p for p in prods if not p.startswith(nt)]
        if rec:
            novo = nt + "'"
            novas[nt] = [p + novo for p in nao_rec]
            novas[novo] = [r + novo for r in rec] + ['ε']
        else:
            novas[nt] = prods
    return novas

def main():
    gramatica = ler_gramatica('gramatica.txt')
    with open('saida.txt', 'w') as f: f.write("")

    escrever_gramatica(gramatica, "Gramática Original", 'saida.txt')

    g1 = remover_inalcancaveis(gramatica)
    escrever_gramatica(g1, "Após remoção de símbolos inalcançáveis", 'saida.txt')

    g2 = remover_inuteis(g1)
    escrever_gramatica(g2, "Após remoção de símbolos inúteis", 'saida.txt')

    g3 = remover_producoes_vazias(g2)
    escrever_gramatica(g3, "Após remoção de produções vazias (ε)", 'saida.txt')

    g4 = remover_unitarias(g3)
    escrever_gramatica(g4, "Após remoção de produções unitárias", 'saida.txt')

    g_chomsky = chomsky_normal_form(g4)
    escrever_gramatica(g_chomsky, "Forma Normal de Chomsky", 'saida.txt')

    g_greibach = greibach_normal_form(g4)
    escrever_gramatica(g_greibach, "Forma Normal de Greibach (simples)", 'saida.txt')

    g_fatorada = fatorar_esquerda(g4)
    escrever_gramatica(g_fatorada, "Após fatoração à esquerda", 'saida.txt')

    g_sem_rec = remover_recursao_esquerda(g4)
    escrever_gramatica(g_sem_rec, "Após remoção de recursão à esquerda", 'saida.txt')

if __name__ == "__main__":
    main()
