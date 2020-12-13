import math

from io_utils import read_input_file


def strafe_move(direction, value, position_x, position_y):
    if direction == "N":
        position_y += value
    if direction == "S":
        position_y -= value
    if direction == "E":
        position_x += value
    if direction == "W":
        position_x -= value
    return position_x, position_y


def rotate(direction, degrees, orientation):
    if direction == "R":
        orientation -= degrees
    if direction == "L":
        orientation += degrees
    return orientation


def move(value, position_x, position_y, orientation):
    position_y += math.sin(math.radians(orientation)) * value
    position_x += math.cos(math.radians(orientation)) * value
    return position_x, position_y


def process_instruction(position_x, position_y, orientation, instruction):
    action = instruction[0]
    value = int(instruction[1:])
    if action in ["N", "S", "E", "W"]:
        position_x, position_y = strafe_move(action, value, position_x, position_y)
    elif action in ["R", "L"]:
        orientation = rotate(action, value, orientation)
    elif action == "F":
        position_x, position_y = move(value, position_x, position_y, orientation)
    return position_x, position_y, orientation


def day12_1():
    instructions = read_input_file("day12.txt", input_type=str)
    position_x, position_y = 0, 0
    orientation = 0
    for instruction in instructions:
        position_x, position_y, orientation = process_instruction(position_x, position_y, orientation, instruction)
    return int(abs(position_x) + abs(position_y))


def rotate_waypoint(direction, value, waypoint_position_x, waypoint_position_y):
    sin = math.sin(math.radians(value))
    cos = math.cos(math.radians(value))
    if direction == "R":
        new_waypoint_position_x = sin * waypoint_position_y + cos * waypoint_position_x
        new_waypoint_position_y = -sin * waypoint_position_x + cos * waypoint_position_y
    if direction == "L":
        new_waypoint_position_x = -sin * waypoint_position_y + cos * waypoint_position_x
        new_waypoint_position_y = +sin * waypoint_position_x + cos * waypoint_position_y
    return new_waypoint_position_x, new_waypoint_position_y


def move_towards_waypoint(value, position_x, position_y, waypoint_position_x, waypoint_position_y):
    position_x += value * waypoint_position_x
    position_y += value * waypoint_position_y
    return position_x, position_y


def process_waypoint_instruction(position_x, position_y, waypoint_position_x, waypoint_position_y, instruction):
    action = instruction[0]
    value = int(instruction[1:])
    if action in ["N", "S", "E", "W"]:
        waypoint_position_x, waypoint_position_y = strafe_move(action, value, waypoint_position_x, waypoint_position_y)
    elif action in ["R", "L"]:
        waypoint_position_x, waypoint_position_y = rotate_waypoint(action, value, waypoint_position_x,
                                                                   waypoint_position_y)
    elif action == "F":
        position_x, position_y = move_towards_waypoint(value, position_x, position_y, waypoint_position_x,
                                                       waypoint_position_y)
    return position_x, position_y, waypoint_position_x, waypoint_position_y


def day12_2():
    instructions = read_input_file("day12.txt", input_type=str)
    position_x, position_y = 0, 0
    waypoint_position_x, waypoint_position_y = 10, 1

    print(rotate_waypoint("R", 180, waypoint_position_x, waypoint_position_y))
    for instruction in instructions:
        position_x, position_y, waypoint_position_x, waypoint_position_y = process_waypoint_instruction(position_x,
                                                                                                         position_y,
                                                                                                         waypoint_position_x,
                                                                                                         waypoint_position_y,
                                                                                                         instruction)
    return int(abs(position_x) + abs(position_y))
