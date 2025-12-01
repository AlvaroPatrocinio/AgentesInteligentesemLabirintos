# 🧠 Inteligência Artificial: Agentes em Labirintos

> Trabalho Prático de Implementação de Agentes Inteligentes para Resolução de Labirintos.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![AI](https://img.shields.io/badge/AI-Search%20%26%20RL-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Concluído-green?style=for-the-badge)

## 📋 Sobre o Projeto

Este projeto implementa e compara o desempenho de **5 tipos de agentes inteligentes** em ambientes de labirinto. [cite_start]O objetivo é demonstrar na prática diferentes paradigmas de Inteligência Artificial, desde reflexos simples sem memória até algoritmos de busca otimizada (A*) e aprendizado por reforço (Q-Learning)[cite: 17, 18, 24].

O sistema é capaz de ler arquivos de texto representando labirintos, identificar pontos de partida e chegada, e executar baterias de testes automatizados.

## 🤖 Agentes Implementados

Conforme as especificações do trabalho, foram desenvolvidos os seguintes agentes:

1.  [cite_start]**Agente Reativo Simples** [cite: 19, 27]
    * **Lógica:** Toma decisões baseadas apenas na percepção imediata (célula atual). Escolhe aleatoriamente um vizinho válido.
    * **Limitação:** Não possui memória, podendo ficar preso em loops infinitos ou "ping-pong" entre células.

2.  [cite_start]**Agente Reativo Baseado em Modelo** [cite: 20, 27]
    * **Lógica:** Mantém um estado interno (memória) das células já visitadas. Prioriza células novas para evitar loops imediatos.
    * **Melhoria:** Consegue sair de situações simples onde o agente reativo falharia, mas ainda não realiza planejamento de longo prazo.

3.  [cite_start]**Agente Baseado em Objetivo (Busca Cega)** [cite: 21, 27]
    * **BFS (Busca em Largura):** Explora o labirinto em camadas. **Garante** encontrar o menor caminho possível, mas consome muita memória.
    * **DFS (Busca em Profundidade):** Explora um caminho até o fim antes de voltar (backtracking). Pode encontrar caminhos muito longos e ineficientes, mas usa menos memória.

4.  [cite_start]**Agente Baseado em Utilidade (Busca Informada)** [cite: 22, 27]
    * **Algoritmo A* (A-Star):** Utiliza uma função de avaliação $f(n) = g(n) + h(n)$, onde $g(n)$ é o custo real e $h(n)$ é a heurística.
    * **Heurísticas Implementadas:**
        * *Manhattan Distance:* Ideal para movimentos em grade (cima/baixo/esquerda/direita).
        * *Euclidean Distance:* Distância em linha reta.
        * *Weighted Manhattan:* Penaliza o custo para forçar exploração.

5.  [cite_start]**Agente de Aprendizagem (Reinforcement Learning)** [cite: 23, 27]
    * **Algoritmo Q-Learning:** O agente não conhece o mapa inicialmente. Ele aprende explorando o ambiente através de tentativas e erros (episódios), recebendo recompensas positivas ao atingir o objetivo e negativas ao bater em paredes ou demorar muito.

## 📂 Arquivos do Projeto

A estrutura do projeto é organizada para facilidade de execução:

* `main.py`: **Arquivo principal**. Contém todo o código fonte (Classes `Maze`, Agentes e lógica de execução).
* `README.md`: Documentação do projeto.
* `*.txt`: Arquivos de labirintos para teste (veja seção abaixo).

## 📊 Métricas de Avaliação

[cite_start]O sistema avalia cada agente com base nos seguintes critérios[cite: 26, 31]:

| Métrica | Descrição | Importância |
| :--- | :--- | :--- |
| **Tempo de Execução** | Tempo total (em segundos) para encontrar a solução. | Mede a eficiência computacional do algoritmo. |
| **Tamanho do Caminho** | Número de passos do início ao fim. | Mede a qualidade da solução (otimalidade). O BFS e o A* devem encontrar o menor caminho. |
| **Nós Explorados** | Quantidade de células verificadas antes de achar o fim. | Indica o esforço de busca. Heurísticas melhores exploram menos nós. |
| **Evolução (Q-Learning)** | Melhora no desempenho ao longo dos episódios. | Verifica se o agente está realmente aprendendo[cite: 30]. |

## 🗺️ Labirintos Suportados

O parser de labirintos (`Maze class`) é robusto e suporta os seguintes formatos[cite: 29]:

### 1. Formato Numérico Espaçado
Comum em arquivos como `labirinto_aleatorio.txt`:
```text
1 1 1 1 1
1 0 0 0 1
1 2 1 3 1

