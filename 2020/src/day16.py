from io_utils import read_input_file


def parse_notes(notes):
    nearby_tickets = []
    rules = {}
    i = 0
    while notes[i] != "":
        field, rule = notes[i].split(": ")
        rule1, rule2 = rule.split(" or ")
        rule1_start, rule1_end = rule1.split("-")
        rule2_start, rule2_end = rule2.split("-")
        rules[field] = (range(int(rule1_start), int(rule1_end) + 1), range(int(rule2_start), int(rule2_end) + 1))
        i += 1
    i += 2
    my_ticket = notes[i]
    i += 3
    while i < len(notes):
        nearby_tickets.append(notes[i])
        i += 1
    return nearby_tickets, my_ticket, rules


def flatten_valid_ranges(rules):
    valid_ranges = []
    for rule_range in rules.values():
        valid_ranges.append(rule_range[0])
        valid_ranges.append(rule_range[1])
    return valid_ranges


def day16_1():
    error_rate = 0
    notes = read_input_file("day16.txt", input_type=str, strip=True)
    nearby_tickets, my_ticket, rules = parse_notes(notes)
    valid_ranges = flatten_valid_ranges(rules)
    for ticket in nearby_tickets:
        field_values = ticket.split(",")
        for value in field_values:
            is_invalid, invalid_value = has_invalid_values(int(value), valid_ranges)
            if is_invalid:
                error_rate += invalid_value
    return error_rate


def has_invalid_values(value, valid_ranges):
    for range in valid_ranges:
        if value in range:
            return False, None

    return True, value


def day16_2():
    notes = read_input_file("day16.txt", input_type=str, strip=True)
    nearby_tickets, my_ticket, rules = parse_notes(notes)
    my_ticket = my_ticket.split(",")
    my_ticket = [int(v) for v in my_ticket]
    valid_ranges = flatten_valid_ranges(rules)
    valid_tickets = []
    for ticket in nearby_tickets:
        field_values = ticket.split(",")
        has_invalid_fields = False
        for value in field_values:
            is_invalid, _ = has_invalid_values(int(value), valid_ranges)
            has_invalid_fields |= is_invalid
        if not has_invalid_fields:
            valid_tickets.append(ticket)
    possible_fieldnames = [set() for i in range(0, len(my_ticket))]
    for position in possible_fieldnames:
        for fieldname in rules.keys():
            position.add(fieldname)
    for ticket in valid_tickets:
        field_values = ticket.split(",")
        for i, value in enumerate(field_values):
            value = int(value)
            for filed_name, ranges_tuple in rules.items():
                if value not in ranges_tuple[0] and value not in ranges_tuple[1]:
                    if filed_name in possible_fieldnames[i]:
                        possible_fieldnames[i].remove(filed_name)

    removed = True
    defined_fields = {}
    while removed:
        removed = False
        for i, field_options in enumerate(possible_fieldnames):
            if len(field_options) == 1:
                defined_fields[field_options.pop()] = i
        for fieldset in possible_fieldnames:
            for df in defined_fields:
                if df in fieldset:
                    fieldset = fieldset.remove(df)
                    removed = True
    departure_vals = 1
    for field_name, field_pos in defined_fields.items():
        if field_name.startswith("departure"):
            field_value = my_ticket[field_pos]
            departure_vals *= field_value

    return departure_vals
