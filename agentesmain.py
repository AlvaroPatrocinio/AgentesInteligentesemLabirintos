import random
import heapq
import time
import numpy as np
from collections import deque

# ==========================================
# 1. MAIN
# ==========================================
class Maze:
    def __init__(self, filename):
        self.grid = []
        self.start = None
        self.end = None
        self.filename = filename
        self.parse_maze(filename)
        self.rows = len(self.grid)
        self.cols = len(self.grid[0]) if self.rows > 0 else 0
        
        # Se nao encontrou Inicio, define padrao (topo-esquerda)
        if self.start is None:
            self.start = self.find_valid_spot(0, 0, 1)
            
        # Se nao encontrou Fim, define padrao (baixo-direita)
        if self.end is None:
            self.end = self.find_valid_spot(self.rows-1, self.cols-1, -1)

    def parse_maze(self, filename):
        try:
            with open(filename, 'r') as f:
                for r, line in enumerate(f):
                    raw_line = line.strip()
                    if not raw_line:
                        continue 
                    
                    # Detecta espaço
                    if ' ' in raw_line:
                        row_chars = raw_line.split()
                    else:
                        row_chars = list(raw_line)

                    parsed_row = []
                    for c, char in enumerate(row_chars):
                        # Mapeamento: 1/# = Parede, 2/S = Inicio, 3/E = Fim
                        if char in ['1', '#']:
                            parsed_row.append('#')
                        elif char in ['2', 'S']:
                            parsed_row.append(' ')
                            self.start = (r, c)
                        elif char in ['3', 'E']:
                            parsed_row.append(' ')
                            self.end = (r, c)
                        else:
                            parsed_row.append(' ')
                    
                    if parsed_row:
                        self.grid.append(parsed_row)
        except Exception as e:
            print(f"Erro ao ler arquivo {filename}: {e}")

    def find_valid_spot(self, start_r, start_c, search_direction):
        r = start_r
        # Procura um espaco vazio se o ponto sugerido for parede
        while 0 <= r < len(self.grid):
            for c in range(len(self.grid[0])):
                if self.grid[r][c] != '#':
                    return (r, c)
            r += search_direction
        return (0, 0)

    def is_valid(self, pos):
        r, c = pos
        if 0 <= r < self.rows and 0 <= c < self.cols:
            if self.grid[r][c] != '#':
                return True
        return False

    def get_neighbors(self, pos):
        r, c = pos
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        result = []
        for dr, dc in directions:
            neighbor = (r + dr, c + dc)
            if self.is_valid(neighbor):
                result.append(neighbor)
        return result

# ==========================================
# 2. AGENTES
# ==========================================

class SimpleReflexAgent:
    def solve(self, maze):
        if not maze.start or not maze.end: return [], 0
        path = [maze.start]
        current = maze.start
        steps = 0
        
        while current != maze.end and steps < 2000:
            neighbors = maze.get_neighbors(current)
            if not neighbors: break
            current = random.choice(neighbors)
            path.append(current)
            steps += 1
        return path, steps

class ModelBasedReflexAgent:
    def solve(self, maze):
        if not maze.start or not maze.end: return [], 0
        path = [maze.start]
        current = maze.start
        visited = {current}
        steps = 0
        
        while current != maze.end and steps < 5000:
            neighbors = maze.get_neighbors(current)
            unvisited = [n for n in neighbors if n not in visited]
            
            if unvisited:
                current = random.choice(unvisited)
            elif neighbors:
                current = random.choice(neighbors)
            else:
                break
            
            visited.add(current)
            path.append(current)
            steps += 1
        return path, len(path)

class GoalBasedAgent:
    def __init__(self, strategy='bfs'):
        self.strategy = strategy

    def solve(self, maze):
        if not maze.start or not maze.end: return [], 0
        queue = deque([(maze.start, [maze.start])])
        visited = {maze.start}
        nodes_explored = 0
        
        while queue:
            nodes_explored += 1
            if self.strategy == 'bfs':
                vertex, path = queue.popleft()
            else:
                vertex, path = queue.pop()
            
            if vertex == maze.end:
                return path, nodes_explored
            
            neighbors = maze.get_neighbors(vertex)
            if self.strategy == 'dfs': random.shuffle(neighbors)
                
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return [], nodes_explored

