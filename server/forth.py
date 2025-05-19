import numpy as np
import sympy as sp
from string import ascii_letters
from scipy.optimize import minimize


class ExtremumFinder:
    def __init__(self):
        self.funcF = None
        self.funcG = None
    
    def SetFuncF(self, func):
        variable = list()
        if '=' in func:
            func = func[func.index('=') + 1:]
        func = func.replace("^", "**")
        func = func.replace("e", "2.71828182845904")
        self.funcF = func
        for letter in ascii_letters:
            if letter in func:
                variable.append(letter)
                if len(variable) == 2:
                    break
                
        self.funcF = self.funcF.replace(variable[0], "(x)")
        self.funcF = self.funcF.replace(variable[1], "(y)")
        
    def SetFuncG(self, func):
        variable = list()
        if '=' in func:
            func = func[func.index('=') + 1:]
        func = func.replace("^", "**")
        func = func.replace("e", "2.71828182845904")
        self.funcG = func
        for letter in ascii_letters:
            if letter in func:
                variable.append(letter)
                if len(variable) == 2:
                    break
                
        self.funcG = self.funcG.replace(variable[0], "(x)")
        self.funcG = self.funcG.replace(variable[1], "(y)")
        
    def penalty_method_search(self, x0, e, r0, C, M=100):
        x_syms = sp.symbols('x y')
        
        f_expr = sp.sympify(self.funcF)
        g_expr = sp.sympify(self.funcG)
        
        f_func = sp.lambdify(x_syms, f_expr, modules=['numpy'])
        g_func = sp.lambdify(x_syms, g_expr, modules=['numpy'])

        def f(x):
            return f_func(*x)

        def g(x):
            return g_func(*x)

        def penalty(x, r):
            return r * g(x)**2

        def F(x, r):
            return f(x) + penalty(x, r)

        r = r0
        x = np.array(x0)
        
        for k in range(M):
            result = minimize(F, x, args=(r,), method='BFGS')
            x_new = result.x
            P_val = penalty(x_new, r)

            if P_val <= e:
                break

            r *= C
            x = x_new

        return x_new.tolist(), round(float(f(x_new)), 5), k + 1
    
    
    
    def barrier_method_search(self, x0, e, r0, C, method, m=100):
        x_syms = sp.symbols('x y')
        
        f_expr = sp.sympify(self.funcF)
        g_expr = sp.sympify(self.funcG)
        
        f_func = sp.lambdify(x_syms, f_expr, modules='numpy')
        g_func = sp.lambdify(x_syms, g_expr, modules='numpy')

        def f(x):
            return f_func(*x)

        def g(x):
            return g_func(*x)

        def barrier(x, r):
            gx = g(x)
            if method == "inverse":
                if gx >= 0:
                    return np.inf
                return -r / gx
            elif method == "log":
                if gx >= 0:
                    return np.inf
                return -r * np.log(-gx)

        def F(x, r):
            return f(x) + barrier(x, r)

        r = r0
        x = np.array(x0)

        for k in range(m):
            result = minimize(F, x, args=(r,), method='BFGS')
            x_new = result.x
            penalty_value = abs(barrier(x_new, r))

            if penalty_value <= e:
                break

            r /= C
            x = x_new

        return x_new, round(f(x_new), 5), k + 1
            
def test():
    finder = ExtremumFinder()
    finder.SetFuncF("x**2 + y**2 - 6*x + 2*y + 25")
    finder.SetFuncG("x + 10*y - 7")
    x = [0, 0]
    e = 8
    r0 = 0.05
    C = 0.5
    result = finder.penalty_method_search(x, e, r0, C)
    print(result)
    
# test()