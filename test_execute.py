from unittest import TestCase, main
import os
from executor import execute


class SimulatedInput:
    def __init__(self, inputs: list[str]):
        self.inputs = inputs
        self.input_number = 0

    def __call__(self) -> str:
        self.input_number += 1
        return self.inputs[self.input_number - 1]


# Import test data set
test_case_machine_code: list[list[str]] = []
for i in range(1, 7):
    program = []
    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            os.path.join("tests", f"example{i}_machinecode.txt"),
        ),
        "r",
    ) as file:
        for line in file:
            program.append(line.strip().lower())
    test_case_machine_code.append(program)

# Example[Test case[[inputs], [outputs]]]
test_case_input_output: list[list[list[list[str]]]] = []
for i in range(1, 7):
    program_test_cases: list[list[list[str]]] = []
    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            os.path.join("tests", f"example{i}_io.txt"),
        ),
        "r",
    ) as file:
        for line in file:
            inputs, outputs = line.strip().lower().split(":")
            program_test_cases.append([inputs.split(" "), outputs.split(" ")])
    test_case_input_output.append(program_test_cases)


class TestExecute(TestCase):
    def test_example1(self):
        for test_case in test_case_input_output[0]:
            output = []

            # Use a lambda to convert output to string for array comparison
            execute(
                test_case_machine_code[0],
                False,
                SimulatedInput(test_case[0]),
                lambda x: output.append(str(x)),
            )
            self.assertListEqual(output, test_case[1])

    def test_example2(self):
        for test_case in test_case_input_output[1]:
            output = []

            # Use a lambda to convert output to string for array comparison
            execute(
                test_case_machine_code[1],
                False,
                SimulatedInput(test_case[0]),
                lambda x: output.append(str(x)),
            )
            self.assertListEqual(output, test_case[1])

    def test_example3(self):
        for test_case in test_case_input_output[2]:
            output = []

            # Use a lambda to convert output to string for array comparison
            execute(
                test_case_machine_code[2],
                False,
                SimulatedInput(test_case[0]),
                lambda x: output.append(str(x)),
            )
            self.assertListEqual(output, test_case[1])

    def test_example4(self):
        for test_case in test_case_input_output[3]:
            output = []

            # Use a lambda to convert output to string for array comparison
            execute(
                test_case_machine_code[3],
                False,
                SimulatedInput(test_case[0]),
                lambda x: output.append(str(x)),
            )
            self.assertListEqual(output, test_case[1])

    def test_example5(self):
        for test_case in test_case_input_output[4]:
            output = []

            # Use a lambda to convert output to string for array comparison
            execute(
                test_case_machine_code[4],
                False,
                SimulatedInput(test_case[0]),
                lambda x: output.append(str(x)),
            )
            self.assertListEqual(output, test_case[1])

    def test_example6(self):
        for test_case in test_case_input_output[5]:
            output = []

            # Use a lambda to convert output to string for array comparison
            execute(
                test_case_machine_code[5],
                False,
                SimulatedInput(test_case[0]),
                lambda x: output.append(str(x)),
            )
            self.assertListEqual(output, test_case[1])


if __name__ == "__main__":
    main()
