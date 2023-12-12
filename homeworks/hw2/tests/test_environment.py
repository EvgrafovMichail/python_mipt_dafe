import pytest

from nim_game.environments.environment_nim import (
    EnvironmentNim,
    STONE_AMOUNT_MIN,
    STONE_AMOUNT_MAX,
)

from tests.data import (
    heaps_amounts,
    heaps_amounts_ids,
    state_changes,
    state_changes_ids,
)


@pytest.mark.parametrize(
    'heap_amount', heaps_amounts, ids=heaps_amounts_ids
)
def test_init_raise_exception(heap_amount):
    with pytest.raises(ValueError):
        EnvironmentNim(heap_amount)


def test_get_state_return_value():
    heap_amount = 5

    environment = EnvironmentNim(heap_amount)
    state = environment.get_state()

    assert isinstance(state, list)
    assert len(state) == heap_amount
    assert all(isinstance(elem, int) for elem in state)
    assert all(
        STONE_AMOUNT_MIN <= elem <= STONE_AMOUNT_MAX
        for elem in state
    )


@pytest.mark.parametrize(
    'state_change', state_changes, ids=state_changes_ids
)
def test_change_state_raise_exception(state_change):
    environment = EnvironmentNim(heaps_amount=5)

    with pytest.raises(ValueError):
        environment.change_state(state_change)
