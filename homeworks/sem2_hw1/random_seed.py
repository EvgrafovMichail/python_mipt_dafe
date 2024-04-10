import numpy.random as npr
import random

# Почему-то после засовывания в utils не обнаруживается файлами, а sklearn заблуждается

SEED = 42


def freeze_random_seed(seed: int = SEED) -> None:
    random.seed(seed)
    npr.seed(seed)
