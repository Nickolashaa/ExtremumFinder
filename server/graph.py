import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import plotly.graph_objects as go
from sympy import sympify, lambdify
from sympy.abc import x, y


def plot_function(func_str: str, a: float, b: float, point_x: float, point_y: float, n_points=1000):
    plt.style.use('dark_background')
    
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='#1a1a1a')
    
    x = np.linspace(a, b, n_points)
    y = eval(func_str, {'x': x, 'np': np})

    ax.plot(x, y, 'b-', linewidth=2, label=f'$f(x) = {func_str}$')

    ax.axhline(0, color='white', linewidth=1)
    ax.axvline(0, color='white', linewidth=1)

    ax.grid(True, linestyle='--', alpha=0.5, color='gray')
    
    ax.spines['left'].set_linewidth(2)
    ax.spines['left'].set_color('red')
    ax.spines['right'].set_linewidth(2)
    ax.spines['right'].set_color('red')

    ax.scatter(point_x, point_y, color='lime', s=100, zorder=5, 
                label=f'Point ({point_x}, {point_y})')

    plt.xlim(a, b)
    plt.savefig("client/static/pic/first.png", dpi=100, bbox_inches='tight', transparent=False)
    plt.close()
    
    image = Image.open("client/static/pic/first.png")
    image = image.resize((646, 476))
    image.save("client/static/pic/first.png")
    

def plot_function_from_string(func_str, x_range=(-5,5), y_range=(-5,5), points=100):
    try:
        expr = sympify(func_str)
        func = lambdify((x, y), expr, modules=['numpy', 'math'])
        
        x_vals = np.linspace(x_range[0], x_range[1], points)
        y_vals = np.linspace(y_range[0], y_range[1], points)
        X, Y = np.meshgrid(x_vals, y_vals)
        
        try:
            Z = func(X, Y)
        except:
            Z = np.zeros_like(X)
            for i in range(len(x_vals)):
                for j in range(len(y_vals)):
                    try:
                        Z[j,i] = func(x_vals[i], y_vals[j])
                    except:
                        Z[j,i] = np.nan
        
        fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
        
        fig.update_layout(
            title=f'График функции: {func_str}',
            scene=dict(
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Z'
            ),
            autosize=False,
            width=800,
            height=600
        )
        
        fig.write_html("client/static/graph.html")
        
        return fig
    
    except Exception as e:
        print(f"Ошибка: {e}")
        return None