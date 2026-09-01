# Relooking v2 — style SaaS moderne, couleurs Gong cha

Cette version remplace la précédente (celle avec la sidebar brun torréfié).
Structure inspirée de ta référence : sidebar en dégradé de marque, cartes
blanches arrondies avec ombre douce, KPI avec badges d'icônes colorés,
onglets en forme de pilule.

Même méthode d'application : GitHub → `app.py` → icône crayon ✏️ → remplacer
les blocs ci-dessous → "Commit changes". Si tu avais déjà appliqué le guide
précédent, ces édits le remplacent simplement (cherche le même bloc `<style>`,
peu importe sa version actuelle).

---

## Édit 1 — Remplacer tout le bloc CSS

Cherche le bloc entre `st.markdown("""` (juste après le commentaire
`# ─── Branding CSS ───`) et `""", unsafe_allow_html=True)` (juste avant
`# ─── Stores ───`). Remplace-le entièrement par :

```python
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Vidaloka&family=Poppins:wght@400;500;600;700;800&display=swap');

:root {
    --ink: #2B1B12;
    --muted: #8A7A69;
    --paper: #F7F4EF;
    --surface: #FFFFFF;
    --line: #ECE4D8;
    --wine: #A81438;
    --wine-dark: #7D0F2A;
    --wine-light: #C8355B;
    --gold: #C9A227;
    --sage: #4C8C6B;
    --rust: #B3492A;
    --shadow: 0 4px 20px rgba(43,27,18,0.06);
}

html, body, [class*="css"], .stApp {
    background-color: var(--paper) !important;
    color: var(--ink) !important;
    font-family: 'Poppins', sans-serif !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Vidaloka', serif !important;
    color: var(--ink) !important;
}

p, span, div, label, li {
    font-family: 'Poppins', sans-serif !important;
    color: var(--ink) !important;
}

header[data-testid="stHeader"] {
    background-color: var(--paper) !important;
    border-bottom: none;
}

/* ── Sidebar : dégradé de marque façon SaaS ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(160deg, var(--wine-dark) 0%, var(--wine) 55%, var(--wine-light) 100%) !important;
    border-right: none;
}
section[data-testid="stSidebar"] * {
    color: #FBEAEE !important;
    font-family: 'Poppins', sans-serif !important;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    font-family: 'Vidaloka', serif !important;
    color: #ffffff !important;
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.18) !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    border-radius: 10px !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #ffffff !important;
}
section[data-testid="stSidebar"] [data-testid="stExpander"] {
    background-color: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 12px !important;
}
section[data-testid="stSidebar"] .stButton > button {
    background-color: rgba(255,255,255,0.15) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    border-radius: 999px !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background-color: rgba(255,255,255,0.28) !important;
}

/* ── Boutons zone principale : pilules pleines ── */
.stButton > button {
    background-color: var(--wine) !important;
    color: #ffffff !important;
    border: none;
    border-radius: 999px !important;
    padding: 8px 22px !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 600 !important;
    box-shadow: var(--shadow);
    transition: background-color 0.15s ease, transform 0.1s ease;
}
.stButton > button:hover {
    background-color: var(--wine-dark) !important;
    transform: translateY(-1px);
}

/* ── Onglets en forme de pilule ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: var(--surface);
    padding: 6px;
    border-radius: 999px;
    border: 1px solid var(--line);
    display: inline-flex;
    box-shadow: var(--shadow);
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 600 !important;
    color: var(--muted) !important;
    background-color: transparent !important;
    border: none !important;
    border-radius: 999px !important;
    padding: 8px 20px !important;
}
.stTabs [aria-selected="true"] {
    color: #ffffff !important;
    background-color: var(--wine) !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }

.stSelectbox label, .stSlider label {
    color: var(--ink) !important;
    font-family: 'Poppins', sans-serif !important;
}
.stSelectbox > div > div {
    background-color: var(--surface) !important;
    color: var(--ink) !important;
    border: 1px solid var(--line) !important;
    border-radius: 10px !important;
}
[data-baseweb="select"] * { background-color: var(--surface) !important; color: var(--ink) !important; }
[data-baseweb="popover"] * { background-color: var(--surface) !important; color: var(--ink) !important; }
[role="option"]:hover { background-color: #FFF1F1 !important; }

[data-testid="stExpander"] {
    background-color: var(--surface) !important;
    border: 1px solid var(--line) !important;
    border-radius: 14px !important;
    box-shadow: var(--shadow);
}
[data-testid="stExpander"] summary {
    color: var(--ink) !important;
    font-family: 'Poppins', sans-serif !important;
}

.stTextArea textarea {
    font-family: 'Poppins', sans-serif !important;
    color: var(--ink) !important;
    background-color: var(--surface) !important;
    border: 1.5px solid var(--line) !important;
    border-radius: 12px !important;
}
.stTextArea textarea:focus {
    border-color: var(--wine) !important;
    box-shadow: 0 0 0 3px rgba(168,20,56,0.12) !important;
    outline: none !important;
}

hr { border-color: var(--line); }

/* ── KPI cards avec badge d'icône ── */
.kpi-card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 20px;
    box-shadow: var(--shadow);
    height: 100%;
}
.kpi-icon {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    margin-bottom: 12px;
    color: #ffffff;
}
.kpi-card .kpi-label {
    font-size: 12.5px;
    color: var(--muted);
    font-weight: 500;
    margin-bottom: 2px;
}
.kpi-card .kpi-value {
    font-family: 'Poppins', sans-serif;
    font-weight: 800;
    font-size: 28px;
    color: var(--ink);
    line-height: 1.1;
}

/* ── Cartes graphiques / conteneurs blancs arrondis ── */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 18px !important;
}
</style>
""", unsafe_allow_html=True)
```

