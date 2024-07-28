from enum import Enum

instructions: dict[str, str] = {
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


class TokenType(Enum):
    LABEL = "label"
    INSTRUCTION = "instruction"
    OPERAND_LITERAL = "operand literal"
    OPERAND_LABEL = "operand label"


class Token:
    def __init__(self, token_type: TokenType, value: str) -> None:
        self.token_type: TokenType = token_type
        self.value: str = value

    def __str__(self) -> str:
        return self.value


def tokenise(code: list[str]) -> list[list[Token]]:
    tokens: list[list[Token]] = []
    for i in code:
        parts: list[str] = i.split(" ")
        line: list[Token] = []

        # Label refers to the the name of a memory location
        # When a label is used as a operand, it is categorised as an operand not a label
        # Label can only be the first element therefore any element after the first element cannot be a label

        for part in parts:
            # Handle empty lines
            if part != "":
                if part in instructions:
                    line.append(Token(TokenType.INSTRUCTION, part))
                elif len(line) == 0:
                    line.append(Token(TokenType.LABEL, part))
                elif part.isdigit():
                    line.append(Token(TokenType.OPERAND_LITERAL, part))
                else:
                    line.append(Token(TokenType.OPERAND_LABEL, part))
        if len(line) > 0:
            tokens.append(line)
    return tokens


def compile(code: list[str]) -> list[str]:
    """
    Converts lmc to "machine code"
    As specified here https://www.yorku.ca/sychen/research/LMC/LMCInstructionSummary.html
    """

    lines: list[list[Token]] = tokenise(code)
    #
    # Label table
    #

    # format(label: line number)
    label_table: dict[str, int] = {}

    for line_number, tokens in enumerate(lines):
        # Each line should either begin with a instruction or a label
        if tokens[0].token_type == TokenType.LABEL:
            label_table[tokens[0].value] = line_number

    machine_code: list[str] = []
    for line_number, tokens in enumerate(lines):

        # Get instruction depending on whether first token is label or not
        instruction: Token | None = None
        operand: Token | None = None

        if tokens[0].token_type == TokenType.LABEL:
            instruction = tokens[1]
        else:
            instruction = tokens[0]

        if (
            tokens[-1].token_type == TokenType.OPERAND_LABEL
            or tokens[-1].token_type == TokenType.OPERAND_LITERAL
        ):
            operand = tokens[-1]

        if instruction.token_type != TokenType.INSTRUCTION:
            raise SyntaxError(
                f"Expected instruction on line {line_number}\n{' '.join(str(token) for token in tokens).upper()}"
            )

        # Maximum tokens per line is 3
        if len(tokens) > 3:
            # Use list comprehension to allow for Tokens to be joined
            raise SyntaxError(
                f"Line {line_number} has too many tokens\n{' '.join(str(token) for token in tokens).upper()}"
            )

        #
        # Code generation
        #

        x: str = instructions[instruction.value]

        if instruction.value == "dat":
            if operand:
                if (
                    operand.value.isdigit()
                    and operand.token_type == TokenType.OPERAND_LITERAL
                ):
                    x = str(int(operand.value))
                else:
                    raise SyntaxError(
                        f"Expected integer. Line {line_number} \n{' '.join(str(token) for token in tokens).upper()}"
                    )
            else:
                x = "0"
        elif "xx" in x:
            if operand:
                if operand.token_type == TokenType.OPERAND_LITERAL:
                    operand_address: str = str(operand.value).zfill(2)
                else:
                    operand_address = str(label_table[operand.value]).zfill(2)
                x = x.replace("xx", operand_address)

        machine_code.append(x)

    return machine_code
