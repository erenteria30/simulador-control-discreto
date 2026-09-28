import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Definir variables simbólicas
z, K_sym = sp.symbols('z K')

# ==========================================
# AQUÍ ESTABLECES EL POLINOMIO DEL PUNTO 4:
# P(z) = z^2 + (K - 0.2)z + K
# ==========================================
char_eq = z**2 + (K_sym - 0.2)*z + K_sym

print("\n" + "="*40)
print(" ANÁLISIS DEL POLINOMIO (PUNTO 4)")
print("="*40)
print(f"Ecuación Característica: {char_eq} = 0")
print("="*40 + "\n")

# Interfaz gráfica con matplotlib nativo
fig, (ax_pz, ax_step) = plt.subplots(1, 2, figsize=(12, 5))
fig.canvas.manager.set_window_title("Simulador - Criterio Routh-Hurwitz / Jury")
plt.subplots_adjust(bottom=0.25, wspace=0.3)

# Slider para modificar K
ax_slider = plt.axes([0.2, 0.1, 0.6, 0.03])
k_slider = Slider(
    ax=ax_slider,
    label='Ganancia (K)',
    valmin=-2.0,
    valmax=2.0,
    valinit=0.5,
    valstep=0.01
)

def update(val):
    K_val = k_slider.val
    
    # Evaluar el polinomio con el valor actual de K
    poly_eval = sp.simplify(char_eq.subs(K_sym, K_val))
    
    # Extraer coeficientes de z
    poly = sp.Poly(poly_eval, z)
    coeffs = [float(c) for c in poly.all_coeffs()]
    
    # Raíces (polos del sistema)
    polos = np.roots(coeffs)
    
    # --- Gráfica 1: Plano Z (Polos) ---
    ax_pz.clear()
    theta = np.linspace(0, 2*np.pi, 100)
    ax_pz.plot(np.cos(theta), np.sin(theta), 'r--', label='Círculo Unitario (|z|=1)')
    ax_pz.axhline(0, color='black', lw=0.8)
    ax_pz.axvline(0, color='black', lw=0.8)
    
    ax_pz.scatter(np.real(polos), np.imag(polos), marker='x', color='blue', s=120, label='Raíces (Polos)')
    
    ax_pz.set_title(f"Raíces en el Plano Z (K = {K_val:.2f})")
    ax_pz.set_xlim([-2.0, 2.0])
    ax_pz.set_ylim([-2.0, 2.0])
    ax_pz.set_xlabel("Eje Real")
    ax_pz.set_ylabel("Eje Imaginario")
    ax_pz.grid(True)
    ax_pz.legend()
    
    # Criterio de estabilidad discreta: módulo de los polos < 1
    es_estable = all(np.abs(p) < 1.0 for p in polos)
    estado_txt = "ESTABLE" if es_estable else "INESTABLE"
    color_txt = "green" if es_estable else "red"
    ax_pz.text(0.05, 0.90, f"Sistema: {estado_txt}", transform=ax_pz.transAxes, 
               fontsize=12, fontweight='bold', color=color_txt, bbox=dict(facecolor='white', alpha=0.8))

    # --- Gráfica 2: Respuesta Temporal al Escalón ---
    ax_step.clear()
    N = 30
    u = np.ones(N)
    y = np.zeros(N)
    
    # Normalizar coeficientes para ecuación de diferencias a y b (asumiendo numerador = 1 o término independiente)
    a = [x / coeffs[0] for x in coeffs]
    b = [1.0] if len(coeffs) == 3 else [0.0, 1.0] # Ajuste simplificado para visualización de escalón
    
    for k in range(N):
        val_b = sum(b[j] * u[k - j] for j in range(len(b)) if k - j >= 0)
        val_a = sum(a[j] * y[k - j] for j in range(1, len(a)) if k - j >= 0)
        y[k] = val_b - val_a
        
    ax_step.stem(range(N), y, linefmt='b-', markerfmt='bo', basefmt='r-')
    ax_step.set_title("Comportamiento Temporal aproximado")
    ax_step.set_xlabel("Muestra (k)")
    ax_step.set_ylabel("Amplitud")
    ax_step.grid(True)
    
    fig.canvas.draw_idle()

k_slider.on_changed(update)
update(k_slider.val)
plt.show()