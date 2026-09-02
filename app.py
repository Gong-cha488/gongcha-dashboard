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
import base64

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Gong cha – Dashboard Avis Google",
    page_icon="🧋",
    layout="wide",
)

# ─── Branding CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Vidaloka&family=Poppins:wght@400;500;600;700&display=swap');

:root {
    --red: #C10230;
    --red-dark: #93011F;
    --black: #1A1414;
    --white: #FFFFFF;
    --line: #E5E1DD;
    --grey: #8A8078;
}

html, body, [class*="css"], .stApp {
    background-color: var(--white) !important;
    color: var(--black) !important;
    font-family: 'Poppins', sans-serif !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Vidaloka', serif !important;
    color: var(--black) !important;
}

p, span, div, label, li {
    font-family: 'Poppins', sans-serif !important;
    color: var(--black) !important;
}

header[data-testid="stHeader"] {
    background-color: var(--white) !important;
    border-bottom: 1px solid var(--line);
}

/* ── Sidebar : blanche, logo en haut, filtres en dessous ── */
section[data-testid="stSidebar"] {
    background-color: var(--white) !important;
    border-right: 1px solid var(--line);
}
section[data-testid="stSidebar"] * {
    color: var(--black) !important;
    font-family: 'Poppins', sans-serif !important;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 700 !important;
    color: var(--black) !important;
}
section[data-testid="stSidebar"] hr {
    border-color: var(--line) !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: var(--white) !important;
    border: 1.5px solid var(--black) !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: var(--black) !important;
}

/* ── Boutons : par défaut noir sur blanc ; actif/principal = rouge sur blanc ── */
.stButton > button {
    background-color: var(--white) !important;
    color: var(--black) !important;
    border: 1.5px solid var(--black) !important;
    border-radius: 8px !important;
    padding: 8px 20px !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 600 !important;
    box-shadow: none !important;
    transition: all 0.15s ease;
}
.stButton > button:hover {
    background-color: var(--black) !important;
    color: var(--white) !important;
    border-color: var(--black) !important;
}
.stButton > button[kind="primary"],
button[data-testid="baseButton-primary"] {
    background-color: var(--red) !important;
    color: var(--white) !important;
    border: 1.5px solid var(--red) !important;
}
.stButton > button[kind="primary"]:hover,
button[data-testid="baseButton-primary"]:hover {
    background-color: var(--red-dark) !important;
    border-color: var(--red-dark) !important;
    color: var(--white) !important;
}

/* ── Onglets : actif = petite pilule fond rose pâle + texte rouge gras ; inactif = texte noir, sans fond ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    border-bottom: none;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
    color: var(--black) !important;
    background-color: transparent !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 6px 14px !important;
}
.stTabs [aria-selected="true"] {
    color: var(--red) !important;
    background-color: #FBE9ED !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }

/* Masque l'indicateur d'exécution Streamlit (ex: "fetch_reviews_from_api(...)") */
[data-testid="stStatusWidget"] { display: none !important; }

