instructions = {
    "lda": "5xx",
    "sta": "3xx",
    "add": "1xx",
    "sub": "2xx",
    "inp": "901",
    "out": "902",
    "hlt": "000",
    "brz": "7xx",
    "brp": "8xx",
    "bra": "6xx",
    "dat": "",
}


def tokenise(code: list[str]) -> list[list[str]]:
    lines: list[list[str]] = []
    for i in code:
        lines.append(i.split(" "))
    return lines


def compile(code: list[str]) -> list[str]:
    """
    Converts lmc to "machine code"
    As specified here https://www.yorku.ca/sychen/research/LMC/LMCInstructionSummary.html
    """

    lines: list[list[str]] = tokenise(code)
    #
    # Label table
    #

    # Each line should either begin with a instruction or a label#

    # format(label: line number)
    label_table: dict[str, int] = {}

    for line_number, tokens in enumerate(lines):
        if tokens[0] not in instructions:
            label_table[tokens[0]] = line_number

    machine_code: list[str] = []
    for line_number, tokens in enumerate(lines):
        # Get instruction depending on whether first token is label or not
        if tokens[0] in label_table:
            instruction_index: int = 1
        else:
            instruction_index: int = 0
        instruction: str = tokens[instruction_index]

        #
        # Error checking
        #

        if instruction not in instructions:
            raise Exception(f"Invalid instruction on line {line_number}: {tokens}")

        # dat is an exception since it can have 1,2 or 3 tokens depending on whether it has no label and no value, no label or no value, a label and a value respectively
        if instruction == "dat":
            if len(tokens) > 3:
                raise Exception(
                    f"Line {line_number} has too many tokens: {' '.join(tokens).upper()}"
                )
        else:

            # If machine code instruction has xx it expects an opcode therefore line should have 2-3 tokens depending on whether or not a label is present or not
            if "xx" in instructions[instruction]:
                expected = 2
            else:
                expected = 1
            if len(tokens) != expected + instruction_index:
                raise Exception(
                    f"Line {line_number} has {'too many' if len(tokens) > expected + instruction_index else 'too few'} tokens: {' '.join(tokens).upper()}"
                )

        #
        # Code generation
        #

        x: str = instructions[instruction]

        if instruction == "dat":
            if len(tokens) == 1 + instruction_index:
                x = "0"
            else:
                x = tokens[instruction_index + 1]
                if x.isdigit():
                    x = str(int(x))
                else:
                    raise Exception(
                        f"Values in memory must be integers. Line {line_number}: {' '.join(tokens)}"
                    )

        if "xx" in x:
            operand = tokens[instruction_index + 1]
            if operand.isnumeric():
                operand_address = operand.zfill(2)
            else:
                operand_address = str(label_table[operand]).zfill(2)
            x = x.replace("xx", operand_address)
        machine_code.append(x)

    return machine_code
