#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re, math, time, requests, pandas as pd

PDP = "https://www.sephora.my/products/sephora-collection-original-new-cream-lip-stain/v/13-marvelous-mauve"
BV_BASE = "https://apps.bazaarvoice.com/deployments/sephora-au/main_site/production/en_MY"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
HEADERS = {"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9", "Referer": "https://www.sephora.my/"}

CONFIG_CANDIDATES = [
    f"{BV_BASE}/api-config.js",
    f"{BV_BASE}/swat_reviews-config.js",
    f"{BV_BASE}/rating_summary-config.js",
    # si hiciera falta, añade más locales: en_SG, en_AU, etc.
]

# regex más flexible: captura comillas y cualquier cosa no-comilla
RE_PASSKEY = re.compile(r'["\'](?:passkey|apiKey|apikey)["\']\s*[:=]\s*["\']([^"\']+)["\']', re.IGNORECASE)

# varios patrones posibles para ProductId; añade comodín 'default-xxx-yyy'
PRODUCT_PATTERNS = [
    r'data-bv-product-id=["\']([^"\']+)',
    r'"bvProductId"\s*:\s*["\']([^"\']+)["\']',
    r'"ProductId"\s*[:=]\s*["\']([^"\']+)["\']',
    r'ProductId:eq:([A-Za-z0-9_\-]+)',
    r'productId=([A-Za-z0-9_\-]+)',
    r'(default-\d{3,}-\d{3,})',  # comodín muy útil
]

def fetch_text(url):
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r.text

def discover_passkey():
    for url in CONFIG_CANDIDATES:
        try:
            txt = fetch_text(url)
            m = RE_PASSKEY.search(txt)
            if m:
                print(f"[passkey] encontrada en: {url}")
                return m.group(1)
        except Exception as e:
            print(f"[warn] no pude leer {url}: {e}")
    return None

def discover_product_id_from_pdp(pdp_url):
    html = fetch_text(pdp_url)
    for pat in PRODUCT_PATTERNS:
        m = re.search(pat, html, flags=re.IGNORECASE)
        if m:
            return m.group(1)
    return None

def fetch_reviews(passkey, product_id, locale="en_MY", limit=100):
    BASE = "https://api.bazaarvoice.com/data/reviews.json"
    params = {
        "passkey": passkey,
        "Filter": f"ProductId:eq:{product_id}",
        "Include": "Products,Comments",
        "Stats": "Reviews",
        "Sort": "SubmissionTime:desc",
        "Limit": limit,
        "Offset": 0,
        "Locale": locale
    }

    def call(off):
        p = params.copy(); p["Offset"] = off
        r = requests.get(BASE, params=p, headers=HEADERS, timeout=30)
        r.raise_for_status()
        return r.json()

    first = call(0)
    total = first.get("TotalResults", len(first.get("Results", [])))
    pages = math.ceil(total / limit)
    rows = first.get("Results", [])[:]
    for i in range(1, pages):
        time.sleep(0.5)
        rows += call(i * limit).get("Results", [])

    data = [{
        "review_id": rv.get("Id"),
        "rating": rv.get("Rating"),
        "title": rv.get("Title"),
        "text": rv.get("ReviewText"),
        "submission_time": rv.get("SubmissionTime"),
        "nickname": rv.get("UserNickname"),
        "helpful_yes": rv.get("TotalPositiveFeedbackCount"),
        "helpful_no": rv.get("TotalNegativeFeedbackCount"),
        "context": rv.get("ContextDataValues"),
    } for rv in rows]
    return pd.DataFrame(data), total

if __name__ == "__main__":
    passkey = discover_passkey()
    print("Passkey:", passkey)

    product_id = discover_product_id_from_pdp(PDP)
    print("ProductId:", product_id)

    # FALLBACKS:
    # 1) Si viste el ProductId en el log (tu caso): ponlo a mano aquí
    if not product_id:
        product_id = "default-100151-258071"  # <-- del log XHR que capturaste
        print("Fallback ProductId (manual):", product_id)

    if not passkey:
        raise SystemExit("❌ No pude extraer la passkey desde las configs de BV. Abre DevTools/Network y copia 'passkey' de una XHR de reviews.")

    df, total = fetch_reviews(passkey, product_id, locale="en_MY", limit=100)
    print(df.head())
    df.to_csv("reviews_sephora_my_lip_stain.csv", index=False)
    print(f"✅ Guardado: reviews_sephora_my_lip_stain.csv | Total reviews: {total} | Filas: {len(df)}")
