from flask import Flask, render_template, request
from server.graph import plot_function, plot_function_from_string, plot_function_and_constraint_3d



app = Flask(__name__)


@app.route("/")
def HomePage():
    return render_template("home.html")


@app.route("/one-dimensional-optimization", methods=["GET", "POST"])
def OneDimensionalOptimization():
    if request.method == "POST":
        try:
            from server.first import ExtremumFinder
            obj = ExtremumFinder()
            func = request.form.get("func")
            findmin = 1 if request.form.get("MaxOrMin") == "min" else 0
            a = float(request.form.get("a"))
            b = float(request.form.get("b"))
            e = float(request.form.get("e"))
            method = request.form.get("Method")
            obj.SetFunc(func)
            if method == "polovin":
                result, x, y = obj.BisectionMethod(a, b, e, findmin)
            if method == "gold":
                result, x, y = obj.GoldenRatioMethod(a, b, e, findmin)
            if method == "fib":
                result, x, y = obj.FibonacciNumberMethod(a, b, e, findmin)
            plot_function(obj.func, a, b, x, y)
            return render_template("first.html", calculated=result)
        except Exception:
            return render_template("first.html")
    else:
        return render_template("first.html")


@app.route("/multidimensional-optimization", methods=["GET", "POST"])
def MultidimensionalOptimization():
    if request.method == "POST":
        try:
            from server.second import ExtremumFinder
            obj = ExtremumFinder()
            func = request.form.get("func")
            x = [float(request.form.get("a")), float(request.form.get("b"))]
            e1 = float(request.form.get("e1"))
            e2 = float(request.form.get("e2"))
            M = float(request.form.get("M"))
            method = request.form.get("Method")
            obj.SetFunc(func)
            if method == "method1":
                x1, x2, y, k = obj.gradient_descent_constant_step_str(x, e1, e2, M)
            if method == "method2":
                x1, x2, y, k = obj.steepest_gradient_descent(x, e1, e2, M)
            result = list()
            result.append(f"Найденная точка: ({x1}; {x2})")
            result.append(f"Значение функции в точке: {y}")
            result.append(f"Количество итераций: {k}")
            plot_function_from_string(func)
            return render_template("second.html", calculated=result, func=func)
        except Exception as e:
            print(e)
            return render_template("second.html")
    else:
        return render_template("second.html")
    
    
@app.route("/multidimensional-optimization-second", methods=["GET", "POST"])
def MultidimensionalOptimizationSecond():
    if request.method == "POST":
        try:
            from server.third import ExtremumFinder
            obj = ExtremumFinder()
            func = request.form.get("func")
            x = [float(request.form.get("a")), float(request.form.get("b"))]
            e1 = float(request.form.get("e1"))
            e2 = float(request.form.get("e2"))
            M = float(request.form.get("M"))
            obj.SetFunc(func)
            x1, x2, y, k = obj.nyuton(x, e1, e2, M)
            result = list()
            result.append(f"Найденная точка: ({x1}; {x2})")
            result.append(f"Значение функции в точке: {y}")
            result.append(f"Количество итераций: {k}")
            plot_function_from_string(func)
            return render_template("third.html", calculated=result, func=func)
        except Exception as e:
            print(e)
            return render_template("third.html")
    else:
        return render_template("third.html")
    
@app.route("/conditional-optimization", methods=["GET", "POST"])
def ConditionalOptimization():
    if request.method == "POST":
        try:
            from server.forth import ExtremumFinder
            obj = ExtremumFinder()
            funcF = request.form.get("funcF")
            funcG = request.form.get("funcG")
            x = [float(request.form.get("a")), float(request.form.get("b"))]
            e = float(request.form.get("e"))
            r0 = float(request.form.get("r0"))
            c = float(request.form.get("c"))
            method = request.form.get("Method")
            obj.SetFuncF(funcF)
            obj.SetFuncG(funcG)
            if method == "method1":
                x, y, k = obj.penalty_method_search(x, e, r0, c)
            if method == "method2":
                x, y, k = obj.barrier_method_search(x, e, r0, c, method="inverse")
            if method == "method3":
                x, y, k = obj.barrier_method_search(x, e, r0, c, method="log")
            result = list()
            result.append(f"Найденная точка: ({round(x[0], 5)}; {round(x[1], 5)})")
            result.append(f"Значение функции в точке: {y}")
            result.append(f"Количество итераций: {k}")
            plot_function_and_constraint_3d(obj.funcF, obj.funcG)
            return render_template("forth.html", calculated=result, func=funcF)
        except Exception as e:
            print(e)
            return render_template("forth.html")
    else:
        return render_template("forth.html")