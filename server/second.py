from string import ascii_letters
import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr


class ExtremumFinder:
    def __init__(self):
        self.func = None
    
    def SetFunc(self, func):
        variable = list()
        if '=' in func:
            func = func[func.index('=') + 1:]
        func = func.replace("^", "**")
        func = func.replace("e", "2.71828182845904")
        self.func = func
        for letter in ascii_letters:
            if letter in func:
                variable.append(letter)
                if len(variable) == 2:
                    break
                
        self.func = self.func.replace(variable[0], "(x)")
        self.func = self.func.replace(variable[1], "(y)")
            
    def gradient_descent_constant_step_str(self, x0, epsilon1, epsilon2, M, t=0.1):
        symbols = [sp.Symbol("x"), sp.Symbol("y")]
        expr = parse_expr(self.func)
        gradient_expr = [sp.diff(expr, var) for var in symbols]
        f = sp.lambdify(symbols, expr, 'numpy')
        grad_f = sp.lambdify(symbols, gradient_expr, 'numpy')

        x = np.array(x0, dtype=float)
        k = 0

        while k < M:
            gradient = np.array(grad_f(*x))
            

            if np.linalg.norm(gradient) < 1e-10:
                break
                
            new_x = x - t * gradient 
            new_fx = f(*new_x)
            fx = f(*x)
            

            if np.isnan(new_fx) or np.isinf(new_fx):
                t = t / 2
                continue
                
            if new_fx < fx:
                delta_x = np.linalg.norm(new_x - x)
                delta_f = abs(new_fx - fx)
                

                if delta_x < epsilon1 and delta_f < epsilon2:
                    break
                    
                x = new_x
                k += 1
            else:
                t = t / 2
                if t < 1e-10:
                    break

        return round(x[0], 5), round(x[1], 5), round(f(*x), 5), k
    
    def steepest_gradient_descent(self, x0, epsilon1, epsilon2, M):
        symbols = [sp.Symbol("x"), sp.Symbol("y")]
        expr = parse_expr(self.func)
        gradient_expr = [sp.diff(expr, var) for var in symbols]
        f = sp.lambdify(symbols, expr, 'numpy')
        grad_f = sp.lambdify(symbols, gradient_expr, 'numpy')

        x = np.array(x0, dtype=float)
        k = 0
        prev_x = None
        prev_fx = None

        while True:
            gradient = np.array(grad_f(*x))
            
            gradient_norm = np.linalg.norm(gradient)
            
            if gradient_norm < epsilon1:
                break
                
            if k >= M:
                break
                
            def phi(t):
                new_point = x - t * gradient
                return f(*new_point)
            
            a, b = 0, 1
            golden_ratio = (1 + np.sqrt(5)) / 2
            tolerance = 1e-5
            
            c = b - (b - a) / golden_ratio
            d = a + (b - a) / golden_ratio
            
            while abs(c - d) > tolerance:
                if phi(c) < phi(d):
                    b = d
                else:
                    a = c
                c = b - (b - a) / golden_ratio
                d = a + (b - a) / golden_ratio
                
            t_k = (a + b) / 2
            
            new_x = x - t_k * gradient
            new_fx = f(*new_x)
            fx = f(*x)
            
            if prev_x is not None:
                delta_x = np.linalg.norm(new_x - x)
                delta_f = abs(new_fx - fx)
                
                if delta_x < epsilon2 and delta_f < epsilon2:
                    delta_x_prev = np.linalg.norm(x - prev_x)
                    delta_f_prev = abs(fx - prev_fx)
                    
                    if delta_x_prev < epsilon2 and delta_f_prev < epsilon2:
                        x = new_x
                        k += 1
                        break
            
            prev_x = x.copy()
            prev_fx = fx
            x = new_x
            k += 1
                    
        return round(x[0], 5),  round(x[1], 5), round(f(*x), 5), k + 1
    
    
def test():
    obj = ExtremumFinder()
    obj.SetFunc("2 * x ** 2 + 0.1 * x * y + 6 * y ** 2")
    x = [0, 0.5]
    e1 = 0.15
    e2 = 0.2
    M = 10
    x1, x2, y, k = obj.gradient_descent_constant_step_str(x, e1, e2, M)
    print(x1, x2)
    print(y)
    print(k)

# test()