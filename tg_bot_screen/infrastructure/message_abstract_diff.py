# ----- #

from typing import Protocol, TypeVar


MessageT = TypeVar("MessageT")
SentMessageT = TypeVar("SentMessageT")


class CheckFunc(Protocol):
    def __call__(
        self,
        old_message,
        new_message,
    ) -> bool: ...


class Index(int): ...


def calc_abstract_difference(
    start: list[SentMessageT],
    end: list[MessageT],
    can_change: CheckFunc,
) -> tuple[list[Index], list[tuple[Index, Index]], list[Index]]:
    """
    Calculates abstract difference between two lists of messages.

    This function determines the optimal way to transform the `start` list
    into the `end` list using three operations:
    - Delete messages from `start` that are not needed
    - Edit messages from `start` to match messages in `end`
    - Send new messages from `end` that have no counterpart in `start`

    The `can_change` function determines whether a message from `start`
    can be transformed into a message from `end`. This allows the algorithm
    to work with any transformation rules (e.g., type compatibility,
    content changes, etc.).

    The algorithm is greedy but optimal for this use case because:
    - Message order is preserved (messages cannot be reordered)
    - If a message cannot be transformed, it must be deleted
    - New messages are appended at the end

    Args:
        start: List of messages to transform from (sent messages)
        end: List of messages to transform to (unsent messages)
        can_change: Function that returns True if a message from start
                   can be transformed into a message from end

    Returns:
        tuple containing:
        - list[Index]: Indices in `start` that should be deleted
        - list[tuple[Index, Index]]: Pairs of (start_index, end_index)
                                     that should be edited
        - list[Index]: Indices in `end` that should be sent as new
    """

    indices_delete: list[Index] = []
    indices_edit: list[tuple[Index, Index]] = []
    indices_send: list[Index] = []
    startn = 0
    for j, new_message in enumerate(end):
        if startn >= len(start):
            indices_send.append(Index(j))
            continue

        for i, old_message in enumerate(start[startn:], start=startn):
            startn += 1
            if can_change(old_message, new_message):
                indices_edit.append((Index(i), Index(j)))  # (from, to)
                break
            else:
                indices_delete.append(Index(i))
        else:
            indices_send = [Index(s) for s in range(j, len(end))]
            break

    indices_delete += [Index(d) for d in range(startn, len(start))]
    return indices_delete, indices_edit, indices_send


class MessageType(int): ...


def calc_abstract_difference_without_send(
    start: list[MessageType], end: list[MessageType]
) -> tuple[list[Index], list[tuple[Index, Index]]] | None:
    """
    Calculates abstract difference between two lists without sending capability.

    start and end is lists of ints, that represents a message category.
    We assume that message category cannot be changed, and function
    calculates optimal way to bring start list to end list using only
    deletions and edits (no sends).

    Returns:
    - tuple[list[int], list[tuple[int, int]]] - (indices_to_delete, indices_to_edit)
      where indices_to_edit is list of (from_index, to_index) tuples
    - None - if transformation is not possible (would require sending new items)
    """
    indices_delete: list[Index] = []
    indices_edit: list[tuple[Index, Index]] = []
    startn = 0

    for j, end_num in enumerate(end):
        if startn >= len(start):
            return

        found = False
        for i, start_num in enumerate(start[startn:], start=startn):
            if end_num == start_num:
                indices_edit.append((Index(i), Index(j)))
                startn = i + 1
                found = True
                break
            else:
                indices_delete.append(Index(i))

        if not found:
            return

    indices_delete += [Index(d) for d in range(startn, len(start))]

    return indices_delete, indices_edit
