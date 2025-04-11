import math

def evaluate_expression(func_str, variable, x_value):
    expr = func_str.replace(variable, str(x_value))
    
    # Обеспечиваем поддержку математических функций (sin, cos, exp и т. д.)
    allowed_names = {
        'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
        'exp': math.exp, 'log': math.log, 'log10': math.log10,
        'sqrt': math.sqrt, 'pi': math.pi, 'e': math.e
    }
    
    # Проверяем, нет ли в выражении запрещённых конструкций
    try:
        # Компилируем выражение в байт-код для безопасности
        code = compile(expr, '<string>', 'eval')
        for name in code.co_names:
            if name not in allowed_names:
                raise ValueError(f"Использование '{name}' запрещено")
        
        # Вычисляем выражение
        result = eval(code, {'__builtins__': None}, allowed_names)
        return result
    except Exception as e:
        raise ValueError(f"Ошибка вычисления выражения: {e}")

def my_power(x, p):
    return eval(f"{x} ** {p}")

# Примеры использования:
print(evaluate_expression("x**2", 'x', -2))
print(my_power(-2, 2))