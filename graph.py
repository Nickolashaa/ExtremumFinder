import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def plot_function(func_str: str, a: float, b: float, n_points=1000):
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

    plt.xlim(a, b)
    plt.savefig("pic.png", dpi=100, bbox_inches='tight', transparent=False)
    plt.close()
    
    image = Image.open("pic.png")
    image = image.resize((400, 300))
    image.save("pic.png")