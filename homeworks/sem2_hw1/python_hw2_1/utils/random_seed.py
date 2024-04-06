import numpy.random as npr
import random


SEED = 42


def freeze_random_seed(seed: int = SEED) -> None:
    random.seed(seed)
    npr.seed(seed)
