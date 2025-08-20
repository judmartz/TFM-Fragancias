import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# 📂 Rutas de entrada
products_path = "data/trusted/sephora_clean/product_info"
reviews_path = "data/exploitation/products/skincare_reviews"

# 📁 Directorio de salida para gráficos
os.makedirs("output", exist_ok=True)

# 📥 Leer datasets
df_products = pd.read_parquet(products_path, engine='pyarrow')
df_reviews = pd.read_parquet(reviews_path, engine='pyarrow')

# 🧼 Inspección inicial
print(df_products.info())
print(df_products.describe(include='all'))
print(df_products.isna().sum())

print(df_reviews.info())
print(df_reviews.isna().sum())

# 📊 Top 10 marcas con más productos
top_brands = df_products['brand_name'].value_counts().head(10)
plt.figure(figsize=(10, 5))
top_brands.plot(kind='bar', color='green')
plt.title("Top 10 marcas por número de productos")
plt.ylabel("Cantidad de productos")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("output/top_brands.png")

# 💲 Distribución de precios
plt.figure(figsize=(8, 5))
sns.histplot(df_products['price_usd'], bins=30, kde=True, color='skyblue')
plt.title("Distribución de precios (USD)")
plt.xlabel("Precio")
plt.ylabel("Frecuencia")
plt.tight_layout()
plt.savefig("output/precio_histograma.png")

# 🧴 Conteo por categoría principal
plt.figure(figsize=(8, 5))
df_products['primary_category'].value_counts().plot(kind='bar', color='orange')
plt.title("Conteo de productos por categoría principal")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("output/categorias.png")

# ☁️ Nube de palabras (reseñas)
text = " ".join(df_reviews['review_text'].dropna().astype(str).tolist())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Nube de palabras - Reseñas")
plt.tight_layout()
plt.savefig("output/nube_palabras_reviews.png")

print("✅ Gráficos guardados en la carpeta 'output/'")
