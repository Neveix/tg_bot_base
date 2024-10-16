from .. import Screen, Menu, Button, ButtonRow, ButtonRows
from .. import StepBackCallbackData as SBCD

screen = Screen("welcome",
    Menu("Welcome!!!!",
        ButtonRows(
            ButtonRow(
                Button("Matrices", SBCD()),
                Button("Matrices", SBCD())
            ),ButtonRow(
                Button("Matrices", SBCD()),
                Button("Matrices", SBCD())
            )
        ), ButtonRows(
            ButtonRow(
                Button("Matrices", SBCD()),
                Button("Matrices", SBCD())
            ),ButtonRow(
                Button("Matrices", SBCD()),
                Button("Matrices", SBCD())
            )
        )
    )
)