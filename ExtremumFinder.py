from string import ascii_letters


class ExtremumFinder:
    def __init__(self):
        self.func = None
        self.variable = None
    
    def SetFunc(self, func):
        if '=' in func:
            func = func[func.index('=') + 1:]
        func = func.replace("^", "**")
        func = func.replace("e", "2.71828182845904")
        self.func = func
        for letter in ascii_letters:
            if letter in func:
                self.variable = letter
                break
            
    def eval(self, x):
        x_str = f"({x})" if x < 0 else str(x)
        answer = self.func.replace(self.variable, x_str)
        return float(eval(answer))
        
    def BisectionMethod(self, a, b, e, findmin):
        base_interval = {
            "a": a,
            "b": b,
        }
        f_a = self.eval(a)
        f_b = self.eval(b)
        if findmin:
            def comparison(a, b):
                return a < b
        else:
            def comparison(a, b):
                return a > b
        L = abs(b - a)
        while L > e:
            x_sr = (a + b) / 2
            f_x_sr = self.eval(x_sr)
            y = a + abs(L) / 4
            z = b - abs(L) / 4
            f_y = self.eval(y)
            f_z = self.eval(z)
            if comparison(f_y, f_x_sr):
                b = x_sr
                x_sr = y
            elif comparison(f_z, f_x_sr):
                a = x_sr
                x_sr = z
            else:
                a = y
                b = z

            L = abs(b - a)
        
        x_ans = (a + b) / 2
        f_x_ans = self.eval(x_ans)
        
        if comparison(f_a, f_x_ans):
            x_ans = base_interval["a"]
            f_x_ans = f_a
        if comparison(f_b, f_x_ans):
            x_ans = base_interval["b"]
            f_x_ans = f_b
        result = f"x* = {x_ans:.5f}\nf(x*) = {f_x_ans:.5f}"
        return result, x_ans, f_x_ans

    
    def GoldenRatioMethod(self, a, b, e, findmin):
        base_interval = {
            "a": a,
            "b": b,
        }
        f_a = self.eval(a)
        f_b = self.eval(b)
        if findmin:
            def comparison(a, b):
                return a <= b
        else:
            def comparison(a, b):
                return a > b
        y = a + ((3 - 5 ** 0.5) / 2) * (b - a)
        z = a + b - y
        delta = None
        while delta is None or delta > e:
            f_y = self.eval(y)
            f_z = self.eval(z)
            if comparison(f_y, f_z):
                b = z
                z = y
                y = a + b - y
            else:
                a = y
                y = z
                z = a + b - z
            
            delta = abs(a - b)
            
        x_ans = (a + b) / 2
        f_x_ans = self.eval(x_ans)
        
        if comparison(f_a, f_x_ans):
            x_ans = base_interval["a"]
            f_x_ans = f_a
        if comparison(f_b, f_x_ans):
            x_ans = base_interval["b"]
            f_x_ans = f_b
        result = f"x* = {x_ans:.5f}\nf(x*) = {f_x_ans:.5f}"
        return result, x_ans, f_x_ans
    
    def NewFibonacci(self, array):
        elem = array[-1] + array[-2]
        array.append(elem)
        return elem

    def FibonacciNumberMethod(self, a, b, e, findmin):
        base_interval = {
            "a": a,
            "b": b,
        }
        f_a = self.eval(a)
        f_b = self.eval(b)
        if findmin:
            def comparison(a, b):
                return a <= b
        else:
            def comparison(a, b):
                return a > b
        l = 2 * e
        L0 = abs(b - a)
        Fib = [1, 1]
        while Fib[-1] < L0 / l:
            self.NewFibonacci(Fib)
        N = len(Fib) - 1
        y = a + (Fib[N-2] / Fib[N]) * (b - a)
        z = a + (Fib[N-1] / Fib[N]) * (b - a)
        f_y = self.eval(y)
        f_z = self.eval(z)
        for k in range(N - 2):
            if comparison(f_y, f_z):
                b = z
                z = y
                y = a + (Fib[N-k-3] / Fib[N-k-1]) * (b - a)
                f_z = f_y
                f_y = self.eval(y)
            else:
                a = y
                y = z
                z = a + (Fib[N-k-2] / Fib[N-k-1]) * (b - a)
                f_y = f_z
                f_z = self.eval(z)
        z = y + e
        f_z = self.eval(z)
        
        if comparison(f_y, f_z):
            b = z
        else:
            a = y
            
        x_ans = (a + b) / 2
        f_x_ans = self.eval(x_ans)
        
        if comparison(f_a, f_x_ans):
            x_ans = base_interval["a"]
            f_x_ans = f_a
        if comparison(f_b, f_x_ans):
            x_ans = base_interval["b"]
            f_x_ans = f_b
        result = f"x* = {x_ans:.5f}\nf(x*) = {f_x_ans:.5f}"
        return result, x_ans, f_x_ans