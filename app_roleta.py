# app_roleta.py
import streamlit as st

# --- A CLASSE 'AnalistaRoleta' COMPLETA FICA AQUI ---
class AnalistaRoleta:
    # (A classe AnalistaRoleta não muda, é a mesma de antes)
    def __init__(self):
        self.historico = []
        self.CILINDRO_EUROPEU = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
        self.VIZINHOS = self._calcular_vizinhos()
        self.CAVALOS_TRIPLOS = {
            0: [3, 7], 1: [4, 8], 2: [5, 9], 3: [6, 0], 4: [7, 1],
            5: [8, 2], 6: [9, 3], 7: [0, 4], 8: [1, 5], 9: [2, 6]
        }
        self.JUNCAO_TERMINAIS = {0, 1, 3, 4}
        self.DISFARCADOS = {
            0: {11, 19, 22, 28, 33}, 1: {12, 23, 29, 32, 34},
            2: {11, 13, 24, 31, 35}, 3: {12, 14, 21, 25, 26, 36},
            4: {13, 15, 22, 26, 28, 31}, 5: {14, 16, 23, 27, 32},
            6: {15, 17, 24, 28, 33}, 7: {16, 18, 25, 29, 34},
            8: {17, 19, 24, 26, 35}, 9: {18, 27, 33, 36}
        }

    def _calcular_vizinhos(self):
        vizinhos = {}
        tamanho = len(self.CILINDRO_EUROPEU)
        for i, num in enumerate(self.CILINDRO_EUROPEU):
            vizinhos[num] = {
                "v-2": self.CILINDRO_EUROPEU[(i - 2 + tamanho) % tamanho],
                "v-1": self.CILINDRO_EUROPEU[(i - 1 + tamanho) % tamanho],
                "v+1": self.CILINDRO_EUROPEU[(i + 1) % tamanho],
                "v+2": self.CILINDRO_EUROPEU[(i + 2) % tamanho],
            }
        return vizinhos

    def adicionar_numero(self, numero):
        if 0 <= numero <= 36:
            self.historico.append(numero)
            if len(self.historico) > 20:
                self.historico.pop(0)

    def _get_terminais_recentes(self, quantidade):
        return [n % 10 for n in self.historico[-quantidade:]]
    
    def _checar_cavalos_diretos(self):
        if len(self.historico) < 2: return None
        t1, t2 = self._get_terminais_recentes(2)
        if t1 == t2: return None
        for cabeca, laterais in self.CAVALOS_TRIPLOS.items():
            if set(laterais) == {t1, t2}:
                return {
                    "analise": f"Gatilho 'Cavalos Diretos' Ativado: T{t1} e T{t2} puxando o central.",
                    "estrategia": f"Focar a aposta na região do Terminal {cabeca}."
                }
        return None

    def _checar_continuacao_cavalos(self):
        if len(self.historico) < 2: return None
        terminais_unicos = set(self._get_terminais_recentes(3))
        if len(terminais_unicos) < 2: return None
        for cabeca, laterais in self.CAVALOS_TRIPLOS.items():
            trindade = {cabeca} | set(laterais)
            if len(trindade.intersection(terminais_unicos)) == 2:
                faltante = list(trindade - terminais_unicos)[0]
                return {
                    "analise": f"Gatilho 'Continuação de Cavalos' Ativado: Grupo {{{', '.join(map(str, sorted(list(trindade))))}}} está incompleto.",
                    "estrategia": f"Focar a aposta na região do cavalo faltante: Terminal {faltante}."
                }
        return None

    def _checar_manipulacao_terminal(self):
        if len(self.historico) < 5: return None
        terminais = self._get_terminais_recentes(7)
        terminal_dominante = max(set(terminais), key=terminais.count)
        contagem = terminais.count(terminal_dominante)
        if contagem >= 4:
            if contagem >= 5:
                disfarçados_str = ", ".join(map(str, sorted(list(self.DISFARCADOS[termin