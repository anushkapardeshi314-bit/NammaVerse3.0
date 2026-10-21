import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import fitz
import io, os, re, json, hashlib, time, base64
from datetime import datetime, date
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))

@st.cache_data(show_spinner=False)
def b64(name):
    with open(os.path.join(BASE, "assets", name), "rb") as f:
        return base64.b64encode(f.read()).decode()

def img_uri(name): return "data:image/png;base64," + b64(name)

try:
    _icon = Image.open(os.path.join(BASE, "assets", "logo_mark.png"))
except Exception:
    _icon = "ಕ"
st.set_page_config(page_title="Nudimane | Your home for Kannada", page_icon=_icon, layout="wide", initial_sidebar_state="collapsed")

# -------------------- Visual system: Blush & Sage --------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=DM+Sans:wght@400;500;600;700&family=Noto+Sans+Kannada:wght@400;500;600;700&display=swap');
:root{--cream:#FBF6F1;--rose:#E8B4B8;--rose-l:#F6DDE0;--sage:#A8BFA3;--sage-l:#DCE7D8;--sage-d:#6F8F6A;--plum:#3B2A3A;--muted:#7A6A75;--line:#EADFD6;--peach:#F4D0B9;}
html,body,[class*="css"]{font-family:'DM Sans','Noto Sans Kannada',sans-serif;}
.stApp{background:var(--cream);color:var(--plum);}
header[data-testid="stHeader"]{background:transparent;}
[data-testid="stSidebar"],[data-testid="collapsedControl"],[data-testid="stSidebarCollapsedControl"]{display:none;}
.block-container{padding-top:1rem;max-width:1240px;}
h1,h2,h3,.serif{font-family:'Fraunces',Georgia,serif !important;color:var(--plum);}
/* top bar */
.brand{display:flex;align-items:center;gap:.7rem;}
.brand img{width:46px;height:46px;}
.brand b{font-family:'Fraunces',serif;font-size:1.55rem;color:var(--plum);letter-spacing:-.01em;line-height:1;}
.brand small{display:block;color:var(--sage-d);font-size:.68rem;letter-spacing:.16em;text-transform:uppercase;margin-top:3px;font-weight:600;}
div[role="radiogroup"]{gap:.35rem;flex-wrap:wrap;justify-content:flex-end;}
div[role="radiogroup"] label{background:#fff;border:1px solid var(--line);border-radius:999px;padding:.35rem .95rem;cursor:pointer;transition:all .2s;}
div[role="radiogroup"] label>div:first-child{display:none;}
div[role="radiogroup"] label:hover{background:var(--rose-l);transform:translateY(-1px);}
div[role="radiogroup"] label:has(input:checked){background:var(--plum);border-color:var(--plum);}
div[role="radiogroup"] label:has(input:checked) p{color:var(--cream) !important;}
div[role="radiogroup"] label p{font-size:.88rem;font-weight:600;color:var(--plum);}
/* hero */
.hero{display:grid;grid-template-columns:1.05fr 1fr;gap:2.2rem;align-items:center;background:linear-gradient(135deg,var(--rose-l),var(--sage-l));border-radius:36px;padding:2.6rem 2.8rem;margin-top:.6rem;overflow:hidden;}
.hero .eyebrow{color:var(--sage-d);font-weight:700;font-size:.78rem;letter-spacing:.18em;text-transform:uppercase;}
.hero h1{font-size:clamp(2.4rem,4.6vw,4.1rem);line-height:1.05;margin:.6rem 0 1rem;font-weight:700;}
.hero h1 em{color:#C9797F;font-style:italic;}
.hero p{color:var(--muted);font-size:1.08rem;line-height:1.7;max-width:520px;}
.hero img{width:100%;border-radius:28px;box-shadow:0 24px 50px rgba(59,42,58,.18);transform:rotate(1.5deg);}
.chip{display:inline-block;background:#fff;border-radius:999px;padding:.32rem .8rem;margin:.25rem .3rem 0 0;font-size:.8rem;font-weight:600;color:var(--plum);}
.kn-big{font-family:'Noto Sans Kannada';font-size:1.1rem;}
/* sections */
.section-title{font-family:'Fraunces',serif;font-size:2rem;font-weight:700;margin:1.6rem 0 .2rem;color:var(--plum);}
.section-sub{color:var(--muted);margin-bottom:1.1rem;font-size:1.02rem;}
.kicker{color:var(--sage-d);font-weight:700;font-size:.75rem;letter-spacing:.18em;text-transform:uppercase;margin-top:2.2rem;}
/* journey */
.journey{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:.6rem 0 0;}
.step{background:#fff;border:1px solid var(--line);border-radius:22px;padding:1.1rem 1.2rem;position:relative;}
.step .n{width:34px;height:34px;border-radius:50%;background:var(--rose);color:var(--plum);display:flex;align-items:center;justify-content:center;font-weight:700;margin-bottom:.6rem;}
.step:nth-child(even) .n{background:var(--sage);}
.step h4{margin:0 0 .25rem;font-size:1.02rem;color:var(--plum);}
.step p{margin:0;color:var(--muted);font-size:.9rem;line-height:1.5;}
/* pinterest masonry */
.masonry{column-count:3;column-gap:18px;margin-top:.8rem;}
.pin{break-inside:avoid;margin-bottom:18px;border-radius:26px;overflow:hidden;background:#fff;border:1px solid var(--line);box-shadow:0 6px 20px rgba(59,42,58,.05);transition:transform .25s,box-shadow .25s;}
.pin:hover{transform:translateY(-5px);box-shadow:0 18px 34px rgba(59,42,58,.12);}
.pin img{width:100%;display:block;}
.pin .body{padding:1rem 1.2rem 1.25rem;}
.pin .tag{font-size:.7rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--sage-d);}
.pin h3{font-size:1.2rem;margin:.25rem 0 .4rem;}
.pin p{color:var(--muted);font-size:.92rem;line-height:1.55;margin:0;}
.pin.quote{background:var(--plum);padding:1.6rem;}
.pin.quote .kn{font-family:'Noto Sans Kannada';font-size:1.9rem;color:var(--rose);font-weight:600;}
.pin.quote p{color:#E9DDE3;margin-top:.6rem;}
.pin.word{background:var(--sage-l);padding:1.5rem;}
.pin.word .kn{font-family:'Noto Sans Kannada';font-size:2rem;font-weight:600;color:var(--plum);}
@media(max-width:900px){.masonry{column-count:2}.hero{grid-template-columns:1fr}.journey{grid-template-columns:1fr 1fr}}
@media(max-width:560px){.masonry{column-count:1}.journey{grid-template-columns:1fr}.hero{padding:1.6rem}}
/* shared widgets (inner pages) */
.card{background:#fff;border:1px solid var(--line);border-radius:22px;padding:1.1rem 1.25rem;box-shadow:0 5px 18px rgba(59,42,58,.04);}
.card h3{font-size:1.1rem;margin:.25rem 0 .45rem;}
.card p{color:var(--muted);font-size:.92rem;line-height:1.55;margin:0;}
.card .icon{font-size:1.5rem;}
.small-note{color:var(--muted);font-size:.84rem;}
div.stButton>button,div.stDownloadButton>button{border-radius:999px;font-weight:650;border:1px solid var(--line);background:#fff;color:var(--plum);padding:.5rem 1.2rem;transition:all .2s;}
div.stButton>button:hover,div.stDownloadButton>button:hover{background:var(--rose-l);border-color:var(--rose);color:var(--plum);transform:translateY(-1px);}
div.stButton>button[kind="primary"]{background:var(--plum);border-color:var(--plum);color:var(--cream);}
div.stButton>button[kind="primary"]:hover{background:#523a50;color:#fff;}
div[data-testid="stMetric"]{background:#fff;padding:1rem;border:1px solid var(--line);border-radius:20px;}
div[data-testid="stVerticalBlockBorderWrapper"]{border-radius:24px;border-color:var(--line);background:#fff;}
div[data-baseweb="select"]>div,.stTextInput input,.stTextArea textarea{border-radius:14px !important;}
div[data-testid="stAlert"]{border-radius:18px;}
hr{border-color:var(--line);}
.footer{margin-top:3rem;background:var(--plum);border-radius:30px;padding:2rem 2.2rem;color:#E9DDE3;display:flex;gap:1.2rem;align-items:center;flex-wrap:wrap;justify-content:space-between;}
.footer b{font-family:'Fraunces',serif;font-size:1.3rem;color:var(--rose);}
.footer small{color:#BFA9B7;display:block;max-width:560px;margin-top:.3rem;line-height:1.5;}
</style>
""", unsafe_allow_html=True)

if "docs" not in st.session_state: st.session_state.docs = []
if "active_text" not in st.session_state: st.session_state.active_text = ""
if "active_name" not in st.session_state: st.session_state.active_name = ""
if "history" not in st.session_state: st.session_state.history = []
if "page" not in st.session_state: st.session_state.page = "Home"

NAV = {"Home":"Home","Document Studio":"Scan","Ask Your Document":"Ask","Kannada Learning":"Learn",
       "Voice & Pronunciation":"Speak","Namma Heritage Map":"Heritage","Karnataka Travel Planner":"Travel",
       "My Library":"Library","Impact & Quality":"Quality"}

def go(p): st.session_state.page = p

# -------------------- Top bar --------------------
tb1, tb2 = st.columns([1, 2.6], vertical_alignment="center")
with tb1:
    st.markdown(f'<div class="brand"><img src="{img_uri("logo_mark.png")}"/><div><b>Nudimane</b><small>ನುಡಿಮನೆ · Kannada AI</small></div></div>', unsafe_allow_html=True)
with tb2:
    page = st.radio("Navigate", list(NAV.keys()), key="page", format_func=lambda k: NAV[k], horizontal=True, label_visibility="collapsed")

# -------------------- Helpers --------------------
def enhance_image(img, mode="Balanced"):
    img = img.convert("RGB")
    if mode in ("Readable", "Old document"):
        img = ImageEnhance.Contrast(img).enhance(1.45 if mode == "Readable" else 1.8)
        img = ImageEnhance.Sharpness(img).enhance(1.6)
        img = img.filter(ImageFilter.MedianFilter(size=3))
    elif mode == "Handwriting":
        img = ImageEnhance.Contrast(img).enhance(1.2)
        img = ImageEnhance.Sharpness(img).enhance(1.3)
    return img

def ocr_image(img, lang, mode):
    img = enhance_image(img, mode)
    config = "--psm 6"
    try:
        return pytesseract.image_to_string(img, lang=lang, config=config), img
    except Exception as e:
        return "", img

def extract_pdf(uploaded, lang, mode):
    data = uploaded.getvalue()
    doc = fitz.open(stream=data, filetype="pdf")
    page_texts = []
    preview = None
    for idx, page in enumerate(doc):
        native = page.get_text("text").strip()
        # If selectable text exists, preserve it. Otherwise OCR rendered page.
        if len(native) > 20:
            text = native
        else:
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            text, img = ocr_image(img, lang, mode)
            if preview is None: preview = img
        page_texts.append(f"--- Page {idx+1} ---\n{text.strip()}")
    return "\n\n".join(page_texts), preview, len(doc)

def simple_summary(text, max_sentences=5):
    text = re.sub(r'\s+', ' ', text).strip()
    if not text: return "No text available to summarize yet."
    parts = re.split(r'(?<=[.!?।])\s+', text)
    return " ".join(parts[:max_sentences])[:2200]

def extract_dates(text):
    patterns = [
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
        r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',
        r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b'
    ]
    found=[]
    for p in patterns: found += re.findall(p, text, flags=re.I)
    return list(dict.fromkeys(found))

def get_keywords(text, limit=12):
    words = re.findall(r'[\w\u0C80-\u0CFF]{3,}', text.lower())
    stop = {"ಮತ್ತು","ಅಥವಾ","ಇದು","ಅವರು","ಇರುವ","ಮಾಡಲು","ಅದರ","ಎಂದು","with","that","this","from","have","will","your","you","the","and","for","are","was","were","not","can"}
    counts={}
    for w in words:
        if w not in stop: counts[w]=counts.get(w,0)+1
    return sorted(counts.items(), key=lambda x:x[1], reverse=True)[:limit]

def make_doc_record(name, text, kind):
    return {"name":name, "text":text, "kind":kind, "saved_at":datetime.now().strftime("%d %b %Y, %H:%M"), "chars":len(text)}

def set_active(name, text):
    st.session_state.active_name=name
    st.session_state.active_text=text

if page == "Home":
    st.markdown(f"""
    <div class="hero">
      <div>
        <div class="eyebrow">Kannada · Culture · AI</div>
        <h1>A warm little home for <em>ಕನ್ನಡ</em></h1>
        <p>Scan old documents, understand them, hear them spoken, learn the language, and wander through Karnataka — all in one gentle, connected space.</p>
        <span class="chip">📄 Kannada OCR</span><span class="chip">🌱 Learn</span><span class="chip">🔊 Speak</span><span class="chip">🧭 Heritage</span><span class="chip">🗺️ Travel</span>
      </div>
      <img src="{img_uri('hero.png')}" alt="Nudimane"/>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    b1, b2, b3, _ = st.columns([1.1, 1.1, 1.1, 2.7])
    b1.button("📄 Scan a document", type="primary", use_container_width=True, on_click=go, args=("Document Studio",))
    b2.button("🌱 Start learning", use_container_width=True, on_click=go, args=("Kannada Learning",))
    b3.button("🗺️ Plan a trip", use_container_width=True, on_click=go, args=("Karnataka Travel Planner",))

    st.markdown('<div class="kicker">How it flows</div><div class="section-title" style="margin-top:.2rem">From a page to a journey</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="journey">
      <div class="step"><div class="n">1</div><h4>Scan</h4><p>Upload a photo or PDF and get editable Kannada text.</p></div>
      <div class="step"><div class="n">2</div><h4>Understand</h4><p>Summaries, dates, key terms and search inside your document.</p></div>
      <div class="step"><div class="n">3</div><h4>Listen & learn</h4><p>Hear phrases, practise situations, build confidence.</p></div>
      <div class="step"><div class="n">4</div><h4>Explore</h4><p>Discover regional words and plan a trip across Karnataka.</p></div>
    </div>
    """, unsafe_allow_html=True)

    words = [("ನಮಸ್ಕಾರ","Namaskāra","Hello"),("ಧನ್ಯವಾದಗಳು","Dhanyavādagaḷu","Thank you"),("ದಯವಿಟ್ಟು","Dayaviṭṭu","Please"),("ಕ್ಷಮಿಸಿ","Kṣamisi","Excuse me"),("ನೀರು ಬೇಕು","Nīru bēku","I need water"),("ಮತ್ತೊಮ್ಮೆ ಹೇಳಿ","Mattomme hēḷi","Please say it again"),("ನನಗೆ ಸಹಾಯ ಬೇಕು","Nanage sahāya bēku","I need help")]
    kn, ro, en = words[date.today().toordinal() % len(words)]

    st.markdown('<div class="kicker">Explore</div><div class="section-title" style="margin-top:.2rem">Pick what inspires you</div>', unsafe_allow_html=True)
    def pin(img, tag, title, desc):
        return f'<div class="pin"><img src="{img_uri(img)}"/><div class="body"><div class="tag">{tag}</div><h3>{title}</h3><p>{desc}</p></div></div>'
    st.markdown('<div class="masonry">' +
        pin("t_scan.png","Document Intelligence","Turn scans into text","Extract Kannada from photos and PDFs, review uncertain words, then summarise and search.") +
        f'<div class="pin word"><div class="tag" style="color:#6F8F6A;font-weight:700;letter-spacing:.14em;font-size:.7rem">WORD OF THE DAY</div><div class="kn">{kn}</div><p style="color:#3B2A3A;margin:.3rem 0 0"><b>{ro}</b> · {en}</p></div>' +
        pin("t_voice.png","Voice of Kannada","Hear it spoken","Play phrases through your browser's voice and practise repeating them aloud.") +
        pin("t_heritage.png","Heritage","Regional words & stories","Collect expressions from different regions with their meaning and cultural context.") +
        '<div class="pin quote"><div class="kn">ನುಡಿ ಒಂದು ಮನೆ</div><p>Language is a home. Come in, sit down, stay a while.</p></div>' +
        pin("t_learn.png","Learn","Grow a little each day","Situation-based phrases for greetings, travel, food and work with simple practice.") +
        pin("t_travel.png","Travel","Draft your Karnataka trip","Pick days, budget and mood — get a sample itinerary you can download.") +
        pin("t_quality.png","Quality & Trust","Measurable, transparent","An evaluation checklist so OCR accuracy and accessibility are actually tested.") +
        '</div>', unsafe_allow_html=True)
    st.caption("Prototype: OCR, speech and AI quality depend on installed models and services. Always verify important outputs against the original source.")

elif page == "Document Studio":
    st.markdown('<div class="section-title">Document Studio</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">From a photo or scanned page to searchable, editable Kannada text.</div>', unsafe_allow_html=True)
    with st.container(border=True):
        c1,c2,c3=st.columns([1.4,1,1])
        with c1:
            uploaded=st.file_uploader("Upload image or PDF", type=["png","jpg","jpeg","webp","tif","tiff","pdf"])
        with c2:
            language=st.selectbox("OCR language", ["Kannada + English", "Kannada", "English"], index=0)
        with c3:
            mode=st.selectbox("Image enhancement", ["Balanced","Readable","Old document","Handwriting"])
        st.caption("Tip: use a clear, well-lit photo. Handwriting support depends heavily on the OCR model and sample quality.")
        if uploaded:
            if language=="Kannada + English": lang="kan+eng"
            elif language=="Kannada": lang="kan"
            else: lang="eng"
            if st.button("✨ Extract text", type="primary", use_container_width=True):
                with st.spinner("Preparing document and extracting text…"):
                    try:
                        if uploaded.name.lower().endswith(".pdf"):
                            text, preview, pages = extract_pdf(uploaded, lang, mode)
                            st.session_state.page_count=pages
                        else:
                            img=Image.open(uploaded)
                            text, preview=ocr_image(img, lang, mode)
                            st.session_state.page_count=1
                        st.session_state.active_text=text
                        st.session_state.active_name=uploaded.name
                        st.session_state.last_preview=preview
                        st.session_state.last_mode=mode
                        st.session_state.last_kind="PDF" if uploaded.name.lower().endswith(".pdf") else "Image"
                        st.success("Extraction complete. Review and correct the text before using it.")
                    except Exception as e:
                        st.error("Could not process this file. Check that Tesseract OCR and Kannada language data are installed. Details: " + str(e))
    if st.session_state.active_text:
        left,right=st.columns([1,1.2], gap="large")
        with left:
            st.markdown("#### Original / enhanced preview")
            preview=st.session_state.get("last_preview")
            if preview is not None: st.image(preview, use_container_width=True)
            else: st.info("For a text-based PDF, selectable text was extracted directly.")
            st.markdown("#### Quick quality signals")
            st.metric("Characters extracted", f"{len(st.session_state.active_text):,}")
            st.metric("Possible date strings", len(extract_dates(st.session_state.active_text)))
        with right:
            st.markdown("#### Review extracted text")
            edited=st.text_area("Editable OCR result", value=st.session_state.active_text, height=330, key="edited_ocr")
            st.session_state.active_text=edited
            b1,b2,b3=st.columns(3)
            b1.download_button("⬇️ Download TXT", data=edited, file_name="kannada_extracted_text.txt", mime="text/plain", use_container_width=True)
            b2.download_button("⬇️ Download JSON", data=json.dumps({"source":st.session_state.active_name,"text":edited,"reviewed_at":datetime.now().isoformat()}, ensure_ascii=False, indent=2), file_name="kannada_document.json", mime="application/json", use_container_width=True)
            if b3.button("＋ Save to Library", use_container_width=True):
                if not any(d["name"]==st.session_state.active_name for d in st.session_state.docs):
                    st.session_state.docs.append(make_doc_record(st.session_state.active_name, edited, st.session_state.get("last_kind","Document")))
                st.success("Saved to this session's library.")
        st.markdown("#### Understand this document")
        a,b,c=st.columns(3)
        with a:
            if st.button("🧠 Create quick summary", use_container_width=True):
                st.session_state.summary=simple_summary(edited)
        with b:
            if st.button("📅 Find dates", use_container_width=True):
                st.session_state.found_dates=extract_dates(edited)
        with c:
            if st.button("🔑 Find key terms", use_container_width=True):
                st.session_state.found_keywords=get_keywords(edited)
        if "summary" in st.session_state: st.info(st.session_state.summary)
        if "found_dates" in st.session_state: st.write("**Dates found:**", ", ".join(st.session_state.found_dates) if st.session_state.found_dates else "No obvious date patterns found.")
        if "found_keywords" in st.session_state: st.write("**Frequent terms:**", ", ".join([f"{w} ({n})" for w,n in st.session_state.found_keywords]) or "No terms found.")
        st.caption("OCR output is a draft, not a verified transcript. Check names, dates, numbers, legal or official details against the original scan.")
    else:
        st.markdown('<div class="card"><div class="icon">🪄</div><h3>Your document, made useful</h3><p>Upload a page to begin. You can edit the extracted result, download it, find dates, and save it to your temporary library.</p></div>', unsafe_allow_html=True)

elif page == "Ask Your Document":
    st.markdown('<div class="section-title">Ask Your Document</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Search and ask questions about the document you have extracted.</div>', unsafe_allow_html=True)
    text=st.session_state.active_text
    if not text:
        st.warning("First upload a document in Document Studio, then return here.")
    else:
        st.success(f"Active document: {st.session_state.active_name or 'Untitled document'}")
        query=st.text_input("Ask a question or search for a phrase", placeholder="e.g. What is this document about? / search for a date")
        if st.button("Search document", type="primary") and query:
            q=query.lower().strip()
            lines=[line.strip() for line in text.splitlines() if line.strip()]
            matches=[(i,line) for i,line in enumerate(lines) if q in line.lower()]
            if matches:
                st.markdown("### Matching passages")
                for i,line in matches[:10]:
                    st.markdown(f"- **Passage {i+1}:** {line}")
            else:
                terms=[t for t in re.findall(r'\w+',q) if len(t)>2]
                ranked=[]
                for i,line in enumerate(lines):
                    score=sum(1 for t in terms if t in line.lower())
                    if score: ranked.append((score,i,line))
                ranked.sort(reverse=True)
                if ranked:
                    st.markdown("### Closest passages")
                    for score,i,line in ranked[:8]:
                        st.markdown(f"- **Passage {i+1} · match score {score}:** {line}")
                else:
                    st.info("No matching passage found. Try a shorter keyword or another spelling.")
        st.markdown("### Quick actions")
        q1,q2,q3=st.columns(3)
        if q1.button("Summarize document"):
            st.info(simple_summary(text, 6))
        if q2.button("Show dates"):
            dates=extract_dates(text)
            st.write(dates if dates else "No obvious date patterns found.")
        if q3.button("Export searchable text"):
            st.download_button("Download TXT", text, file_name="document_search_text.txt", mime="text/plain")
        st.warning("This prototype uses keyword search, not a connected generative-AI model. AI answers with citations can be added by connecting a retrieval-augmented generation (RAG) service.")

elif page == "Kannada Learning":
    st.markdown('<div class="section-title">Kannada for Everyone</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Practical Kannada for everyday situations — start small, practise often.</div>', unsafe_allow_html=True)
    lessons={
      "Greetings":[("ನಮಸ್ಕಾರ","Namaskāra","Hello / Greetings"),("ಧನ್ಯವಾದಗಳು","Dhanyavādagaḷu","Thank you"),("ದಯವಿಟ್ಟು","Dayaviṭṭu","Please"),("ಕ್ಷಮಿಸಿ","Kṣamisi","Excuse me / Sorry")],
      "Travel":[("ಬಸ್ ನಿಲ್ದಾಣ ಎಲ್ಲಿದೆ?","Bus nilḍāṇa ellide?","Where is the bus station?"),("ಇದು ಎಷ್ಟು?","Idu eṣṭu?","How much is this?"),("ನನಗೆ ಸಹಾಯ ಬೇಕು","Nanage sahāya bēku","I need help")],
      "Food & shopping":[("ನೀರು ಬೇಕು","Nīru bēku","I need water"),("ಮೆನು ಕೊಡುತ್ತೀರಾ?","Menu koḍuttīrā?","Could you give me the menu?"),("ನಗದು ಅಥವಾ UPI?","Nagadu athavā UPI?","Cash or UPI?")],
      "Work & study":[("ನನಗೆ ಅರ್ಥವಾಯಿತು","Nanage arthavāyitu","I understood"),("ಮತ್ತೊಮ್ಮೆ ಹೇಳಿ","Mattomme hēḷi","Please say it again"),("ನಿಧಾನವಾಗಿ ಮಾತನಾಡಿ","Nidhānavāgi mātanāḍi","Please speak slowly")]
    }
    category=st.selectbox("Choose a situation", list(lessons.keys()))
    for kannada,roman,meaning in lessons[category]:
        st.markdown(f'<div class="card" style="min-height:90px;margin-bottom:10px"><h3 style="font-family:Noto Sans Kannada,sans-serif;font-size:1.35rem">{kannada}</h3><p><b>{roman}</b> · {meaning}</p></div>', unsafe_allow_html=True)
    st.markdown("### Quick practice")
    phrase=st.selectbox("Choose the meaning", [x[2] for x in lessons[category]])
    if st.button("Reveal Kannada phrase"):
        row=next(x for x in lessons[category] if x[2]==phrase)
        st.success(f"{row[0]}  ·  {row[1]}")
    st.caption("Romanization is approximate. Ask a Kannada speaker to review phrases before using them in formal or sensitive situations.")

elif page == "Voice & Pronunciation":
    st.markdown('<div class="section-title">Voice of Kannada</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">A voice-ready space for listening, speaking, and practising Kannada.</div>', unsafe_allow_html=True)
    st.info("This deployable starter includes text-to-speech where the browser supports it. Speech recognition varies by browser and device; cloud speech services can be integrated for stronger Kannada support.")
    voice_text=st.text_area("Kannada text to listen to", value="ನಮಸ್ಕಾರ! ಕನ್ನಡ ಕಲಿಯಲು ಸ್ವಾಗತ.", height=110)
    st.components.v1.html(f"""
    <div style="font-family:Arial,sans-serif;background:#fff;border:1px solid #EADFD6;border-radius:16px;padding:18px">
      <p style="color:#3B2A3A;font-weight:700;margin-top:0">Listen in your browser</p>
      <button id="speak" style="background:#3B2A3A;color:white;border:0;padding:11px 16px;border-radius:10px;cursor:pointer">▶ Play Kannada</button>
      <button id="stop" style="background:#DCE7D8;color:#3B2A3A;border:0;padding:11px 16px;border-radius:10px;cursor:pointer">■ Stop</button>
      <p id="status" style="color:#7A6A75;font-size:13px">Voice availability depends on your device/browser.</p>
      <script>
        const text = {json.dumps(voice_text, ensure_ascii=False)};
        document.getElementById('speak').onclick = () => {{
          if (!('speechSynthesis' in window)) {{ document.getElementById('status').innerText='Speech synthesis is not supported here.'; return; }}
          window.speechSynthesis.cancel();
          const u = new SpeechSynthesisUtterance(text);
          const voices = window.speechSynthesis.getVoices();
          const v = voices.find(x => x.lang && x.lang.toLowerCase().startsWith('kn')) || voices.find(x => x.lang && x.lang.toLowerCase().startsWith('hi'));
          if (v) {{ u.voice=v; u.lang=v.lang; }} else {{ u.lang='kn-IN'; }}
          u.rate=0.85; window.speechSynthesis.speak(u);
          document.getElementById('status').innerText = v ? 'Using available voice: '+v.name : 'Requested Kannada voice; browser may substitute if unavailable.';
        }};
        document.getElementById('stop').onclick = () => window.speechSynthesis.cancel();
      </script>
    </div>
    """, height=170)
    st.markdown("### Pronunciation practice")
    st.write("1. Listen to a phrase.  2. Repeat it aloud.  3. Compare with a trusted native-speaker recording.  4. Practise in a real-life sentence.")
    st.caption("The browser speech demo is best-effort and does not score pronunciation. A dedicated Kannada speech API is needed for dependable speech recognition and feedback.")

elif page == "Namma Heritage Map":
    st.markdown('<div class="section-title">Heritage Map</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">A community-led seed collection for regional Kannada words, expressions, and cultural context.</div>', unsafe_allow_html=True)
    st.warning("Entries below are starter examples for demonstration. Regional usage varies by community; verify entries with local speakers before publishing them as authoritative.")
    seed=[
      {"Region":"Mysuru","Expression":"ಏನ್ ಸಮಾಚಾರ?","Meaning":"What's the news? / How are things?","Context":"Informal greeting; usage varies"},
      {"Region":"North Karnataka","Expression":"ಏನ್ ಮಾಡ್ತಿದೀರೀ?","Meaning":"What are you doing?","Context":"Colloquial expression; local forms vary"},
      {"Region":"Coastal Karnataka","Expression":"ನಮಸ್ಕಾರ","Meaning":"Hello / Greetings","Context":"Common greeting; local languages and variants coexist"},
      {"Region":"Bengaluru","Expression":"ಸ್ವಲ್ಪ ನಿಧಾನವಾಗಿ ಹೇಳಿ","Meaning":"Please say it a little slowly","Context":"Useful everyday phrase"}
    ]
    if "heritage" not in st.session_state: st.session_state.heritage=seed
    with st.form("heritage_form"):
        c1,c2=st.columns(2)
        region=c1.text_input("Region / community")
        expression=c2.text_input("Kannada word or phrase")
        meaning=st.text_input("Meaning / translation")
        context=st.text_area("When is it used? Add cultural context or source.")
        submitted=st.form_submit_button("＋ Add community entry")
        if submitted:
            if region and expression and meaning:
                st.session_state.heritage.append({"Region":region,"Expression":expression,"Meaning":meaning,"Context":context or "Needs community review"})
                st.success("Added to this session. Review before public sharing.")
            else: st.error("Add a region, phrase, and meaning.")
    df=pd.DataFrame(st.session_state.heritage)
    filter_region=st.selectbox("Filter by region", ["All"]+sorted(df["Region"].unique().tolist()))
    if filter_region!="All": df=df[df["Region"]==filter_region]
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.download_button("Download entries as CSV", df.to_csv(index=False).encode("utf-8-sig"), "nudimane_heritage_entries.csv", "text/csv")
    st.caption("Production version: add consent, contributor attribution preferences, moderation, dialect labels, audio samples, and a source-verification workflow.")

elif page == "Karnataka Travel Planner":
    st.markdown('<div class="section-title">Karnataka Travel Planner</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">A flexible itinerary builder shaped by time, budget, and the kind of Karnataka you want to experience.</div>', unsafe_allow_html=True)
    with st.form("trip_form"):
        c1,c2,c3=st.columns(3)
        days=c1.slider("Trip length (days)",1,10,3)
        budget=c2.selectbox("Budget per person",["Budget","Comfort","Premium"])
        travel_type=c3.selectbox("Travel style",["Heritage & architecture","Nature & wildlife","Food & local culture","Spiritual & peaceful","Family-friendly","Mixed highlights"])
        start=c1.selectbox("Starting point",["Bengaluru","Mysuru","Mangaluru","Hubballi","Belagavi","Other"])
        pace=c2.selectbox("Pace",["Relaxed","Balanced","Packed"])
        transport=c3.selectbox("Transport",["Public transport","Car / taxi","Two-wheeler","Flexible"])
        submitted=st.form_submit_button("✨ Build my sample itinerary", type="primary")
    destinations={
      "Heritage & architecture":[("Bengaluru","City heritage, museums, gardens"),("Mysuru","Palaces, markets, cultural heritage"),("Hampi","Vijayanagara-era monuments"),("Badami","Rock-cut cave temples and architecture"),("Pattadakal","Chalukya-era temple complex")],
      "Nature & wildlife":[("Coorg","Coffee country and hill landscapes"),("Chikkamagaluru","Hill scenery and coffee estates"),("Jog Falls region","Waterfall viewpoints; seasonal conditions matter"),("Kabini region","Wildlife and river landscapes; permits may be needed"),("Gokarna","Coastal scenery and beaches")],
      "Food & local culture":[("Bengaluru","Regional food and markets"),("Mysuru","Mysore pak, markets, cultural sites"),("Dharwad","Local food traditions and music heritage"),("Udupi","Temple-town heritage and regional cuisine"),("Mangaluru","Coastal food and cultural mix")],
      "Spiritual & peaceful":[("Mysuru","Temples and cultural sites"),("Dharmasthala region","Pilgrimage and local heritage"),("Udupi","Krishna temple town"),("Sringeri","River valley and temple heritage"),("Belur & Halebidu","Hoysala temple architecture")],
      "Family-friendly":[("Mysuru","Palace, zoo, gardens"),("Bengaluru","Parks, museums, family attractions"),("Udupi","Coastal outings and cultural sites"),("Shivamogga region","Nature-oriented day trips"),("Hampi","Open-air heritage exploration")],
      "Mixed highlights":[("Bengaluru","Urban culture and gardens"),("Mysuru","Palace and cultural heritage"),("Coorg","Hill landscapes"),("Hampi","Historic ruins"),("Udupi","Coastal culture")]
    }
    if submitted:
        places=destinations[travel_type]
        if days==1: chosen=places[:1]
        else: chosen=[places[min(round(i*(len(places)-1)/max(days-1,1)),len(places)-1)] for i in range(days)]
        st.markdown("### Your draft itinerary")
        st.info(f"{days} day(s) · {budget} budget · {travel_type} · {pace.lower()} pace · transport: {transport}")
        for i,(place,desc) in enumerate(chosen,1):
            st.markdown(f'<div class="card" style="min-height:80px;margin-bottom:10px"><h3>Day {i} · {place}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
        st.caption(f"Starting point: {start}. This is a draft route, not a live route or booking plan. Check travel time, opening hours, weather, accessibility, permits, and local conditions before departure.")
        itinerary="\n".join([f"Day {i}: {p} — {d}" for i,(p,d) in enumerate(chosen,1)])
        st.download_button("Download itinerary", itinerary, "karnataka_itinerary.txt", "text/plain")
    st.markdown("### Planning features to add next")
    st.write("Map-based routing • estimated journey times • seasonal recommendations • accessible travel filters • verified opening hours • Kannada phrase pack for each destination.")

elif page == "My Library":
    st.markdown('<div class="section-title">My Library</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Documents saved during this session.</div>', unsafe_allow_html=True)
    if not st.session_state.docs:
        st.info("Your library is empty. Extract a document and choose **Save to Library**.")
    else:
        df=pd.DataFrame([{k:d[k] for k in ["name","kind","saved_at","chars"]} for d in st.session_state.docs])
        st.dataframe(df, use_container_width=True, hide_index=True)
        chosen=st.selectbox("Open a saved document", [d["name"] for d in st.session_state.docs])
        doc=next(d for d in st.session_state.docs if d["name"]==chosen)
        st.text_area("Saved text", doc["text"], height=250, key="library_view")
        st.download_button("Download selected text", doc["text"], file_name=re.sub(r'[^A-Za-z0-9._-]','_',chosen)+".txt", mime="text/plain")
        if st.button("Delete selected document"):
            st.session_state.docs=[d for d in st.session_state.docs if d["name"]!=chosen]
            st.success("Deleted from this session.")
    st.caption("This starter library is session-only. Add authentication and persistent storage for a production application. Avoid uploading sensitive documents to a public demo.")

elif page == "Impact & Quality":
    st.markdown('<div class="section-title">Impact & Quality Lab</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Make language technology measurable, transparent, and worthy of trust.</div>', unsafe_allow_html=True)
    docs=st.session_state.docs
    c1,c2,c3=st.columns(3)
    c1.metric("Documents saved this session",len(docs))
    c2.metric("Characters in active document",f"{len(st.session_state.active_text):,}")
    c3.metric("Active document", "Yes" if st.session_state.active_text else "No")
    st.markdown("### Research evaluation checklist")
    st.write("Use a manually transcribed ground-truth set to evaluate printed Kannada, handwriting, old scans, low-resolution photos, and mixed Kannada-English pages separately.")
    checklist=[
      "Character Error Rate (CER) against verified transcripts",
      "Word Error Rate (WER) against verified transcripts",
      "OCR confidence calibration and uncertain-word review rate",
      "Processing time per page and failure rate",
      "Search retrieval quality (Precision@k / Recall@k)",
      "Question-answer grounding: every answer linked to a source passage",
      "Human correction time saved, measured in a small usability study",
      "Accessibility checks: keyboard-only use, contrast, text resizing, screen reader"
    ]
    for item in checklist: st.checkbox(item, key="check_"+hashlib.md5(item.encode()).hexdigest()[:8])
    st.markdown("### Trust and provenance")
    st.write("For each production document, store source filename, upload timestamp, OCR engine/version, preprocessing settings, reviewer edits, export history, and optional source citation. Keep the original file separate from corrected text.")
    st.warning("This app is a research prototype. It does not guarantee OCR accuracy, professional translation, legal interpretation, or live travel information.")


st.markdown(f"""
<div class="footer"><div style="display:flex;gap:.8rem;align-items:center"><img src="{img_uri('logo_mark.png')}" width="46"/><div><b>Nudimane</b><small>ನುಡಿಮನೆ · Your home for Kannada. A research prototype, so please verify OCR, translations and travel details with trusted sources. Avoid uploading sensitive documents to a public demo.</small></div></div><div style="font-size:.85rem;color:#BFA9B7">Digitize · Learn · Speak · Explore</div></div>
""", unsafe_allow_html=True)
