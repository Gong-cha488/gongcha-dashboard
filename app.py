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

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 18px !important;
}
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

        model = genai.GenerativeModel("models/gemini-3.6-flash")
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Supprimer le formatage markdown gras (**mot**)
        import re
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        return text, None
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


def test_api_connection():
    """Test each step of the API connection and return a detailed report."""
    results = []

    # Step 1: Check secrets
    try:
        creds = st.secrets["google"]
        has_client_id     = bool(creds.get("client_id"))
        has_client_secret = bool(creds.get("client_secret"))
        has_refresh_token = bool(creds.get("refresh_token"))
        if has_client_id and has_client_secret and has_refresh_token:
            results.append(("✅", "Secrets Streamlit", "client_id, client_secret, refresh_token trouvés"))
        else:
            missing = [k for k, v in [("client_id", has_client_id), ("client_secret", has_client_secret), ("refresh_token", has_refresh_token)] if not v]
            results.append(("❌", "Secrets Streamlit", f"Manquants : {', '.join(missing)}"))
            return results
    except Exception as e:
        results.append(("❌", "Secrets Streamlit", f"Section [google] introuvable : {e}"))
        return results

    # Step 2: Get access token
    try:
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
        data = resp.json()
        if resp.status_code == 200 and "access_token" in data:
            access_token = data["access_token"]
            results.append(("✅", "Token OAuth", "Access token obtenu avec succès"))
        else:
            error_msg = data.get("error_description") or data.get("error") or str(data)
            results.append(("❌", "Token OAuth", f"Échec ({resp.status_code}) : {error_msg}"))
            return results
    except Exception as e:
        results.append(("❌", "Token OAuth", f"Erreur réseau : {e}"))
        return results

    # Step 3: Get account
    try:
        resp = requests.get(
            "https://mybusinessaccountmanagement.googleapis.com/v1/accounts",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )
        data = resp.json()
        if resp.status_code == 200:
            accounts = data.get("accounts", [])
            if accounts:
                account_name = accounts[0]["name"]
                results.append(("✅", "Compte Google Business", f"Compte trouvé : {account_name}"))
            else:
                results.append(("⚠️", "Compte Google Business", "Aucun compte trouvé (vérifiez les droits du compte Google)"))
                return results
        else:
            error_msg = data.get("error", {}).get("message") or str(data)
            results.append(("❌", "Compte Google Business", f"Échec ({resp.status_code}) : {error_msg}"))
            return results
    except Exception as e:
        results.append(("❌", "Compte Google Business", f"Erreur : {e}"))
        return results

    # Step 4: Fetch reviews for first store
    try:
        first_store = list(STORES.values())[0]
        url = f"https://mybusiness.googleapis.com/v4/{account_name}/locations/{first_store['location_id']}/reviews"
        resp = requests.get(
            url,
            headers={"Authorization": f"Bearer {access_token}"},
            params={"pageSize": 1},
            timeout=10,
        )
        data = resp.json()
        if resp.status_code == 200:
            reviews = data.get("reviews", [])
            results.append(("✅", "Avis Google", f"{len(reviews)} avis récupéré(s) pour {first_store['name']}"))
        else:
            error_msg = data.get("error", {}).get("message") or str(data)
            results.append(("❌", "Avis Google", f"Échec ({resp.status_code}) : {error_msg}"))
    except Exception as e:
        results.append(("❌", "Avis Google", f"Erreur : {e}"))

    return results


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

# Diagnostic API
with st.sidebar.expander("🔧 Tester la connexion API"):
    if st.button("▶ Lancer le diagnostic", key="diag_btn"):
        with st.spinner("Test en cours..."):
            diag_results = test_api_connection()
        for icon, step, detail in diag_results:
            if icon == "✅":
                st.success(f"**{step}**\n\n{detail}")
            elif icon == "❌":
                st.error(f"**{step}**\n\n{detail}")
            else:
                st.warning(f"**{step}**\n\n{detail}")

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
    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Note moyenne par magasin")
        sr = df_f.groupby("store_name")["rating"].mean().reset_index()
        sr.columns = ["Magasin", "Note"]
        sr = sr.sort_values("Note")
        fig = px.bar(sr, x="Note", y="Magasin", orientation="h",
                     color="Note", color_continuous_scale=["#B3492A","#C9A227","#4C8C6B"],
                     range_color=[1,5], range_x=[0,5])
        fig.update_layout(height=360, coloraxis_showscale=False,
                          margin=dict(l=0,r=0,t=10,b=0),
                          paper_bgcolor="white", plot_bgcolor="white", font_color="#000000")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("#### Répartition des sentiments")
        sc = df_f["sentiment"].value_counts().reset_index()
        sc.columns = ["Sentiment", "Nombre"]
        cmap = {"Positif":"#4C8C6B","Neutre":"#C9A227","Négatif":"#B3492A"}
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

    sentiment_colors = {"Positif": "#4C8C6B", "Neutre": "#C9A227", "Négatif": "#B3492A"}
    sentiment_labels = {"Positif": "Positif", "Neutre": "Neutre", "Négatif": "Négatif"}

    for i, (idx, row) in enumerate(df_reply.head(30).iterrows()):
        stars_filled = int(row["rating"])
        stars_html = "".join([
            f'<span style="color:#C9A227;font-size:16px">★</span>' if j < stars_filled
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
            f'<div style="border:1px solid #ECE4D8;border-left:4px solid {sent_color};border-radius:16px;'
            f'padding:14px 18px;margin-bottom:4px;background:#fff;box-shadow:0 4px 20px rgba(43,27,18,.06)">'
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
                    st.session_state[f"text_{i}"] = draft  # injecte dans le textarea
                    st.session_state.pop(ai_err_key, None)
                else:
                    st.session_state[ai_err_key] = err or "Erreur inconnue"
                st.rerun()
            if st.session_state.get(ai_err_key):
                st.error(f"Erreur IA : {st.session_state[ai_err_key]}")

            # Initialise le textarea avec la réponse existante si pas encore défini
            if f"text_{i}" not in st.session_state:
                st.session_state[f"text_{i}"] = saved_response
            response_text = st.text_area(
                "Votre réponse",
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
