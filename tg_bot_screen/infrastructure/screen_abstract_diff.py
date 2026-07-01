# ----- #


from typing import Literal


def calc_abstract_difference(
    start: list[int], end: list[int]
) -> tuple[list[int], list[tuple[int, int]], list[int]]:
    """
    Calculates abstract difference between two lists.

    start and end is lists of ints, that represents a message category.
    We assume that message category cannot be changed, and function
    calculates optimal way to bring start list to end list.

    Returns tuple of:
    list[int] - list of indices of start, that should be deleted
    list[tuple[int, int]] - list of indices of start, that should be edited to indices of end
    list[int] - list of indices of end, that should be sent
    """
    indices_delete = []
    indices_edit = []
    indices_send = []
    startn = 0
    for j, end_type in enumerate(end):
        if startn >= len(start):
            indices_send.append(j)
            continue
        for i, start_type in enumerate(start[startn:], start=startn):
            startn += 1
            if end_type == start_type:
                indices_edit.append((i, j))  # (from, to)
                break
            else:
                indices_delete.append(i)
        else:
            indices_send = list(range(j, len(end)))
            break
    indices_delete += list(range(startn, len(start)))
    return indices_delete, indices_edit, indices_send


def calc_abstract_difference_without_send(
    start: list[int], end: list[int]
) -> tuple[list[int], list[tuple[int, int]]] | None:
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
    indices_delete = []
    indices_edit = []
    startn = 0

    for j, end_num in enumerate(end):
        if startn >= len(start):
            return

        found = False
        for i, start_num in enumerate(start[startn:], start=startn):
            if end_num == start_num:
                indices_edit.append((i, j))
                startn = i + 1
                found = True
                break
            else:
                indices_delete.append(i)

        if not found:
            return

    indices_delete += list(range(startn, len(start)))

    return indices_delete, indices_edit