class UtilityAgent:
    def __init__(self, heuristic_type='manhattan'):
        self.heuristic_type = heuristic_type

    def heuristic(self, a, b):
        if self.heuristic_type == 'manhattan':
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5

    def solve(self, maze):
        if not maze.start or not maze.end: return [], 0
        pq = [(0, 0, maze.start, [maze.start])]
        visited = set()
        nodes_explored = 0
        g_score = {maze.start: 0}
        
        while pq:
            nodes_explored += 1
            f, _, current, path = heapq.heappop(pq)
            
            if current == maze.end:
                return path, nodes_explored
            
            if current in visited: continue
            visited.add(current)
            
            for neighbor in maze.get_neighbors(current):
                new_g = g_score[current] + 1
                if neighbor not in g_score or new_g < g_score[neighbor]:
                    g_score[neighbor] = new_g
                    h = self.heuristic(neighbor, maze.end)
                    heapq.heappush(pq, (new_g + h, new_g, neighbor, path + [neighbor]))
        return [], nodes_explored

class QLearningAgent:
    def __init__(self, maze, episodes=500):
        self.maze = maze
        self.episodes = episodes
        self.q_table = {} 
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 1.0
        self.decay = 0.99
        self.min_eps = 0.05
        self.actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def get_q(self, state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(4)
        return self.q_table[state]

    def train(self):
        if not self.maze.start or not self.maze.end: return []
        for ep in range(self.episodes):
            state = self.maze.start
            steps = 0
            done = False
            while not done and steps < 300:
                if random.random() < self.epsilon:
                    act = random.randint(0, 3)
                else:
                    act = np.argmax(self.get_q(state))
                
                dr, dc = self.actions[act]
                nxt = (state[0]+dr, state[1]+dc)
                
                reward = -1
                if not self.maze.is_valid(nxt):
                    reward = -10
                    nxt = state
                elif nxt == self.maze.end:
                    reward = 100
                    done = True
                
                old_q = self.get_q(state)[act]
                next_max = np.max(self.get_q(nxt)) if not done else 0
                self.q_table[state][act] = old_q + self.alpha*(reward + self.gamma*next_max - old_q)
                
                state = nxt
                steps += 1
            
            if self.epsilon > self.min_eps:
                self.epsilon *= self.decay

    def solve_after_training(self):
        if not self.maze.start: return []
        path = [self.maze.start]
        curr = self.maze.start
        for _ in range(100):
            if curr == self.maze.end: break
            act = np.argmax(self.get_q(curr))
            dr, dc = self.actions[act]
            nxt = (curr[0]+dr, curr[1]+dc)
            if self.maze.is_valid(nxt):
                curr = nxt
                path.append(curr)
            else:
                break
        return path

# ==========================================
# 3. EXECUÇÃO
# ==========================================
def run_tests():
    files = [
        "/labirinto_aleatorio.txt", "/labirinto_aleatorio_2.txt",
        "/labirinto_colmeia.txt", "/labirinto_espiral.txt",
        "/labirinto_estrela.txt", "/labirinto_onda.txt"
    ]
    
    agents = [
        ("Simples", SimpleReflexAgent()),
        ("Modelo", ModelBasedReflexAgent()),
        ("BFS", GoalBasedAgent('bfs')),
        ("DFS", GoalBasedAgent('dfs')),
        ("A*", UtilityAgent('manhattan'))
    ]

    print("INICIANDO TESTES...\n")
    for f in files:
        print(f"--- Labirinto: {f} ---")
        try:
            m = Maze(f)
            if not m.grid:
                print("Arquivo vazio ou invalido.\n")
                continue
                
            print(f"Tamanho: {m.rows}x{m.cols}")
            
            # Agentes Classicos
            print(f"{'Agente':<15} | {'Tempo':<8} | {'Passos'}")
            for name, ag in agents:
                t0 = time.time()
                p, ops = ag.solve(m)
                dt = time.time() - t0
                print(f"{name:<15} | {dt:<8.4f} | {len(p)}")
            
            # Agente Q-Learning
            print("Treinando Q-Learning...", end=" ")
            ql = QLearningAgent(m, episodes=200)
            ql.train()
            p_ql = ql.solve_after_training()
            print(f"Fim. Caminho: {len(p_ql)}\n")
            
        except FileNotFoundError:
            print(f"ARQUIVO NAO ENCONTRADO: {f}\n")

if __name__ == "__main__":
    run_tests()