from io_utils import read_input_file


def execute_instruction(instructions, rule_index, accumulator, executed_instructions):
    if rule_index >= len(instructions):
        return accumulator, True
    if rule_index in executed_instructions:
        return accumulator, False
    else:
        instruction = instructions[rule_index]
        instruction = instruction.strip()
        operation, argument = instruction.split(" ")
        argument = int(argument)
        executed_instructions.append(rule_index)
        if operation == "nop":
            # print("no operation")
            return execute_instruction(instructions=instructions, rule_index=rule_index + 1, accumulator=accumulator,
                                       executed_instructions=executed_instructions)

        if operation == "jmp":
            # print(f"jump {argument}")
            return execute_instruction(instructions=instructions, rule_index=rule_index + argument,
                                       accumulator=accumulator, executed_instructions=executed_instructions)

        if operation == "acc":
            accumulator += argument
            # print(f"accumulator {accumulator}")
            return execute_instruction(instructions=instructions, rule_index=rule_index + 1, accumulator=accumulator,
                                       executed_instructions=executed_instructions)


def day8_1():
    input_list = read_input_file("day8.txt", input_type=str)
    accumulator, _ = execute_instruction(instructions=input_list, rule_index=0, accumulator=0, executed_instructions=[])
    return accumulator


def day8_2():
    input_list = read_input_file("day8.txt", input_type=str)
    # this is really not a good solution, basically trying every possible option. TODO: redo
    for i, line in enumerate(input_list):
        finished_normally = False
        if line[0:3] == "nop":
            input_list[i] = line.replace("nop", "jmp")
            accumulator, finished_normally = execute_instruction(instructions=input_list, rule_index=0, accumulator=0,
                                                                 executed_instructions=[])
            input_list[i] = line.replace("jmp", "nop")
        if line[0:3] == "jmp":
            input_list[i] = line.replace("jmp", "nop")
            accumulator, finished_normally = execute_instruction(instructions=input_list, rule_index=0, accumulator=0,
                                                                 executed_instructions=[])
            input_list[i] = line.replace("nop", "jmp")
        if finished_normally:
            return accumulator
