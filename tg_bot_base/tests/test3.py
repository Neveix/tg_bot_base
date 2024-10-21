from .. import StaticScreen, Menu, Button, ButtonRow, ButtonRows
from .. import StepBackCallbackData as SBCD
from ..user_data import UserDataManager

screen = StaticScreen(
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
    ), name = "welcome"
)

user_data_manager = UserDataManager(None)

user_data_manager.get(0)

print(user_data_manager.users_data)

user_data_manager.get(1)

print(user_data_manager.users_data)
