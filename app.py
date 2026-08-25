import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import requests
import random

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Gong cha – Dashboard Avis Google",
    page_icon="🧋",
    layout="wide",
)

# ─── Stores ─────────────────────────────────────────────────────────────────
STORES = {
    "FR001": {"name": "Gong cha Paris Opéra",  "country": "France",   "location_id": ""},
    "FR002": {"name": "Gong cha Paris Marais",  "country": "France",   "location_id": ""},
    "FR003": {"name": "Gong cha Lyon",           "country": "France",   "location_id": ""},
    "FR004": {"name": "Gong cha Bordeaux",       "country": "France",   "location_id": ""},
    "FR005": {"name": "Gong cha Marseille",      "country": "France",   "location_id": ""},
    "FR006": {"name": "Gong cha Toulouse",       "country": "France",   "location_id": ""},
    "FR007": {"name": "Gong cha Lille",          "country": "France",   "location_id": ""},
    "BE001": {"name": "Gong cha Bruxelles",      "country": "Belgique", "location_id": ""},
    "BE002": {"name": "Gong cha Anvers",         "country": "Belgique", "location_id": ""},
    "BE003": {"name": "Gong cha Gand",           "country": "Belgique", "location_id": ""},
}

USER_STORES = {
    "admin":        list(STORES.keys()),
    "franchisé_fr": ["FR001","FR002","FR003","FR004","FR005","FR006","FR007"],
    "franchisé_be": ["BE001","BE002","BE003"],
}

# ─── Mock data ───────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def get_mock_data():
    random.seed(42)
    comments_pos = [
        "Excellent service, les boissons sont délicieuses !",
        "Le bubble tea est parfait, je reviendrai !",
        "Très bon rapport qualité/prix, staff sympa.",
        "J'adore cet endroit, ambiance super.",
        "Les thés sont frais et sucrés exactement comme je les aime.",
        "Rapide, propre et vraiment bon !",
        "Meilleur bubble tea de la ville sans hésitation.",
    ]
    comments_neu = [
        "Correct, rien d'exceptionnel.",
        "Bons produits mais file d'attente assez longue.",
        "Service standard, boissons agréables.",
    ]
    comments_neg = [
        "Attente trop longue pour une simple commande.",
        "Prix un peu élevés pour la quantité servie.",
        "Commande incorrecte, mais résolue rapidement par le staff.",
    ]

    rows = []
    for store_id, store in STORES.items():
        n = random.randint(45, 150)
        for _ in range(n):
            days_ago = random.randint(0, 365)
            date = datetime.now() - timedelta(days=days_ago)
            rating = random.choices([1,2,3,4,5], weights=[3,5,10,35,47])[0]
            if rating >= 4:
                sentiment, comment = "Positif",  random.choice(comments_pos)
            elif rating <= 2:
                sentiment, comment = "Négatif",  random.choice(comments_neg)
            else:
                sentiment, comment = "Neutre",   random.choice(comments_neu)
            rows.append({
                "store_id":   store_id,
                "store_name": store["name"],
                "country":    store["country"],
                "date":       date,
                "rating":     rating,
                "comment":    comment,
                "sentiment":  sentiment,
                "author":     f"Utilisateur{random.randint(100,999)}",
            })
    return pd.DataFrame(rows)

