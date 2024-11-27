import numpy as np
import os
import psutil
import gc
import time
import matplotlib.pyplot as plt

# Listas para armazenar os valores de memória e desvios
before_memory = []
after_memory = []
iterations = []
deviation_threshold = 2.0  # Limite aceitável de desvio (em MB)


def print_ram_usage(label=""):
    """
    Captura e exibe o uso de memória do processo atual.
    """
    process = psutil.Process(os.getpid())
    memory_in_mb = process.memory_info().rss / (1024 ** 2)
    print(f"{label} Script Memory Usage: {memory_in_mb:.2f} MB")
    return memory_in_mb


class InputProcess:
    def run(self):
        """
        Simula um processamento pesado, gerando e descartando uma matriz.
        """
        data = np.random.uniform(10000, 999910000, (5, 100000))
        del data
        return 1


def process_task(iteration):
    """
    Executa uma tarefa de processamento e monitora o uso de memória antes e depois.
    """
    print(f"Starting Conversion process for Iteration {iteration}...")

    # Captura o valor de memória antes do processamento
    before = print_ram_usage("Before: ")
    total = 0
    proc = InputProcess()

    # Executa o processamento
    for _ in range(1000):
        total += proc.run()

    # Cleanup explícito
    del proc
    gc.collect()

    # Captura o valor de memória após o processamento
    after = print_ram_usage("After: ")

    # Armazena os valores para análise
    before_memory.append(before)
    after_memory.append(after)
    iterations.append(iteration)

    print(f"Iteration {iteration} Total:", total)


def plot_memory_usage():
    """
    Gera um gráfico para analisar o uso de memória ao longo das iterações.
    """
    plt.figure(figsize=(12, 6))

    # Plotando os valores "Before" e "After"
    plt.plot(iterations, before_memory, marker='o', linestyle='-', color='blue', label='Before Memory')
    plt.plot(iterations, after_memory, marker='o', linestyle='-', color='red', label='After Memory')

    # Calculando desvios
    deviations = [abs(after - before) for before, after in zip(before_memory, after_memory)]
    for i, deviation in enumerate(deviations):
        if deviation > deviation_threshold:
            plt.annotate(f"{deviation:.2f} MB",
                         (iterations[i], after_memory[i]),
                         textcoords="offset points",
                         xytext=(0, 10),
                         ha='center',
                         color='darkred')

    # Configuração do gráfico
    plt.xlabel('Iteration', fontsize=12)
    plt.ylabel('Memory Usage (MB)', fontsize=12)
    plt.title('Memory Usage Before and After Processing', fontsize=16)
    plt.legend(fontsize=10)
    plt.grid(True)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)

    # Mostrando o gráfico
    plt.show()


def continuous_processing(max_iterations=100):
    """
    Executa o processamento de forma contínua e monitora o uso de memória.
    """
    for iteration in range(1, max_iterations + 1):
        process_task(iteration)
        time.sleep(1)  # Intervalo de espera entre as iterações


def main():
    """
    Função principal para iniciar o processamento e exibir os resultados.
    """
    try:
        continuous_processing(max_iterations=100)
    except Exception as e:
        print(f"Error during processing: {e}")
    finally:
        plot_memory_usage()  # Garante a exibição do gráfico mesmo em caso de erro


if __name__ == "__main__":
    main()
