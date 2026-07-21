"""
Shared UI components for the MultiVision AI Assistant.
All reusable styled elements live here — zero duplicated UI code across modules.
"""

import streamlit as st
import time


# =============================================
# Color Palette
# =============================================

ACCENT_COLORS = {
    "emotion": "#eab308",     # Yellow
    "animal": "#22c55e",      # Green
    "car": "#3b82f6",         # Blue
    "voice": "#a855f7",       # Purple
    "sign": "#f97316",        # Orange
    "drowsiness": "#06b6d4",  # Cyan
}


# =============================================
# Global CSS
# =============================================

def inject_global_css():
    """Inject all custom CSS once at the top of the app."""
    st.markdown("""
    <style>
        /* ---- Typography ---- */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* ---- Hide default Streamlit elements ---- */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}

        /* ---- Card base ---- */
        .ui-card {
            background: #1a1c2e;
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }

        .ui-card:hover {
            border-color: rgba(255, 255, 255, 0.12);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }

        /* ---- Module card (homepage) ---- */
        .module-card {
            background: #1a1c2e;
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 12px;
            padding: 1.25rem;
            text-align: center;
            transition: border-color 0.2s ease, transform 0.2s ease;
        }

        .module-card:hover {
            border-color: rgba(255, 255, 255, 0.15);
            transform: translateY(-2px);
        }

        .module-card .card-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }

        .module-card .card-title {
            font-size: 0.95rem;
            font-weight: 600;
            color: #e2e8f0;
            margin-bottom: 0.25rem;
        }

        .module-card .card-desc {
            font-size: 0.8rem;
            color: #94a3b8;
            line-height: 1.4;
        }

        /* ---- Hero section ---- */
        .hero-section {
            text-align: center;
            padding: 2rem 0 1.5rem 0;
        }

        .hero-section .hero-icon {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }

        .hero-section .hero-title {
            font-size: 1.75rem;
            font-weight: 700;
            color: #f1f5f9;
            margin-bottom: 0.25rem;
        }

        .hero-section .hero-desc {
            font-size: 1rem;
            color: #94a3b8;
            font-weight: 300;
        }

        /* ---- Result card ---- */
        .result-card {
            background: #1a1c2e;
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 12px;
            padding: 1.25rem;
            text-align: center;
        }

        .result-card .result-label {
            font-size: 0.8rem;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.25rem;
        }

        .result-card .result-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #f1f5f9;
            margin-bottom: 0.5rem;
        }

        /* ---- Confidence bar ---- */
        .confidence-bar-container {
            background: rgba(255, 255, 255, 0.06);
            border-radius: 6px;
            height: 8px;
            overflow: hidden;
            margin-top: 0.5rem;
        }

        .confidence-bar-fill {
            height: 100%;
            border-radius: 6px;
            transition: width 0.5s ease;
        }

        /* ---- Badge ---- */
        .confidence-badge {
            display: inline-block;
            font-size: 0.7rem;
            font-weight: 600;
            padding: 0.15rem 0.5rem;
            border-radius: 999px;
            margin-top: 0.4rem;
        }

        /* ---- Warning card ---- */
        .warning-card {
            background: rgba(234, 179, 8, 0.08);
            border: 1px solid rgba(234, 179, 8, 0.2);
            border-radius: 12px;
            padding: 1.25rem;
            text-align: center;
        }

        .warning-card .warning-icon {
            font-size: 1.75rem;
            margin-bottom: 0.5rem;
        }

        .warning-card .warning-title {
            font-size: 1rem;
            font-weight: 600;
            color: #eab308;
            margin-bottom: 0.25rem;
        }

        .warning-card .warning-text {
            font-size: 0.85rem;
            color: #94a3b8;
        }

        /* ---- Empty state ---- */
        .empty-state {
            text-align: center;
            padding: 3rem 1rem;
            color: #64748b;
        }

        .empty-state .empty-icon {
            font-size: 3rem;
            margin-bottom: 0.75rem;
        }

        .empty-state .empty-text {
            font-size: 1rem;
            color: #94a3b8;
            margin-bottom: 0.5rem;
        }

        .empty-state .empty-formats {
            font-size: 0.8rem;
            color: #64748b;
        }

        /* ---- Tech badge ---- */
        .tech-badge {
            display: inline-block;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 8px;
            padding: 0.4rem 0.75rem;
            margin: 0.2rem;
            font-size: 0.8rem;
            color: #94a3b8;
            font-weight: 500;
        }

        /* ---- Model info ---- */
        .model-info-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
        }

        .model-info-card .info-label {
            font-size: 0.7rem;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .model-info-card .info-value {
            font-size: 0.95rem;
            font-weight: 600;
            color: #e2e8f0;
        }

        /* ---- Footer ---- */
        .app-footer {
            text-align: center;
            padding: 2rem 0 1rem 0;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            margin-top: 3rem;
        }

        .app-footer .footer-text {
            font-size: 0.75rem;
            color: #475569;
        }

        /* ---- Inference time ---- */
        .inference-badge {
            display: inline-block;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 8px;
            padding: 0.3rem 0.6rem;
            font-size: 0.75rem;
            color: #94a3b8;
        }

        /* ---- Streamlit overrides ---- */
        .stButton > button {
            border-radius: 10px;
            font-weight: 500;
            transition: all 0.2s ease;
        }

        div[data-testid="stFileUploader"] {
            border-radius: 12px;
        }

        div[data-testid="stExpander"] {
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 12px;
        }
    </style>
    """, unsafe_allow_html=True)


