#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re, math, time, requests, pandas as pd

PDP = "https://www.sephora.my/products/sephora-collection-original-new-cream-lip-stain/v/13-marvelous-mauve"
BV_CONFIG = "https://apps.bazaarvoice.com/deployments/sephora-au/main_site/production/en_MY/api-config.js"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
HEADERS = {"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9", "Referer": "https://www.sephora.my/"}

def get_passkey(config_url: str) -> str | None:
    r = requests.get(config_url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    m = re.search(r'(?:passkey|apiKey)\s*[:=]\s*["\']([A-Za-z0-9]+)["\']', r.text)
    return m.group(1) if m else None

def get_product_id(pdp_url: str) -> str | None:
    html = requests.get(pdp_url, headers=HEADERS, timeout=30).text
    # varios patrones posibles
    for pat in [
        r'data-bv-product-id=["\']([^"\']+)',
        r'"bvProductId"\s*:\s*["\']([^"\']+)',
        r'"ProductId"\s*[:=]\s*["\']([^"\']+)',
        r'productId=([A-Za-z0-9_-]+)',            # p.ej. en los gifs de analytics
        r'ProductId:eq:([A-Za-z0-9_-]+)',         # a veces embebido
    ]:
        m = re.search(pat, html)
        if m:
            return m.group(1)
    return None

def fetch_reviews(passkey: str, product_id: str, locale: str = "en_MY", limit: int = 100) -> pd.DataFrame:
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
    def call(off: int):
        p = params.copy(); p["Offset"] = off
        r = requests.get(BASE, params=p, headers=HEADERS, timeout=30)
        r.raise_for_status()
        return r.json()

    first = call(0)
    total = first.get("TotalResults", len(first.get("Results", [])))
    pages = math.ceil(total / limit)
    rows = first.get("Results", [])[:]
    for i in range(1, pages):
        time.sleep(0.5)  # evita rate limit
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
    return pd.DataFrame(data)

if __name__ == "__main__":
    passkey = get_passkey(BV_CONFIG)
    print("Passkey:", passkey)
    product_id = get_product_id(PDP)
    print("ProductId:", product_id)

    if not passkey:
        raise SystemExit("❌ No pude extraer la passkey desde api-config.js")
    if not product_id:
        raise SystemExit("❌ No pude extraer el ProductId desde la PDP")

    df = fetch_reviews(passkey, product_id, locale="en_MY", limit=100)
    print(df.head())
    df.to_csv("reviews_sephora_my_lip_stain.csv", index=False)
    print("✅ Guardado: reviews_sephora_my_lip_stain.csv | Filas:", len(df))
