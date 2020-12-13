from io_utils import read_input_file


def nearest_departure(departure_timestamp, possible_buses):
    min_waiting_time = max(possible_buses)
    bus_candidate = max(possible_buses)
    for bus in possible_buses:
        waiting_time = bus - departure_timestamp % bus
        if waiting_time < min_waiting_time:
            min_waiting_time = waiting_time
            bus_candidate = bus
    return min_waiting_time, bus_candidate


def day13_1():
    input = read_input_file("day13.txt", input_type=str)
    departure_timestamp = int(input[0])
    possible_buses = []
    for bus in input[1].split(","):
        if bus != "x":
            possible_buses.append(int(bus))
    waiting_time, bus = nearest_departure(departure_timestamp, possible_buses)
    return waiting_time * bus


def generate_offseted_departures(bus, offset, lim):
    result = set()
    i = 1
    while (bus * (i - 1)) < lim:
        result.add(bus * i + offset)
        i += 1
    return result


def day13_2_0():
    input = read_input_file("day13.txt", input_type=str)
    possible_buses = {}
    for offset, bus in enumerate(input[1].split(",")):
        if bus != "x":
            possible_buses[int(bus)] = int(bus) - offset
    lim = 1
    for bus in possible_buses.keys():
        lim *= bus
    solemnly_suitable_timestamps = {}
    for bus, offset in possible_buses.items():
        solemnly_suitable_timestamps[bus] = generate_offseted_departures(bus, offset, lim)
    common_timestamp = set(list(solemnly_suitable_timestamps.values())[0])
    for bus, timestamps in solemnly_suitable_timestamps.items():
        common_timestamp = common_timestamp.intersection(timestamps)
    return common_timestamp


def suits_other_buses(possible_buses, suggested_timestamp):
    for bus, offset  in possible_buses.items():
        if (suggested_timestamp-offset)%bus == 0:
            continue
        else:
            return False
    return True

def day13_2():
    input = read_input_file("day13.txt", input_type=str)
    possible_buses = {}
    for offset, bus in enumerate(input[1].split(",")):
        if bus != "x":
            possible_buses[int(bus)] = int(bus) - offset
    lim = 1
    for bus in possible_buses.keys():
        lim *= bus

    max_bus = max(possible_buses.keys())
    some_solutions = generate_offseted_departures(max_bus, possible_buses[max_bus], lim)
    some_solutions = sorted(some_solutions, reverse=True)
    for some_solution in some_solutions:
        if not suits_other_buses(possible_buses, some_solution):
            continue
        else:
            return some_solution
