import re

from io_utils import read_2d_array


def count_occupied_seats(waiting_area_state):
    occupied_seats = 0
    for row in waiting_area_state:
        occupied_seats += len(re.findall("#", "".join(row)))
    return occupied_seats


def is_occupied(seat_char):
    if seat_char == "#":
        return True
    else:
        return False


def is_empty(seat_char):
    if seat_char == "L":
        return True
    else:
        return False


def check_closest_seat(waiting_area_state, row_index, column_index, row_iterator, column_iterator, max_steps=1):
    for i in range(1, max_steps + 1):
        x = row_index + row_iterator * i
        y = column_index + column_iterator * i
        x = max(0, x)
        y = max(0, y)
        y = min(len(waiting_area_state[row_index])-1, y)
        x = min(len(waiting_area_state)-1, x)

        if is_occupied(waiting_area_state[x][y]):
            return 1
        elif is_empty(waiting_area_state[x][y]):
            return 0
        else:
            continue
    return 0


def count_occupied_adjacent_seats(waiting_area_state, row_index, column_index, max_steps=1):
    adjacent_seats = 0
    adjacent_seats += check_closest_seat(waiting_area_state, row_index, column_index,
                                         column_iterator=1, row_iterator=-1, max_steps=max_steps)
    adjacent_seats += check_closest_seat(waiting_area_state, row_index, column_index,
                                         column_iterator=1, row_iterator=0, max_steps=max_steps)
    adjacent_seats += check_closest_seat(waiting_area_state, row_index, column_index,
                                         column_iterator=1, row_iterator=1, max_steps=max_steps)
    adjacent_seats += check_closest_seat(waiting_area_state, row_index, column_index,
                                         column_iterator=-1, row_iterator=-1, max_steps=max_steps)
    adjacent_seats += check_closest_seat(waiting_area_state, row_index, column_index,
                                         column_iterator=-1, row_iterator=0, max_steps=max_steps)
    adjacent_seats += check_closest_seat(waiting_area_state, row_index, column_index,
                                         column_iterator=-1, row_iterator=1, max_steps=max_steps)
    adjacent_seats += check_closest_seat(waiting_area_state, row_index, column_index,
                                         column_iterator=0, row_iterator=1, max_steps=max_steps)
    adjacent_seats += check_closest_seat(waiting_area_state, row_index, column_index,
                                         column_iterator=0, row_iterator=-1, max_steps=max_steps)
    return adjacent_seats


def update_seats(waiting_area_state, occupancy_tolerance=4, max_steps=1):
    new_state = []
    for i, row in enumerate(waiting_area_state):
        new_state.append([])
        for k, seat in enumerate(row):
            if is_occupied(seat):
                if count_occupied_adjacent_seats(waiting_area_state, i, k, max_steps) >= occupancy_tolerance:
                    new_state[i].append("L")
                else:
                    new_state[i].append("#")
            elif is_empty(seat):

                if count_occupied_adjacent_seats(waiting_area_state, i, k, max_steps) == 0:
                    new_state[i].append("#")
                else:
                    new_state[i].append("L")
            else:
                new_state[i].append(seat)
    return new_state


def add_floor_borders(waiting_area_state):
    for row in waiting_area_state:
        row.insert(0, ".")
        row.append(".")
    waiting_area_state.insert(0, [])
    waiting_area_state.append([])
    for seat in range(0, len(waiting_area_state[1])):
        waiting_area_state[0].append(".")
        waiting_area_state[(len(waiting_area_state) - 1)].append(".")


def day11_1():
    seats_scheme = read_2d_array("day11.txt", strip=True)
    previous_state = seats_scheme
    add_floor_borders(previous_state)  # this way it is easier to count adjacent seats later
    new_state = update_seats(previous_state)
    while previous_state != new_state:
        updated_state = update_seats(new_state)
        previous_state = new_state.copy()
        new_state = updated_state.copy()
    occupied_seats = count_occupied_seats(new_state)
    return occupied_seats


def day11_2():
    seats_scheme = read_2d_array("day11.txt", strip=True)
    previous_state = seats_scheme
    add_floor_borders(previous_state)  # this way it is easier to count adjacent seats later
    new_state = update_seats(previous_state, occupancy_tolerance=5, max_steps=len(previous_state[0]))
    while previous_state != new_state:
        updated_state = update_seats(new_state, occupancy_tolerance=5, max_steps=len(previous_state[0]))
        previous_state = new_state.copy()
        new_state = updated_state.copy()
    occupied_seats = count_occupied_seats(new_state)
    return occupied_seats
