from unittest import TestCase, main
import os
from compiler import compile

# Import test data set
testcases: list[list[str]] = []
testcase_answers: list[list[str]] = []
for i in range(1, 7):
    program = []
    answer = []
    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            os.path.join("tests", f"example{i}.txt"),
        ),
        "r",
    ) as file:
        for line in file:
            program.append(line.strip().lower())
    testcases.append((program))

    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            os.path.join("tests", f"example{i}_machinecode.txt"),
        ),
        "r",
    ) as file:
        for line in file:
            answer.append(line.strip().lower())
    testcase_answers.append(answer)


class TestCompiler(TestCase):
    def test_machinecode(self):
        for i in range(len(testcases)):
            self.assertListEqual(compile(testcases[i]), testcase_answers[i])


if __name__ == "__main__":
    main()
