import time
from backend.blockchain.blockchain import Blockchain
from backend.config import SECONDS_MULTIPLIER
from more_itertools import last

NUMBER_OF_ITERATIONS = 1000
PRECISION = 6


def calculate_block_time(blockchain, times, i, round_to_precision=lambda n: round(n, PRECISION)):
    """
    Calculates and prints different metrics for current iteration
    of block
    """
    start_time = time.time_ns()
    blockchain.add_block(f"{i} block data")
    end_time = time.time_ns()
    time_to_mine = (end_time - start_time) / SECONDS_MULTIPLIER

    new_block = last(blockchain.chain)
    times.append(time_to_mine)
    average_time = sum(times) / len(times)

    print(f"Average time to add blocks: {round_to_precision(average_time)}s")
    print(f"New block difficulty: {new_block.difficulty}")
    print(f"Time to mine new block: {round_to_precision(time_to_mine)}s")


blockchain = Blockchain()
times = []

try:
    for i in range(NUMBER_OF_ITERATIONS):
        calculate_block_time(blockchain, times, i)
except KeyboardInterrupt:
    print(f"Interrupted at {i} block")
