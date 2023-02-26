from math import e
import numpy as np

def sigmoid(x) -> float:
    return 1/(1+e**-x)

class RedeNeural:
    
    def __init__(self, camadas : list[int], funcoes : list[list]):
        if len(funcoes) != len(camadas)-1:
            print("ERRO: Quantidade errada de funções de ativação.")
            exit(0)
        self.camadas = camadas
        self.pesos = []
        self.vieses = []
        for i in range(len(camadas)-1): # [3, 3, 1], 0 1
            self.vieses.append([])
            self.vieses[i].extend([1] for i in range(camadas[i+1]))
            self.pesos.append([]) # [[]]
            self.pesos[i].extend([[] for j in range(camadas[i+1])]) # [[[],[],[]]]
            for line in self.pesos[i]:
                line.extend([np.random.normal() for neuronio in range(camadas[i])])
        for i in range(len(self.pesos)):
            self.pesos[i] = np.array(self.pesos[i])
        for i in range(len(self.vieses)):
            self.vieses[i] = np.array(self.vieses[i])
        self.act_funcoes = np.array(funcoes)

    def feed_foward(self, a : np.ndarray, camada : int = 0):
        s = np.matmul(self.pesos[camada], a)+self.vieses[camada]
        ativacoes = self.act_funcoes[camada](s)
        if camada == len(self.pesos)-1:
            return ativacoes
        return self.feed_foward(ativacoes, camada+1)

class Individuo:
    
    def __init__(self, genes : list[int], funcoes : list, fitness : float = None) -> None:
        self.neural_net = RedeNeural(genes, funcoes)
        self.fitness = fitness

    def pular(self, caracteristicas : list[list[float]]) -> bool:
        caracteristicas = np.array(caracteristicas)
        return self.neural_net.feed_foward(caracteristicas)[0] >= 0.5

    def mutar(self) -> None:

        # Se alfa menor que a taxa adotada a mutação é realizada para aquele gene em questão
        # O processo se repete para todos os genes dos filhos
        # Os genes são equivalentes aos pesos nas redes neurais de cada individuo/filho
            #mudar cada peso na rede neural
        for i, matriz_peso in enumerate(self.neural_net.pesos):
            for j in range(matriz_peso.shape[0]):
                for k in range(matriz_peso.shape[1]):
                    if np.random.random() < 0.35:
                        matriz_peso[j, k] = np.random.normal()

class Populacao:

    def __init__(self, numero_individuos = None, individuos : list[Individuo] = None) -> None:
        if individuos is None:
            self.individuos = []
        else:
            self.individuos = individuos.copy()
        if numero_individuos != None:
            for i in range(numero_individuos):
                self.individuos.append(Individuo(
                    genes=[2, 2, 1],
                    funcoes=[sigmoid,sigmoid]
                ))
            
    def selecao(self) -> "Populacao":
        # Cria uma lista pras porcentagens que cada indivíduo possui de entrar
        # na seleção, com base no fitness de cada um.       

        porcentagens = []
        auxfitness = self.individuos[0].fitness 
        for individuo in self.individuos:
            if individuo.fitness > auxfitness:
                auxfitness = individuo.fitness
        if auxfitness == 0:
            for individuo in self.individuos:
                porcentagens.append(1/len(self.individuos))
        else:    
            for individuo in self.individuos:
                porcentagens.append(individuo.fitness/auxfitness)
        # Seleciona 10 indivíduos para o cruzamento utilizando as porcentagens acima.
        
        selecionados = []
        
        for i in range(10):
            j = 0 
            escolhido = 0
            chance_atual = 0
            while not escolhido:
                alfa = np.random.random()
                chance_atual = chance_atual + porcentagens[j]
                alfa < chance_atual
                if not self.individuos in selecionados and alfa < chance_atual:
                    selecionados.append(self.individuos[j])
                    escolhido = 1
                if j+1 >= len(self.individuos):
                    j = 0
                else:
                    j = j+1
        # Retorna nova população de indivíduos selecionados.
        populacao_resultado = Populacao(10, selecionados)
        return populacao_resultado
    
    def get_elite(self) -> list[Individuo]:
        auxfitness = self.individuos[0].fitness 
        elite_index = 0
        for i, individuo in enumerate(self.individuos):
            if individuo.fitness > auxfitness:
                auxfitness = individuo.fitness
                elite_index = i
        return [self.individuos[elite_index],]

    def animal_crossing(self, elite : list[Individuo]) -> "Populacao":
        populacao_resultado = Populacao()
        # Realiza o cruzamento até possuir um total de 100 indivíduos novamente.
        # Lembrando que a população utilizada é aquela obtida pela seleção
        populacao_resultado.individuos.extend(elite)
        while (len(populacao_resultado.individuos) < 30):
            i = 0
            print(f"Gerando população: {len(populacao_resultado.individuos)}")
            pai1 = self.individuos[i:i+2][0]
            pai2 = self.individuos[i:i+2][1]

            beta = np.random.random()
            alfa = np.random.random()
            if alfa < 0.85:
                filho1 = Individuo(
                    genes=pai1.neural_net.camadas,
                    funcoes = pai1.neural_net.act_funcoes
                )
                for w in range(len(filho1.neural_net.pesos)):
                    filho1.neural_net.pesos[w] = beta*pai1.neural_net.pesos[w]+(1-beta)*pai2.neural_net.pesos[w]
                filho2 = Individuo(
                    genes=pai1.neural_net.camadas,
                    funcoes = pai1.neural_net.act_funcoes
                )
                for w in range(len(filho1.neural_net.pesos)):
                    filho2.neural_net.pesos[w] = beta*pai2.neural_net.pesos[w]+(1-beta)*pai1.neural_net.pesos[w]
                filho1.mutar()
                filho2.mutar()

                populacao_resultado.individuos.append(filho1) 
                populacao_resultado.individuos.append(filho2) 
            else: 
                populacao_resultado.individuos.append(pai1) 
                populacao_resultado.individuos.append(pai2) 
            i+= 2
            if (i == 30): i = 0
        return populacao_resultado