# ─── Authentication ───────────────────────────────────────────────────────────
with open("users.yaml") as f:
    config = yaml.load(f, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

name, authentication_status, username = authenticator.login("main")

# ─── Not logged in ────────────────────────────────────────────────────────────
if authentication_status is False:
    st.error("Nom d'utilisateur ou mot de passe incorrect")
    st.stop()

if authentication_status is None:
    st.markdown("""
        <div style="text-align:center;padding:80px 0">
            <h1>🧋 Gong cha</h1>
            <h3 style="color:#888">Dashboard Avis Google</h3>
            <p style="color:#aaa;margin-top:24px">Connectez-vous pour accéder au tableau de bord</p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─── Logged in ────────────────────────────────────────────────────────────────
user_store_ids = USER_STORES.get(username, [])
user_stores    = {k: v for k, v in STORES.items() if k in user_store_ids}

# Header
col_title, _, col_logout = st.columns([4, 2, 1])
with col_title:
    st.title("🧋 Gong cha — Dashboard Avis Google")
with col_logout:
    authenticator.logout("Déconnexion", "main")
st.markdown(f"Bienvenue, **{name}**")
st.markdown("---")

# Sidebar
st.sidebar.title("🔍 Filtres")
countries = sorted(set(s["country"] for s in user_stores.values()))
sel_country = st.sidebar.selectbox("Pays", ["Tous"] + countries)

filtered_stores = user_stores
if sel_country != "Tous":
    filtered_stores = {k: v for k, v in user_stores.items() if v["country"] == sel_country}

store_names = ["Tous"] + [v["name"] for v in filtered_stores.values()]
sel_store = st.sidebar.selectbox("Magasin", store_names)

st.sidebar.markdown("---")
st.sidebar.info("📊 Données : démonstration\n\nLes données réelles seront chargées une fois l'API Google configurée.")

# Data
df = get_mock_data()
df_f = df[df["store_id"].isin(list(filtered_stores.keys()))]
if sel_store != "Tous":
    df_f = df_f[df_f["store_name"] == sel_store]

# ─── KPIs ────────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("⭐ Note moyenne",    f"{df_f['rating'].mean():.2f} / 5")
k2.metric("💬 Total avis",      f"{len(df_f)}")
k3.metric("😊 Avis positifs",   f"{(df_f['sentiment']=='Positif').mean()*100:.0f}%")
k4.metric("😞 Avis négatifs",   f"{(df_f['sentiment']=='Négatif').mean()*100:.0f}%")

st.markdown("---")

# ─── Charts row 1 ─────────────────────────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.markdown("#### Note moyenne par magasin")
    sr = df_f.groupby("store_name")["rating"].mean().reset_index()
    sr.columns = ["Magasin", "Note"]
    sr = sr.sort_values("Note")
    fig = px.bar(sr, x="Note", y="Magasin", orientation="h",
                 color="Note", color_continuous_scale=["#e74c3c","#f39c12","#2ecc71"],
                 range_color=[1, 5], range_x=[0, 5])
    fig.update_layout(height=360, coloraxis_showscale=False,
                      margin=dict(l=0,r=0,t=10,b=0))
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("#### Répartition des sentiments")
    sc = df_f["sentiment"].value_counts().reset_index()
    sc.columns = ["Sentiment", "Nombre"]
    cmap = {"Positif":"#2ecc71","Neutre":"#f39c12","Négatif":"#e74c3c"}
    fig = px.pie(sc, values="Nombre", names="Sentiment",
                 color="Sentiment", color_discrete_map=cmap, hole=0.4)
    fig.update_layout(height=360, margin=dict(l=0,r=0,t=10,b=0))
    st.plotly_chart(fig, use_container_width=True)

# ─── Rating evolution ─────────────────────────────────────────────────────────
st.markdown("#### Évolution de la note dans le temps")
df_f2 = df_f.copy()
df_f2["month"] = df_f2["date"].dt.to_period("M").astype(str)

if sel_store == "Tous":
    monthly = df_f2.groupby(["month","store_name"])["rating"].mean().reset_index()
    monthly.columns = ["Mois","Magasin","Note"]
    fig = px.line(monthly, x="Mois", y="Note", color="Magasin", markers=True)
else:
    monthly = df_f2.groupby("month")["rating"].mean().reset_index()
    monthly.columns = ["Mois","Note"]
    fig = px.line(monthly, x="Mois", y="Note", markers=True)

fig.update_layout(height=360, yaxis_range=[0,5], margin=dict(l=0,r=0,t=10,b=0))
st.plotly_chart(fig, use_container_width=True)

# ─── Reviews table ────────────────────────────────────────────────────────────
st.markdown("#### Derniers avis")
rating_range = st.select_slider("Filtrer par note ⭐", options=[1,2,3,4,5], value=(1,5))
df_table = df_f[
    (df_f["rating"] >= rating_range[0]) &
    (df_f["rating"] <= rating_range[1])
].sort_values("date", ascending=False).copy()

df_table["Date"]        = df_table["date"].dt.strftime("%d/%m/%Y")
df_table["Note"]        = df_table["rating"].apply(lambda x: "⭐"*x)
df_table["Sentiment"]   = df_table["sentiment"]
df_table["Magasin"]     = df_table["store_name"]
df_table["Commentaire"] = df_table["comment"]
df_table["Auteur"]      = df_table["author"]

st.dataframe(
    df_table[["Date","Magasin","Note","Sentiment","Commentaire","Auteur"]],
    use_container_width=True,
    hide_index=True,
)
