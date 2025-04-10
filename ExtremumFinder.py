from string import ascii_letters


class ExtremumFinder:
    def __init__(self):
        self.func = None
        self.variable = None
    
    def SetFunc(self, func):
        if '=' in func:
            func = func[func.index('=') + 1:]
        func = func.replace("^", "**")
        self.func = func
        for letter in ascii_letters:
            if letter in func:
                self.variable = letter
                break
            
    def eval(self, x):
        return float(eval(self.func.replace(self.variable, str(x))))
        
    def BisectionMethod(self, a, b, e, findmin):
        if findmin:
            x_sr = (a + b) / 2
            L = abs(b - a)
            f_x_sr = self.eval(x_sr)
            while L > e:
                y = a + abs(L) / 4
                z = b - abs(L) / 4
                f_y = self.eval(y)
                f_z = self.eval(z)
                if f_y < f_x_sr:
                    b = x_sr
                    x_sr = y
                elif f_z < f_x_sr:
                    a = x_sr
                    x_sr = z
                else:
                    a = y
                    b = z

                L = abs(b - a)
            
            result = f"x* принадлежит [{a:.5f}, {b:.5f}]\nx* = {(a + b) / 2:.5f}"
            return result
        else:
            pass
    
    def GoldenRatioMethod(self, a, b, e, findmin):
        if findmin:
            y = a + ((3 - 5 ** 0.5) / 2) * (b - a)
            z = a + b - y
            delta = None
            while delta is None or delta > e:
                f_y = self.eval(y)
                f_z = self.eval(z)
                if f_y <= f_z:
                    b = z
                    z = y
                    y = a + b - y
                else:
                    a = y
                    y = z
                    z = a + b - z
                
                delta = abs(a - b)
            result = f"x* принадлежит [{a:.5f}, {b:.5f}]\nx* = {(a + b) / 2:.5f}"
            return result
        else:
            pass
    
    def NewFibonacci(self, array):
        elem = array[-1] + array[-2]
        array.append(elem)
        return elem

    def FibonacciNumberMethod(self, a, b, e, findmin):
        if findmin:
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
                if f_y <= f_z:
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
            
            if f_y < f_z:
                b = z
            else:
                a = y
            
            result = f"x* принадлежит [{a:.5f}, {b:.5f}]\nx* = {(a + b) / 2:.5f}"
            return result
        else:
            pass