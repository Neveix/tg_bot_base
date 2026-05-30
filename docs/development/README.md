# Руководство для разработчиков

## Как деплоить?

### Установка зависимостей
`pip install hatch twine`

### Деплой

`hatch build`  
`twine upload dist/* --skip-existing`

### Использование тестовых скриптов

#### Использовать текущую библиотеку:
`pip install -e .`