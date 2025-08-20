import subprocess
import os

# 📂 Detectar la raíz del proyecto
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(project_root)

# 0️⃣ Crear estructura de carpetas solo si no existe
if not os.path.exists("data"):
    subprocess.run(["bash", os.path.join(project_root, "scripts", "setup_estructura.sh")])
    print("✅ Estructura de carpetas creada")
else:
    print("📁 Estructura de carpetas ya existente")

# Helper para ejecutar scripts python con ruta absoluta
def run_python(script_name):
    script_path = os.path.join(project_root, "scripts", script_name)
    subprocess.run(["python3", script_path])

# 1️⃣ Descarga datasets de Kaggle
run_python("descarga_kaggle_reviews.py")

# 2️⃣ Conversión a Delta
run_python("conversion_a_delta.py")

# 3️⃣ Procesar Open Beauty Facts EAN (descarga y conversión a Delta)
run_python("Open_beauty_facts_EAN.py")

# 4️⃣ Exploraciones de Open Beauty Facts
run_python("exploration_openbeauty_products.py")
run_python("exploration_openbeauty_products_cat+brand.py")

# 5️⃣ Limpieza de datos trusted (solo si existen carpetas de entrada)
if os.path.exists("data/landing/sephora/delta") or os.path.exists("data/landing/ulta/delta"):
    run_python("trusted_clean_driver.py")
    print("✅ trusted_clean_driver.py ejecutado. trusted_clean_single.py es invocado internamente por ese script para cada tabla encontrada.")
else:
    print("⚠️ Carpetas de entrada para limpieza no encontradas. Saltando limpieza.")

# 6️⃣ Explotación skincare
run_python("explotation_skincare.py")

# 7️⃣ Análisis de reseñas skincare
run_python("analisis_skincare_reviews.py")

print("✅ Flujo completo ejecutado correctamente")


