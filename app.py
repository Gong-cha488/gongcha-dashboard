import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import random
import os

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Gong cha – Dashboard Avis Google",
    page_icon="🧋",
    layout="wide",
)

# ─── Branding CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Brand colors */
    :root {
        --gc-brown: #3d2b1f;
        --gc-red:   #c8102e;
    }
    .stApp { background-color: #fafafa; }
    header[data-testid="stHeader"] { background-color: #ffffff; border-bottom: 2px solid #c8102e; }
    .stButton > button {
        background-color: #c8102e;
        color: white;
        border: none;
        border-radius: 6px;
    }
    .stButton > button:hover { background-color: #a00d24; color: white; }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 16px 20px;
        border-left: 4px solid #c8102e;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    }
    .sidebar .sidebar-content { background-color: #3d2b1f; }
    h1, h2, h3 { color: #3d2b1f; }
</style>
""", unsafe_allow_html=True)

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
                sentiment, comment = "Positif", random.choice(comments_pos)
            elif rating <= 2:
                sentiment, comment = "Négatif", random.choice(comments_neg)
            else:
                sentiment, comment = "Neutre", random.choice(comments_neu)
            rows.append({
                "store_id":   store_id,
                "store_name": store["name"],
                "country":    store["country"],
                "date":       date,
                "rating":     rating,
                "comment":    comment,
                "sentiment":  sentiment,
                "author":     f"Utilisateur{random.randint(100,999)}",
                "response":   "",
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

if authentication_status is False:
    st.error("Nom d'utilisateur ou mot de passe incorrect")
    st.stop()

if authentication_status is None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=320)
        st.markdown("<h3 style='text-align:center;color:#3d2b1f'>Dashboard Avis Google</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#888'>Connectez-vous pour accéder au tableau de bord</p>", unsafe_allow_html=True)
    st.stop()

# ─── Logged in ────────────────────────────────────────────────────────────────
user_store_ids = USER_STORES.get(username, [])
user_stores    = {k: v for k, v in STORES.items() if k in user_store_ids}

# Header with logo
col_logo, col_title, col_logout = st.columns([1, 4, 1])
with col_logo:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=160)
with col_title:
    st.markdown("<h1 style='margin-top:10px'>Dashboard Avis Google</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#888'>Bienvenue, <b>{name}</b></p>", unsafe_allow_html=True)
with col_logout:
    st.write("")
    authenticator.logout("Déconnexion", "main")

st.markdown("---")

# Sidebar
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", use_container_width=True)
st.sidebar.markdown("---")
st.sidebar.title("🔍 Filtres")

countries = sorted(set(s["country"] for s in user_stores.values()))
sel_country = st.sidebar.selectbox("Pays", ["Tous"] + countries)

filtered_stores = user_stores
if sel_country != "Tous":
    filtered_stores = {k: v for k, v in user_stores.items() if v["country"] == sel_country}

store_names = ["Tous"] + [v["name"] for v in filtered_stores.values()]
sel_store = st.sidebar.selectbox("Magasin", store_names)

st.sidebar.markdown("---")
st.sidebar.info("📊 Données de démonstration\n\nConnectez l'API Google pour les données réelles.")

# Data
df = get_mock_data()
df_f = df[df["store_id"].isin(list(filtered_stores.keys()))].copy()
if sel_store != "Tous":
    df_f = df_f[df_f["store_name"] == sel_store]

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📊 Tableau de bord", "💬 Répondre aux avis"])

with tab1:
    # KPIs
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("⭐ Note moyenne",  f"{df_f['rating'].mean():.2f} / 5")
    k2.metric("💬 Total avis",    f"{len(df_f)}")
    k3.metric("😊 Avis positifs", f"{(df_f['sentiment']=='Positif').mean()*100:.0f}%")
    k4.metric("😞 Avis négatifs", f"{(df_f['sentiment']=='Négatif').mean()*100:.0f}%")
    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Note moyenne par magasin")
        sr = df_f.groupby("store_name")["rating"].mean().reset_index()
        sr.columns = ["Magasin", "Note"]
        sr = sr.sort_values("Note")
        fig = px.bar(sr, x="Note", y="Magasin", orientation="h",
                     color="Note", color_continuous_scale=["#c8102e","#f39c12","#2ecc71"],
                     range_color=[1,5], range_x=[0,5])
        fig.update_layout(height=360, coloraxis_showscale=False, margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("#### Répartition des sentiments")
        sc = df_f["sentiment"].value_counts().reset_index()
        sc.columns = ["Sentiment", "Nombre"]
        cmap = {"Positif":"#2ecc71","Neutre":"#f39c12","Négatif":"#c8102e"}
        fig = px.pie(sc, values="Nombre", names="Sentiment",
                     color="Sentiment", color_discrete_map=cmap, hole=0.4)
        fig.update_layout(height=360, margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Évolution de la note dans le temps")
    df_f2 = df_f.copy()
    df_f2["month"] = df_f2["date"].dt.to_period("M").astype(str)
    if sel_store == "Tous":
        monthly = df_f2.groupby(["month","store_name"])["rating"].mean().reset_index()
        monthly.columns = ["Mois","Magasin","Note"]
        fig = px.line(monthly, x="Mois", y="Note", color="Magasin", markers=True,
                      color_discrete_sequence=["#c8102e","#3d2b1f","#f39c12","#2ecc71","#3498db","#9b59b6","#1abc9c","#e67e22","#e74c3c","#2980b9"])
    else:
        monthly = df_f2.groupby("month")["rating"].mean().reset_index()
        monthly.columns = ["Mois","Note"]
        fig = px.line(monthly, x="Mois", y="Note", markers=True,
                      color_discrete_sequence=["#c8102e"])
    fig.update_layout(height=360, yaxis_range=[0,5], margin=dict(l=0,r=0,t=10,b=0))
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("#### Répondre aux avis")
    st.info("Les réponses seront publiées directement sur Google Business Profile une fois l'API connectée.")

    # Filters for this tab
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filter_sentiment = st.selectbox("Filtrer par sentiment", ["Tous","Négatif","Neutre","Positif"])
    with col_f2:
        filter_responded = st.selectbox("Statut réponse", ["Tous","Sans réponse","Avec réponse"])

    df_reply = df_f.sort_values("date", ascending=False).copy()
    if filter_sentiment != "Tous":
        df_reply = df_reply[df_reply["sentiment"] == filter_sentiment]
    if filter_responded == "Sans réponse":
        df_reply = df_reply[df_reply["response"] == ""]
    elif filter_responded == "Avec réponse":
        df_reply = df_reply[df_reply["response"] != ""]

    # Initialize responses in session state
    if "responses" not in st.session_state:
        st.session_state.responses = {}

    for i, (idx, row) in enumerate(df_reply.head(30).iterrows()):
        stars = "⭐" * int(row["rating"])
        sentiment_color = {"Positif":"🟢","Neutre":"🟡","Négatif":"🔴"}.get(row["sentiment"],"⚪")

        with st.expander(f"{sentiment_color} {row['store_name']} — {stars} — {row['author']} ({row['date'].strftime('%d/%m/%Y')})"):
            st.markdown(f"**Commentaire :** {row['comment']}")

            response_key = f"response_{idx}"
            saved_response = st.session_state.responses.get(response_key, "")

            if saved_response:
                st.success(f"✅ Réponse envoyée : *{saved_response}*")
                if st.button("Modifier", key=f"edit_{i}"):
                    del st.session_state.responses[response_key]
                    st.rerun()
            else:
                response_text = st.text_area(
                    "Votre réponse",
                    placeholder="Bonjour, merci pour votre avis...",
                    key=f"text_{i}",
                    height=100
                )
                if st.button("📤 Envoyer la réponse", key=f"send_{i}"):
                    if response_text.strip():
                        st.session_state.responses[response_key] = response_text
                        st.success("✅ Réponse enregistrée ! (sera publiée sur Google une fois l'API connectée)")
                        st.rerun()
                    else:
                        st.warning("Veuillez écrire une réponse avant d'envoyer.")