# =============================================
# Hero Section
# =============================================

def render_hero(icon, title, description):
    """Render a centered hero header for a module page."""
    st.markdown(f"""
    <div class="hero-section">
        <div class="hero-icon">{icon}</div>
        <div class="hero-title">{title}</div>
        <div class="hero-desc">{description}</div>
    </div>
    """, unsafe_allow_html=True)


# =============================================
# Empty State
# =============================================

def render_empty_state(icon, message, formats):
    """Render a friendly empty state when no file is uploaded."""
    st.markdown(f"""
    <div class="empty-state">
        <div class="empty-icon">{icon}</div>
        <div class="empty-text">{message}</div>
        <div class="empty-formats">Supported: {formats}</div>
    </div>
    """, unsafe_allow_html=True)


# =============================================
# Result Card
# =============================================

def render_result_card(label, value, confidence=None, accent_color="#a78bfa"):
    """Render a styled result card with optional confidence bar."""
    badge_html = ""
    bar_html = ""

    if confidence is not None:
        # Determine badge
        if confidence >= 80:
            badge_text, badge_bg, badge_fg = "High", "rgba(34,197,94,0.15)", "#22c55e"
        elif confidence >= 50:
            badge_text, badge_bg, badge_fg = "Medium", "rgba(234,179,8,0.15)", "#eab308"
        else:
            badge_text, badge_bg, badge_fg = "Low", "rgba(239,68,68,0.15)", "#ef4444"

        badge_html = f"""
        <div style="font-size:0.85rem; color:#94a3b8; margin-bottom:0.25rem;">
            {confidence:.1f}%
        </div>
        <span class="confidence-badge" style="background:{badge_bg}; color:{badge_fg};">
            {badge_text}
        </span>
        """
        bar_html = f"""
        <div class="confidence-bar-container">
            <div class="confidence-bar-fill" style="width:{min(confidence, 100)}%; background:{accent_color};"></div>
        </div>
        """

    st.markdown(f"""
    <div class="result-card">
        <div class="result-label">{label}</div>
        <div class="result-value">{value}</div>
        {badge_html}
        {bar_html}
    </div>
    """, unsafe_allow_html=True)


# =============================================
# Warning Card
# =============================================

def render_warning_card(title, message):
    """Render a styled warning card."""
    st.markdown(f"""
    <div class="warning-card">
        <div class="warning-icon">⚠️</div>
        <div class="warning-title">{title}</div>
        <div class="warning-text">{message}</div>
    </div>
    """, unsafe_allow_html=True)


# =============================================
# Model Info Section
# =============================================

def render_model_info(models):
    """
    Render a model information section.
    models: list of dicts with keys: label, value
    Example: [{"label": "Model", "value": "YOLOv8n"}, {"label": "Dataset", "value": "COCO"}]
    """
    cols = st.columns(len(models))
    for col, info in zip(cols, models):
        with col:
            st.markdown(f"""
            <div class="model-info-card">
                <div class="info-label">{info["label"]}</div>
                <div class="info-value">{info["value"]}</div>
            </div>
            """, unsafe_allow_html=True)


# =============================================
# Inference Time
# =============================================

def render_inference_time(seconds):
    """Render an inference time badge."""
    st.markdown(f"""
    <div style="text-align: center; margin-top: 0.75rem;">
        <span class="inference-badge">⚡ Inference: {seconds:.2f}s</span>
    </div>
    """, unsafe_allow_html=True)


# =============================================
# Tech Stack Badges
# =============================================

def render_tech_stack(techs):
    """Render tech stack badges."""
    badges = " ".join(f'<span class="tech-badge">{t}</span>' for t in techs)
    st.markdown(f"""
    <div style="text-align: center; margin-top: 1rem;">
        {badges}
    </div>
    """, unsafe_allow_html=True)


# =============================================
# Footer
# =============================================

def render_footer():
    """Render the app footer."""
    st.markdown("""
    <div class="app-footer">
        <div class="footer-text">
            Built with YOLOv8 · TensorFlow · XGBoost · Streamlit · OpenCV · Librosa
        </div>
    </div>
    """, unsafe_allow_html=True)


# =============================================
# Module Card (Homepage)
# =============================================

def render_module_card(icon, title, description):
    """Render a module card for the homepage. Returns nothing — just renders HTML."""
    st.markdown(f"""
    <div class="module-card">
        <div class="card-icon">{icon}</div>
        <div class="card-title">{title}</div>
        <div class="card-desc">{description}</div>
    </div>
    """, unsafe_allow_html=True)