.stSelectbox label, .stSlider label {
    color: var(--black) !important;
    font-family: 'Poppins', sans-serif !important;
}
.stSelectbox > div > div {
    background-color: var(--white) !important;
    color: var(--black) !important;
    border: 1.5px solid var(--black) !important;
    border-radius: 8px !important;
}
[data-baseweb="select"] * { background-color: var(--white) !important; color: var(--black) !important; }
div[data-baseweb="popover"],
div[data-baseweb="popover"] div,
ul[data-baseweb="menu"] {
    background-color: var(--white) !important;
}
[data-baseweb="popover"] * { background-color: var(--white) !important; color: var(--black) !important; }
li[role="option"] { background-color: var(--white) !important; color: var(--black) !important; }
li[role="option"]:hover,
li[aria-selected="true"] { background-color: #FBE9ED !important; color: var(--black) !important; }

[data-testid="stExpander"] {
    background-color: var(--white) !important;
    border: 1.5px solid var(--black) !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"] summary {
    color: var(--black) !important;
    font-family: 'Poppins', sans-serif !important;
}

.stTextArea textarea {
    font-family: 'Poppins', sans-serif !important;
    color: var(--black) !important;
    background-color: var(--white) !important;
    border: 1.5px solid var(--black) !important;
    border-radius: 8px !important;
}
.stTextArea textarea:focus {
    border-color: var(--red) !important;
    box-shadow: 0 0 0 2px rgba(193,2,48,0.15) !important;
    outline: none !important;
}

hr { border-color: var(--line); }

/* ── Cartes KPI : fond gris très clair, badge d'icône, ombre douce ── */
.kpi-card {
    background: #F7F5F3;
    border: none;
    border-radius: 16px;
    padding: 18px 20px;
    height: 100%;
    box-shadow: 0 2px 8px rgba(26,20,20,0.05);
}
.kpi-card .kpi-label {
    font-size: 13px;
    color: var(--grey);
    font-weight: 500;
    margin-bottom: 4px;
}
.kpi-card .kpi-value {
    font-family: 'Vidaloka', serif;
    font-size: 26px;
    color: var(--black);
    line-height: 1.1;
    margin-top: 10px;
}

/* Cartes de graphiques : sélecteur basé sur key= (stable, cf. doc Streamlit st.container) */
div[class*="st-key-chart_"] {
    border-radius: 14px !important;
    border: 1.5px solid var(--line) !important;
    border-top: 3px solid var(--red) !important;
    box-shadow: 0 8px 24px rgba(26,20,20,0.09), 0 2px 6px rgba(26,20,20,0.06) !important;
    padding: 10px 6px !important;
    background: var(--white) !important;
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}
div[class*="st-key-chart_"]:hover {
    box-shadow: 0 12px 32px rgba(26,20,20,0.13), 0 4px 10px rgba(26,20,20,0.08) !important;
    transform: translateY(-2px);
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
@st.cache_data(ttl=3000)  # 50 min : un peu moins que la durée de vie du token (1h)
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


@st.cache_data(ttl=3000)
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

# Header
col_title, col_logout = st.columns([5, 1])
with col_title:
    st.markdown("<h1 style='margin-top:10px'>Dashboard Avis Google</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#888'>Bienvenue, <b>{name}</b></p>", unsafe_allow_html=True)
with col_logout:
    st.write("")
    authenticator.logout("Déconnexion", "main")

st.markdown("---")

# Sidebar — bandeau établissement en haut, façon Malou
countries = sorted(set(s["country"] for s in user_stores.values()))
all_store_names = ["Tous"] + [v["name"] for v in user_stores.values()]

st.sidebar.markdown("""
<div style="display:flex; align-items:center; gap:8px; padding:10px 4px 4px 4px;">
    <div style="width:26px; height:26px; border-radius:50%; background:#C10230;
                display:flex; align-items:center; justify-content:center;
                color:#fff; font-size:13px;">🏠</div>
    <span style="font-weight:700; font-family:'Poppins', sans-serif; font-size:14px;">Établissement</span>
</div>
""", unsafe_allow_html=True)
sel_store = st.sidebar.selectbox(
    "Établissement", all_store_names,
    format_func=lambda x: "Tous les établissements" if x == "Tous" else x,
    label_visibility="collapsed",
)
st.sidebar.markdown("<hr style='margin:8px 0 14px 0;'>", unsafe_allow_html=True)

# Menu de navigation — seul "E-réputation" est actif pour l'instant
def _nav_item(icon, label, active=False, soon=False):
    if active:
        st.sidebar.markdown(f"""
        <div style="display:flex; align-items:center; gap:10px; padding:9px 12px;
                    border-radius:10px; background:#FBE9ED; color:#C10230;
                    font-weight:700; font-family:'Poppins', sans-serif; font-size:14.5px; margin-bottom:2px;">
            <span style="font-size:16px;">{icon}</span> {label}
        </div>
        """, unsafe_allow_html=True)
    else:
        soon_tag = ('<span style="margin-left:auto; font-size:10px; color:#B0A89E; '
                    'background:#F1EEEA; padding:1px 7px; border-radius:8px;">Bientôt</span>') if soon else ""
        st.sidebar.markdown(f"""
        <div style="display:flex; align-items:center; gap:10px; padding:9px 12px;
                    border-radius:10px; color:#B0A89E;
                    font-family:'Poppins', sans-serif; font-size:14.5px; margin-bottom:2px;">
            <span style="font-size:16px;">{icon}</span> {label} {soon_tag}
        </div>
        """, unsafe_allow_html=True)

_nav_item("🔍", "Référencement", soon=True)
_nav_item("⭐", "E-réputation", active=True)
_nav_item("🚀", "Boosters", soon=True)
_nav_item("📈", "Statistiques", soon=True)

st.sidebar.markdown("<hr style='margin:14px 0;'>", unsafe_allow_html=True)

with st.sidebar.expander("Filtre par pays"):
    sel_country = st.selectbox("Pays", ["Tous"] + countries, label_visibility="collapsed")

filtered_stores = user_stores
if sel_country != "Tous":
    filtered_stores = {k: v for k, v in user_stores.items() if v["country"] == sel_country}

# Load data
with st.spinner("Chargement des avis..."):
    df_all, is_real = load_real_data(user_stores)

# Filter
if sel_store != "Tous":
    df_f = df_all[df_all["store_name"] == sel_store].copy()
else:
    df_f = df_all[df_all["store_id"].isin(list(filtered_stores.keys()))].copy()

# Logo Gong cha tout en bas de la sidebar
def _logo_b64():
    if os.path.exists("logo.png"):
        with open("logo.png", "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_b64 = _logo_b64()
st.sidebar.markdown("<div style='margin-top:60px;'></div>", unsafe_allow_html=True)
if logo_b64:
    st.sidebar.markdown(f"""
    <div style="display:flex; align-items:center; gap:8px; padding:10px 4px;
                border-top:1px solid #ECE8E3;">
        <img src="data:image/png;base64,{logo_b64}" style="width:26px; height:26px; border-radius:50%; object-fit:cover;">
        <span style="font-family:'Vidaloka', serif; font-size:15px; color:#1A1414;">Gong cha</span>
    </div>
    """, unsafe_allow_html=True)

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📊 Tableau de bord", "💬 Répondre aux avis"])

with tab1:
    def kpi_card(label, value, icon, icon_bg):
        st.markdown(f"""
        <div class="kpi-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div class="kpi-label">{label}</div>
                <div style="width:34px; height:34px; border-radius:10px; background:{icon_bg};
                            display:flex; align-items:center; justify-content:center;
                            font-size:15px; flex-shrink:0;">{icon}</div>
            </div>
            <div class="kpi-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        kpi_card("Note moyenne", f"{df_f['rating'].mean():.2f} / 5", "⭐", "#FBE9ED")
    with k2:
        kpi_card("Total avis", f"{len(df_f)}", "💬", "#F1EEEA")
    with k3:
        kpi_card("Avis positifs", f"{(df_f['sentiment']=='Positif').mean()*100:.0f}%", "😊", "#E4F1E9")
    with k4:
        kpi_card("Avis négatifs", f"{(df_f['sentiment']=='Négatif').mean()*100:.0f}%", "😞", "#FBE9ED")
    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True, key="chart_bar"):
            st.markdown("#### Note moyenne par magasin")
            sr = df_f.groupby("store_name")["rating"].mean().reset_index()
            sr.columns = ["Magasin", "Note"]
            sr = sr.sort_values("Note")
            fig = px.bar(sr, x="Note", y="Magasin", orientation="h",
                         color="Note", color_continuous_scale=["#C10230","#D4A017","#1E8449"],
                         range_color=[1,5], range_x=[0,5])
            fig.update_layout(height=340, coloraxis_showscale=False,
                              margin=dict(l=0,r=0,t=10,b=0),
                              paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#000000")
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        with st.container(border=True, key="chart_pie"):
            st.markdown("#### Répartition des sentiments")
            sc = df_f["sentiment"].value_counts().reset_index()
            sc.columns = ["Sentiment", "Nombre"]
            cmap = {"Positif":"#1E8449","Neutre":"#D4A017","Négatif":"#C10230"}
            fig = px.pie(sc, values="Nombre", names="Sentiment",
                         color="Sentiment", color_discrete_map=cmap, hole=0.4)
            fig.update_layout(height=340, margin=dict(l=0,r=0,t=10,b=0),
                              paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#000000")
            st.plotly_chart(fig, use_container_width=True)

    with st.container(border=True, key="chart_line"):
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
        fig.update_layout(height=340, yaxis_range=[0,5],
                          margin=dict(l=0,r=0,t=10,b=0),
                          paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#000000")
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

    sentiment_colors = {"Positif": "#1E8449", "Neutre": "#D4A017", "Négatif": "#C10230"}
    sentiment_labels = {"Positif": "Positif", "Neutre": "Neutre", "Négatif": "Négatif"}

    for i, (idx, row) in enumerate(df_reply.head(30).iterrows()):
        stars_filled = int(row["rating"])
        stars_html = "".join([
            f'<span style="color:#C10230;font-size:16px">★</span>' if j < stars_filled
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
            f'<div style="border:1.5px solid #1A1414;border-left:4px solid {sent_color};border-radius:10px;'
            f'padding:14px 18px;margin-bottom:4px;background:#fff;box-shadow:none">'
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
