from nim_game.common.models import NimStateChange


# test_init_raise_exception
heaps_amounts = [1, 11]
heaps_amounts_ids = [
    'lower-than-zero',
    'greater-than-ten',
]

# test_change_state_raise_exception
state_changes = [
    NimStateChange(heap_id=-1, decrease=1),
    NimStateChange(heap_id=5, decrease=1),
    NimStateChange(heap_id=10, decrease=1),
    NimStateChange(heap_id=3, decrease=0),
    NimStateChange(heap_id=3, decrease=100),
]
state_changes_ids = [
    'negative-heap-id',
    'heap-id-too-large',
    'to-large-heap-id',
    'nonpositive-decrease',
    'to-large-decrease',
]
