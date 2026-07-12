from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import nbformat

PATH = Path("scripts/execute_notebooks.py")
SPEC = spec_from_file_location("execute_notebooks", PATH)
assert SPEC and SPEC.loader
EXECUTOR = module_from_spec(SPEC)
SPEC.loader.exec_module(EXECUTOR)


def test_without_learner_exercises_keeps_only_gate_cells() -> None:
    notebook = nbformat.v4.new_notebook(
        cells=[
            nbformat.v4.new_code_cell("value = 1"),
            nbformat.v4.new_code_cell(
                "raise NotImplementedError",
                metadata={"tags": ["learner-exercise"]},
            ),
        ]
    )

    execution_copy = EXECUTOR.without_learner_exercises(notebook)

    assert [cell.source for cell in execution_copy.cells] == ["value = 1"]
