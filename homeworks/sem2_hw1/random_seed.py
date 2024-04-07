import numpy.random as npr
import random

# я пытался засунуть их в utils, нщ импорты октазывались работать, не успел

SEED = 42


def freeze_random_seed(seed: int = SEED) -> None:
    random.seed(seed)
    npr.seed(seed)
