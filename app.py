import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import random
import os
import requests
import html as html_lib

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Gong cha – Dashboard Avis Google",
    page_icon="🧋",
    layout="wide",
)

# ─── Branding CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Vidaloka&family=Poppins:wght@400;500;600&display=swap');

    html, body, [class*="css"], .stApp {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-family: 'Poppins', sans-serif !important;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Vidaloka', serif !important;
        color: #000000 !important;
    }
    p, span, div, label, li {
        font-family: 'Poppins', sans-serif !important;
        color: #000000 !important;
    }
    header[data-testid="stHeader"] {
        background-color: #ffffff !important;
        border-bottom: 2px solid #c8102e;
    }
    section[data-testid="stSidebar"] {
        background-color: #f8f8f8 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #000000 !important;
        font-family: 'Poppins', sans-serif !important;
    }
    .stButton > button {
        background-color: #c8102e !important;
        color: #ffffff !important;
        border: none;
        border-radius: 6px;
        font-family: 'Poppins', sans-serif !important;
    }
    .stButton > button:hover {
        background-color: #a00d24 !important;
        color: #ffffff !important;
    }
    /* ── Onglets ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 2px solid #eeeeee;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Poppins', sans-serif !important;
        font-weight: 500 !important;
        color: #555555 !important;
        background-color: transparent !important;
        border: 2px solid transparent !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 8px 20px !important;
        transition: all 0.2s ease !important;
        position: relative;
        bottom: -2px;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #c8102e !important;
        border-color: #c8102e !important;
        background-color: #fff5f5 !important;
    }
    .stTabs [aria-selected="true"] {
        color: #c8102e !important;
        border-color: #c8102e !important;
        border-bottom-color: #ffffff !important;
        background-color: #ffffff !important;
        font-weight: 600 !important;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        display: none !important;
    }
    .stMetric label, .stMetric [data-testid="stMetricValue"] {
        color: #000000 !important;
        font-family: 'Poppins', sans-serif !important;
    }
    .stSelectbox label, .stSlider label {
        color: #000000 !important;
        font-family: 'Poppins', sans-serif !important;
    }
    .stSelectbox > div > div {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #cccccc !important;
    }
    .stSelectbox > div > div > div {
        color: #000000 !important;
    }
    [data-baseweb="select"] {
        background-color: #ffffff !important;
    }
    [data-baseweb="select"] * {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    [data-baseweb="popover"] * {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    [role="listbox"] {
        background-color: #ffffff !important;
    }
    [role="option"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    [role="option"]:hover {
        background-color: #f5f5f5 !important;
    }
    [data-testid="stExpander"] summary {
        color: #000000 !important;
        font-family: 'Poppins', sans-serif !important;
    }
    .stTextArea textarea {
        font-family: 'Poppins', sans-serif !important;
        color: #000000 !important;
    }
    hr { border-color: #eeeeee; }
</style>
""", unsafe_allow_html=True)

# ─── Stores ─────────────────────────────────────────────────────────────────
STORES = {
    "FR001": {"name": "Gong cha Mouffetard – Paris V",        "country": "France",   "location_id": "01705875247679560607"},
    "FR002": {"name": "Gong cha Place d'Italie – Paris XIII", "country": "France",   "location_id": "15591641451818809160"},
    "FR003": {"name": "Gong cha Paris Rambuteau",             "country": "France",   "location_id": "04393882467532873946"},
    "FR004": {"name": "Gong cha Angers",                      "country": "France",   "location_id": "13804649806498896511"},
    "FR005": {"name": "Gong cha Toulouse",                    "country": "France",   "location_id": "09057985996391839636"},
    "BE001": {"name": "Gong cha The Mint – Bruxelles",        "country": "Belgique", "location_id": "02421871038781132236"},
    "BE002": {"name": "Gong cha Charleroi Ville 2",           "country": "Belgique", "location_id": "10189574050012545821"},
    "BE003": {"name": "Gong cha Mons",                        "country": "Belgique", "location_id": "16874631373780109329"},
}

USER_STORES = {
    "admin":        list(STORES.keys()),
    "franchisé_fr": ["FR001","FR002","FR003","FR004","FR005"],
    "franchisé_be": ["BE001","BE002","BE003"],
}

# ─── Gemini AI helper ────────────────────────────────────────────────────────
def generate_ai_response(comment, sentiment, store_name):
    """Generate a review response using Gemini API."""
    try:
        api_key = st.secrets["gemini"]["api_key"]
    except Exception:
        return None, "Clé Gemini introuvable dans les secrets Streamlit."

    tone_instructions = {
        "Positif": (
            "Ton chaleureux, enthousiaste et reconnaissant. "
            "Remercie sincèrement le client et invite-le à revenir."
        ),
        "Neutre": (
            "Ton professionnel et courtois. "
            "Remercie le client et propose-lui de découvrir d'autres saveurs."
        ),
        "Négatif": (
            "Ton empathique, compréhensif et solution-focused. "
            "Excuse-toi sincèrement, reconnaît le problème et propose une solution concrète."
        ),
    }
    tone = tone_instructions.get(sentiment, tone_instructions["Neutre"])

    seo_keywords = (
        "bubble tea, boba, thé tapioca, perles de tapioca, Gong cha, "
        "thé premium, boisson artisanale, milk tea, fruit tea"
    )

    prompt = (
        f"Tu es le responsable du {store_name}, enseigne Gong cha de bubble tea.\n"
        f"Rédige une réponse à cet avis Google en français (3-4 phrases max).\n\n"
        f"Avis du client : \"{comment}\"\n\n"
        f"Consignes de ton : {tone}\n"
        f"Intègre naturellement 1-2 mots-clés SEO parmi : {seo_keywords}\n"
        f"Signe avec 'L'équipe {store_name}'.\n"
        f"Réponse :"
    )

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash-lite")
        response = model.generate_content(prompt)
        return response.text.strip(), None
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


# ─── Google API helpers ───────────────────────────────────────────────────────
def get_access_token():
    """Exchange refresh token for access token."""
    try:
        creds = st.secrets["google"]
        resp = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id":     creds["client_id"],
                "client_secret": creds["client_secret"],
                "refresh_token": creds["refresh_token"],
                "grant_type":    "refresh_token",
            },
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json().get("access_token")
    except Exception:
        return None


def get_account_id(access_token):
    """Fetch the first Google Business account ID."""
    try:
        resp = requests.get(
            "https://mybusinessaccountmanagement.googleapis.com/v1/accounts",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )
        resp.raise_for_status()
        accounts = resp.json().get("accounts", [])
        if accounts:
            # resource name like "accounts/123456789"
            return accounts[0]["name"]
        return None
    except Exception:
        return None


@st.cache_data(ttl=1800)
def fetch_reviews_from_api(account_name, location_id, access_token):
    """Fetch reviews for one location from Google Business Profile API."""
    try:
        url = f"https://mybusiness.googleapis.com/v4/{account_name}/locations/{location_id}/reviews"
        reviews = []
        page_token = None
        while True:
            params = {"pageSize": 50}
            if page_token:
                params["pageToken"] = page_token
            resp = requests.get(
                url,
                headers={"Authorization": f"Bearer {access_token}"},
                params=params,
                timeout=15,
            )
            if resp.status_code != 200:
                break
            data = resp.json()
            reviews.extend(data.get("reviews", []))
            page_token = data.get("nextPageToken")
            if not page_token:
                break
        return reviews
    except Exception:
        return []


def reply_to_review(account_name, location_id, review_id, reply_text, access_token):
    """Post a reply to a Google review."""
    url = f"https://mybusiness.googleapis.com/v4/{account_name}/locations/{location_id}/reviews/{review_id}/reply"
    resp = requests.put(
        url,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        json={"comment": reply_text},
        timeout=15,
    )
    return resp.status_code == 200


def star_to_int(star_rating):
    mapping = {"ONE": 1, "TWO": 2, "THREE": 3, "FOUR": 4, "FIVE": 5}
    return mapping.get(star_rating, 3)


def sentiment_from_rating(rating):
    if rating >= 4:
        return "Positif"
    elif rating <= 2:
        return "Négatif"
    return "Neutre"


# ─── Mock data (fallback) ────────────────────────────────────────────────────
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
                "review_id":  "",
            })
    return pd.DataFrame(rows)


def load_real_data(stores_to_load):
    """Try to load real data from API; return (df, is_real)."""
    token = get_access_token()
    if not token:
        return get_mock_data(), False

    account = get_account_id(token)
    if not account:
        return get_mock_data(), False

    rows = []
    for store_id, store in stores_to_load.items():
        reviews = fetch_reviews_from_api(account, store["location_id"], token)
        for r in reviews:
            rating = star_to_int(r.get("starRating", "THREE"))
            comment = r.get("comment", "")
            author  = r.get("reviewer", {}).get("displayName", "Anonyme")
            create_time = r.get("createTime", "")
            try:
                date = datetime.fromisoformat(create_time.replace("Z", "+00:00"))
            except Exception:
                date = datetime.now()
            reply = r.get("reviewReply", {}).get("comment", "")
            review_id = r.get("reviewId", "")
            rows.append({
                "store_id":   store_id,
                "store_name": store["name"],
                "country":    store["country"],
                "date":       date,
                "rating":     rating,
                "comment":    comment,
                "sentiment":  sentiment_from_rating(rating),
                "author":     author,
                "response":   reply,
                "review_id":  review_id,
                "_account":   account,
                "_location":  store["location_id"],
                "_token":     token,
            })

    if rows:
        return pd.DataFrame(rows), True
    return get_mock_data(), False


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

# Load data
with st.spinner("Chargement des avis..."):
    df_all, is_real = load_real_data(user_stores)

if is_real:
    st.sidebar.success("✅ Données réelles Google")
else:
    st.sidebar.info("📊 Données de démonstration\n\nVérifiez vos secrets API pour les données réelles.")

# Filter
df_f = df_all[df_all["store_id"].isin(list(filtered_stores.keys()))].copy()
if sel_store != "Tous":
    df_f = df_f[df_f["store_name"] == sel_store]

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📊 Tableau de bord", "💬 Répondre aux avis"])

with tab1:
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
        fig.update_layout(height=360, coloraxis_showscale=False,
                          margin=dict(l=0,r=0,t=10,b=0),
                          paper_bgcolor="white", plot_bgcolor="white", font_color="#000000")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("#### Répartition des sentiments")
        sc = df_f["sentiment"].value_counts().reset_index()
        sc.columns = ["Sentiment", "Nombre"]
        cmap = {"Positif":"#2ecc71","Neutre":"#f39c12","Négatif":"#c8102e"}
        fig = px.pie(sc, values="Nombre", names="Sentiment",
                     color="Sentiment", color_discrete_map=cmap, hole=0.4)
        fig.update_layout(height=360, margin=dict(l=0,r=0,t=10,b=0),
                          paper_bgcolor="white", plot_bgcolor="white", font_color="#000000")
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
    fig.update_layout(height=360, yaxis_range=[0,5],
                      margin=dict(l=0,r=0,t=10,b=0),
                      paper_bgcolor="white", plot_bgcolor="white", font_color="#000000")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("#### Répondre aux avis")
    if is_real:
        st.success("✅ Les réponses seront publiées directement sur Google Business Profile.")
    else:
        st.info("Les réponses seront publiées sur Google une fois l'API connectée.")

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

    if "responses" not in st.session_state:
        st.session_state.responses = {}
    if "open_cards" not in st.session_state:
        st.session_state.open_cards = {}

    sentiment_colors = {"Positif": "#2ecc71", "Neutre": "#f39c12", "Négatif": "#c8102e"}
    sentiment_labels = {"Positif": "Positif", "Neutre": "Neutre", "Négatif": "Négatif"}

    for i, (idx, row) in enumerate(df_reply.head(30).iterrows()):
        stars_filled = int(row["rating"])
        stars_html = "".join([
            f'<span style="color:#f39c12;font-size:16px">★</span>' if j < stars_filled
            else f'<span style="color:#cccccc;font-size:16px">★</span>'
            for j in range(5)
        ])
        response_key = f"response_{idx}"
        saved_response = st.session_state.responses.get(response_key, row.get("response", ""))
        card_open = st.session_state.open_cards.get(response_key, False)

        sent_color = sentiment_colors.get(row["sentiment"], "#888")
        sent_label = sentiment_labels.get(row["sentiment"], "")
        replied_badge = ' &nbsp;<span style="background:#2ecc71;color:white;padding:2px 8px;border-radius:10px;font-size:11px">&#10003; Répondu</span>' if saved_response else ''
        store_name_safe = html_lib.escape(str(row['store_name']))
        author_safe     = html_lib.escape(str(row['author']))
        comment_safe    = html_lib.escape(str(row['comment']))

        header_html = (
            f'<div style="border:1px solid #eee;border-left:4px solid {sent_color};border-radius:8px;'
            f'padding:12px 16px;margin-bottom:4px;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.06)">'
            f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">'
            f'<div><b>{store_name_safe}</b>&nbsp;&nbsp;{stars_html}&nbsp;&nbsp;'
            f'<span style="color:#888;font-size:13px">{author_safe}</span>&nbsp;'
            f'<span style="color:#aaa;font-size:12px">{row["date"].strftime("%d/%m/%Y")}</span>'
            f'{replied_badge}</div>'
            f'<span style="background:{sent_color}22;color:{sent_color};padding:2px 10px;'
            f'border-radius:10px;font-size:12px;font-weight:600">{sent_label}</span>'
            f'</div>'
            f'<div style="margin-top:6px;color:#444;font-size:13px;font-style:italic">&ldquo;{comment_safe}&rdquo;</div>'
            f'</div>'
        )
        st.markdown(header_html, unsafe_allow_html=True)

        btn_label = "▲ Fermer" if card_open else ("✏️ Modifier la réponse" if saved_response else "💬 Répondre")
        if st.button(btn_label, key=f"toggle_{i}"):
            st.session_state.open_cards[response_key] = not card_open
            st.rerun()

        if card_open:
            if saved_response:
                st.success(f"Réponse publiée : *{saved_response}*")

            # AI generation
            ai_key = f"ai_draft_{idx}"
            ai_err_key = f"ai_err_{idx}"
            if st.button("✨ Générer une réponse avec l'IA", key=f"ai_{i}"):
                with st.spinner("Génération en cours..."):
                    draft, err = generate_ai_response(row["comment"], row["sentiment"], row["store_name"])
                if draft:
                    st.session_state[ai_key] = draft
                    st.session_state.pop(ai_err_key, None)
                else:
                    st.session_state[ai_err_key] = err or "Erreur inconnue"
                st.rerun()
            if st.session_state.get(ai_err_key):
                st.error(f"Erreur IA : {st.session_state[ai_err_key]}")

            default_text = st.session_state.get(ai_key, saved_response)
            response_text = st.text_area(
                "Votre réponse",
                value=default_text,
                placeholder="Bonjour, merci pour votre avis...",
                key=f"text_{i}",
                height=120,
            )
            col_send, col_cancel = st.columns([2, 1])
            with col_send:
                if st.button("📤 Envoyer la réponse", key=f"send_{i}", type="primary"):
                    if response_text.strip():
                        success = False
                        if is_real and row.get("review_id") and row.get("_token"):
                            success = reply_to_review(
                                row["_account"],
                                row["_location"],
                                row["review_id"],
                                response_text,
                                row["_token"],
                            )
                        else:
                            success = True
                        if success:
                            st.session_state.responses[response_key] = response_text
                            st.session_state.open_cards[response_key] = False
                            st.success("✅ Réponse publiée sur Google !" if is_real else "✅ Réponse enregistrée !")
                            st.rerun()
                        else:
                            st.error("Erreur lors de l'envoi. Veuillez réessayer.")
                    else:
                        st.warning("Veuillez écrire une réponse avant d'envoyer.")
            with col_cancel:
                if st.button("Annuler", key=f"cancel_{i}"):
                    st.session_state.open_cards[response_key] = False
                    st.rerun()

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
