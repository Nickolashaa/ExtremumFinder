import numpy as np
from sympy import symbols, diff, hessian, lambdify
from string import ascii_letters

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
        
    def nyuton(self, x, e1, e2, M):

        x_sym, y_sym = symbols('x y')
        

        f_expr = eval(self.func, {'x': x_sym, 'y': y_sym})
        

        gradient = [diff(f_expr, var) for var in (x_sym, y_sym)]
        grad_func = lambdify((x_sym, y_sym), gradient, 'numpy')
        

        hessian_matrix = hessian(f_expr, (x_sym, y_sym))
        hessian_func = lambdify((x_sym, y_sym), hessian_matrix, 'numpy')
        
        k = 0
        x_k = np.array(x, dtype=float)
        
        while True:

            grad = np.array(grad_func(x_k[0], x_k[1]), dtype=float)
            

            if np.linalg.norm(grad) <= e1:
                x = x_k1.tolist()
                return round(x[0], 5), round(x[1], 5), round(float(eval(self.func, {'x': x[0], 'y': x[1]})), 5), k
            

            if k >= M:
                x = x_k1.tolist()
                return round(x[0], 5), round(x[1], 5), round(float(eval(self.func, {'x': x[0], 'y': x[1]})), 5), k
            

            H = np.array(hessian_func(x_k[0], x_k[1]), dtype=float)
            

            H_inv = np.linalg.inv(H)

            if np.all(np.linalg.eigvals(H_inv) > 0):

                d_k = -H_inv @ grad
            else:

                d_k = -grad
            

            if np.array_equal(d_k, -H_inv @ grad):

                x_k1 = x_k + d_k
            else:

                t = 1.0
                while True:
                    x_k1 = x_k + t * d_k
                    f_k = float(eval(self.func, {'x': x_k[0], 'y': x_k[1]}))
                    f_k1 = float(eval(self.func, {'x': x_k1[0], 'y': x_k1[1]}))
                    if f_k1 < f_k:
                        break
                    t *= 0.5

            if np.linalg.norm(x_k1 - x_k) < e2 and abs(float(eval(self.func, {'x': x_k1[0], 'y': x_k1[1]})) - abs(float(eval(self.func, {'x': x_k[0], 'y': x_k[1]}))) < e2):
                x = x_k1.tolist()
                return round(x[0], 5), round(x[1], 5), round(float(eval(self.func, {'x': x[0], 'y': x[1]})), 5), k

            x_k = x_k1
            k += 1
            
def test():
    finder = ExtremumFinder()
    finder.SetFunc("2 * x ** 2 + 0.1 * x * y + 2 * y ** 2")
    x = [1.5, 0.5]
    e1 = 0.0001
    e2 = 0.0001
    M = 1000
    result = finder.nyuton(x, e1, e2, M)
    print(result)
    
# test()