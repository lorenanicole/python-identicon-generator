import subprocess
import time
from os import remove
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).parent.absolute()

def test_sample_case_one():
    subprocess.Popen(
        f'python3 main.py --t lorena@example.io --o lorenaemail',
        cwd=f"{PROJECT_ROOT.parent}",
        stdin=subprocess.PIPE,
        shell=True,
    )

    time.sleep(1)

    output = []
    with open(f"{PROJECT_ROOT}/lorenaoutput.png", "rb") as f:
        output = f.readlines(); print(output)
        output = list(map(lambda l: l.decode("utf-8"), output))

    remove(f"{PROJECT_ROOT}/lorenaoutput.png")

    assert output == ['Result(value=6, parser=infix, expression="3*2")']