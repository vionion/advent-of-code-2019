from io_utils import read_input_file


def get_ticket_id(row, column):
    return row * 8 + column


def narrow_down_range(char, rows_range, columns_range):
    if char == "F":
        rows_range = rows_range[:len(rows_range) // 2]
    if char == "B":
        rows_range = rows_range[len(rows_range) // 2:]
    if char == "L":
        columns_range = columns_range[:len(columns_range) // 2]
    if char == "R":
        columns_range = columns_range[len(columns_range) // 2:]
    return rows_range, columns_range


def get_seat(seat_code):
    rows_range = range(0, 128)
    columns_range = range(0, 8)
    for char in seat_code:
        rows_range, columns_range = narrow_down_range(char, rows_range, columns_range)
    return rows_range[0], columns_range[0]


def day5_1():
    tickets_list = read_input_file("day5.txt", input_type=str)
    max_ticket_id = 0
    for ticket in tickets_list:
        row, column = get_seat(ticket)
        ticket_id = get_ticket_id(row, column)
        if ticket_id > max_ticket_id:
            max_ticket_id = ticket_id
    return max_ticket_id


def day5_2():
    tickets_list = read_input_file("day5.txt", input_type=str)
    ticket_ids = []
    for ticket in tickets_list:
        row, column = get_seat(ticket)
        ticket_id = get_ticket_id(row, column)
        ticket_ids.append(ticket_id)
    ticket_ids.sort()
    for ticket_id_index, ticket_id in enumerate(ticket_ids):
        if ticket_ids[ticket_id_index + 1] != ticket_id + 1:
            return ticket_id + 1
