
from .. import MenuCallbackData as MCD
from ..menu import buttons_are_correct
buttons = [
    [
            ["Матрицы", MCD("matrices")]
        ,["Линейные операторы", MCD("operators")]
    ], [
            ["Линейные пространства", MCD("spaces")]
    ], [
            ["Аккаунт", MCD("account")]
        ,["Помощь", MCD("help")]
    ]
]

print(buttons_are_correct(buttons))
