def execute(code: list[str], debug=False, output=print) -> None:
    # Let the output function be varied to allow for easily being able to extract output if needed

    if debug:
        print(code)

    # Memory stored as string so that "000" (halt command) and "0" (empty memory location) can be distinguished
    memory: list[str] = ["0"] * 99
    accumulator: int = 0
    program_counter = 0

    running = True

    # loading program into memory
    for i in range(len(code)):
        memory[i] = code[i]

    while running:
        if debug:
            print(f"memory: {memory}")
            print(f"accumulator: {accumulator}")
            print(f"program_counter: {program_counter}")
            print(f"current instruction: {memory[program_counter]}")
            input("Press any key to continue")

        branched = False

        # First handle instructions with no operands
        match memory[program_counter]:
            case "000":
                running = False
            case "901":
                try:
                    accumulator = int(input())
                except ValueError:
                    raise ValueError(
                        "Unexpected input, only integer inputs are allowed"
                    )
            case "902":
                print(accumulator)
            case _:
                #
                # Handle instructions with operands
                #
                index = int(memory[program_counter][-2:])
                match memory[program_counter][0]:
                    case "1":
                        # Addition
                        accumulator = accumulator + int(memory[index])
                    case "2":
                        # Subtraction
                        accumulator = accumulator - int(memory[index])
                    case "3":
                        # Store
                        memory[index] = str(accumulator)
                    case "5":
                        # Load
                        accumulator = int(memory[index])
                    case "6":
                        # Branch always
                        program_counter = int(index)
                        branched = True
                    case "7":
                        # Branch if zero
                        if accumulator == 0:
                            program_counter = int(index)
                            branched = True
                    case "8":
                        # Branch if zero or positive
                        if accumulator >= 0:
                            program_counter = int(index)
                            branched = True

        if not branched:
            program_counter += 1