---

## Édit 2 — Cartes KPI avec badges d'icônes

Cherche le bloc des 4 métriques (`st.metric(...)` d'origine, ou le
`kpi_card(...)` si tu as déjà appliqué le guide v1) et remplace-le par :

```python
    def kpi_card(icon, label, value, badge_color="#A81438"):
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon" style="background:{badge_color}">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        kpi_card("⭐", "Note moyenne", f"{df_f['rating'].mean():.2f} / 5", "#C9A227")
    with k2:
        kpi_card("💬", "Total avis", f"{len(df_f)}", "#A81438")
    with k3:
        kpi_card("😊", "Avis positifs", f"{(df_f['sentiment']=='Positif').mean()*100:.0f}%", "#4C8C6B")
    with k4:
        kpi_card("😞", "Avis négatifs", f"{(df_f['sentiment']=='Négatif').mean()*100:.0f}%", "#B3492A")
```

---

## Édit 3 — Couleurs de sentiment (graphiques + cartes d'avis)

Identique au guide précédent — si tu ne l'as pas encore fait :

Dans le bloc du graphique en barres, remplace :
```python
color_continuous_scale=["#c8102e","#f39c12","#2ecc71"],
```
par :
```python
color_continuous_scale=["#B3492A","#C9A227","#4C8C6B"],
```

Remplace :
```python
cmap = {"Positif":"#2ecc71","Neutre":"#f39c12","Négatif":"#c8102e"}
```
par :
```python
cmap = {"Positif":"#4C8C6B","Neutre":"#C9A227","Négatif":"#B3492A"}
```

Dans l'onglet "Répondre aux avis", remplace :
```python
sentiment_colors = {"Positif": "#2ecc71", "Neutre": "#f39c12", "Négatif": "#c8102e"}
```
par :
```python
sentiment_colors = {"Positif": "#4C8C6B", "Neutre": "#C9A227", "Négatif": "#B3492A"}
```

Et pour les étoiles, remplace `#f39c12` par `#C9A227` dans la ligne :
```python
f'<span style="color:#f39c12;font-size:16px">★</span>' if j < stars_filled
```

---

## Édit 4 — Cartes d'avis arrondies (cohérence visuelle)

Dans l'onglet "Répondre aux avis", cherche cette ligne (début du HTML de
chaque carte d'avis) :

```python
            f'<div style="border:1px solid #eee;border-left:4px solid {sent_color};border-radius:8px;'
            f'padding:12px 16px;margin-bottom:4px;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.06)">'
```

Remplace par :

```python
            f'<div style="border:1px solid #ECE4D8;border-left:4px solid {sent_color};border-radius:16px;'
            f'padding:14px 18px;margin-bottom:4px;background:#fff;box-shadow:0 4px 20px rgba(43,27,18,.06)">'
```

---

Résultat attendu : sidebar en dégradé rouge vin → rouge clair (comme le
violet de ta référence, mais en marque Gong cha), cartes blanches arrondies
avec ombre douce, badges d'icônes colorés sur chaque KPI, onglets en pilule
rouge plein quand actifs.
