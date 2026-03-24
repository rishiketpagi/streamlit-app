import streamlit as st
import os
from video_utils import extract_audio_from_video
from transcriber import transcribe_audio
from subtitle_generator import generate_srt

st.set_page_config(
    page_title="CaptionFlow",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0b1020 0%, #11182d 45%, #1d1240 100%);
        color: white;
    }

    .block-container {
        max-width: 1050px;
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    .topbar {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 22px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(12px);
    }

    .app-title {
        font-size: 2rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.2rem;
    }

    .app-subtitle {
        color: #cbd5e1;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    .glass-card {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 22px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(14px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.18);
    }

    .section-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.8rem;
    }

    .mini-text {
        color: #cbd5e1;
        font-size: 0.9rem;
    }

    .metric-box {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 0.9rem;
        text-align: center;
        margin-bottom: 0.7rem;
    }

    .metric-number {
        font-size: 1.15rem;
        font-weight: 800;
        color: white;
    }

    .metric-label {
        color: #cbd5e1;
        font-size: 0.85rem;
    }

    div[data-baseweb="select"] > div {
        background-color: rgba(255,255,255,0.08) !important;
        color: white !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
    }

    .stTextArea textarea {
        background-color: rgba(255,255,255,0.06) !important;
        color: white !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
    }

    .stButton > button, .stDownloadButton > button {
        width: 100%;
        border: none;
        border-radius: 14px;
        padding: 0.85rem 1rem;
        font-weight: 700;
        background: linear-gradient(90deg, #7c3aed, #2563eb);
        color: white;
        box-shadow: 0 8px 20px rgba(37,99,235,0.25);
    }

    .stButton > button:hover, .stDownloadButton > button:hover {
        transform: translateY(-1px);
    }

    section[data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.04);
        border: 1px dashed rgba(255,255,255,0.2);
        border-radius: 18px;
        padding: 0.8rem;
    }

    .footer-box {
        text-align: center;
        padding: 1rem;
        border-radius: 16px;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        color: #cbd5e1;
        margin-top: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

# -------------------- COMPACT HEADER --------------------
st.markdown("""
<div class="topbar">
    <div class="app-title">🎬 CaptionFlow</div>
    <div class="app-subtitle">
        Upload a video and generate subtitle files automatically using AI.
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------- MAIN TOOL FIRST --------------------
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Generate subtitles</div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader(
        "Upload your video",
        type=["mp4", "mov", "avi", "mkv"]
    )
    st.markdown(
        "<div class='mini-text'>Supported formats: MP4, MOV, AVI, MKV</div>",
        unsafe_allow_html=True
    )

with col2:
    model_size = st.selectbox(
        "Whisper model",
        ["tiny", "base", "small"],
        index=0
    )
    st.markdown(
        "<div class='mini-text'>Use <b>tiny</b> for faster cloud performance.</div>",
        unsafe_allow_html=True
    )

generate = st.button("🚀 Generate Subtitles", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# -------------------- PROCESS ONLY IF BOTH AVAILABLE --------------------
if uploaded_file is not None:
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("audio", exist_ok=True)
    os.makedirs("subtitles", exist_ok=True)

    video_path = os.path.join("uploads", uploaded_file.name)

    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())

    preview_col, details_col = st.columns([2, 1])

    with preview_col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Video preview</div>', unsafe_allow_html=True)
        st.video(video_path)
        st.markdown('</div>', unsafe_allow_html=True)

    with details_col:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">File details</div>', unsafe_allow_html=True)

        ext = uploaded_file.name.split(".")[-1].upper()
        size_mb = round(uploaded_file.size / (1024 * 1024), 2)

        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-number">{ext}</div>
            <div class="metric-label">Format</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-number">{size_mb} MB</div>
            <div class="metric-label">Size</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-number">{model_size.upper()}</div>
            <div class="metric-label">Model</div>
        </div>
        """, unsafe_allow_html=True)

        st.warning("Best performance: short videos under 1 minute.")
        st.markdown('</div>', unsafe_allow_html=True)

    if generate:
        try:
            audio_filename = os.path.splitext(uploaded_file.name)[0] + ".mp3"
            audio_path = os.path.join("audio", audio_filename)

            with st.spinner("Extracting audio from video..."):
                extract_audio_from_video(video_path, audio_path)

            with st.spinner("Transcribing speech with AI..."):
                segments = transcribe_audio(audio_path, model_size=model_size)

            with st.spinner("Creating subtitle file..."):
                srt_content = generate_srt(segments)

            srt_filename = os.path.splitext(uploaded_file.name)[0] + ".srt"

            st.success("✅ Subtitles generated successfully!")

            tab1, tab2 = st.tabs(["Subtitle File", "Transcript Segments"])

            with tab1:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Generated SRT</div>', unsafe_allow_html=True)
                st.text_area(
                    "Generated subtitle text",
                    srt_content,
                    height=340,
                    label_visibility="collapsed"
                )
                st.download_button(
                    "⬇ Download Subtitle File",
                    data=srt_content,
                    file_name=srt_filename,
                    mime="text/plain",
                    use_container_width=True
                )
                st.markdown('</div>', unsafe_allow_html=True)

            with tab2:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">Transcript segments</div>', unsafe_allow_html=True)

                for i, seg in enumerate(segments[:25], start=1):
                    st.markdown(f"""
                    <div style="
                        background: rgba(255,255,255,0.05);
                        border: 1px solid rgba(255,255,255,0.08);
                        border-radius: 14px;
                        padding: 0.9rem;
                        margin-bottom: 0.7rem;
                    ">
                        <div style="font-weight:700; color:#93c5fd; margin-bottom:0.3rem;">
                            Segment {i} • {seg['start']:.2f}s - {seg['end']:.2f}s
                        </div>
                        <div style="color:#e5e7eb;">
                            {seg['text']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error: {e}")

elif generate:
    st.error("Please upload a video first.")

# -------------------- SMALL FOOTER ONLY --------------------
st.markdown("""
<div class="footer-box">
    Built with Streamlit, MoviePy, and Faster-Whisper • Designed by Rishiket Pagi
</div>
""", unsafe_allow_html=True)