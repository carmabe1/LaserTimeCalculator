import svgelements
from svgelements import Path, Matrix

# Simular usuario: archivo 100 unidades (DPI 100) -> quiere 25.4mm
p = Path("M 0 0 L 100 0") # 100 unidades

# Escala: 100 unidades son 1 pulgada (25.4mm)
user_ppi = 100.0
scale_factor = 25.4 / user_ppi

p *= Matrix.scale(scale_factor)
p.reify()
print(f"Resultado final para 100 unids con PPI=100: {p.length()} mm")
