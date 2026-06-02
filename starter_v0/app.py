"""
Streamlit UI for Day 04 Research Agent.
Run: streamlit run app.py
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st

from env_loader import load_lab_env
from providers import make_provider
from tools import TOOL_FUNCTIONS, load_tool_declarations, to_openai_tools
from versioning import build_artifact_version

ROOT = Path(__file__).parent
ARTIFACTS_DIR = ROOT / "artifacts"
load_lab_env(ROOT)


def _load_artifacts(version: str = "v3"):
    sp_path = ARTIFACTS_DIR / "system_prompt.md"
    t_path = ARTIFACTS_DIR / "tools.yaml"
    sp = sp_path.read_text(encoding="utf-8")
    decls = load_tool_declarations(t_path)
    oi_tools = to_openai_tools(decls)
    av = build_artifact_version(version, sp_path, t_path)
    return sp, oi_tools, av


def _exec_tool(name: str, args: dict[str, Any]) -> dict[str, Any]:
    func = TOOL_FUNCTIONS.get(name)
    if not func:
        return {"error": "unknown_tool"}
    try:
        return func(**args)
    except Exception as exc:
        return {"error": str(exc)}


st.set_page_config(page_title="Research Agent", page_icon="🔬", layout="wide")

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
.stApp { font-family: 'Inter', sans-serif; }
.hdr { background: linear-gradient(135deg,#667eea,#764ba2); padding:1.5rem 2rem;
  border-radius:16px; color:white; margin-bottom:1.5rem; }
.hdr h1 { margin:0; font-size:1.8rem; }
.hdr p { margin:.3rem 0 0; opacity:.9; font-size:.95rem; }
.tcb { background:#1a1a2e; border:1px solid #0f3460; border-radius:12px;
  padding:1rem; margin:.5rem 0; color:#e0e0e0; font-size:.85rem; }
.tn { color:#00d2ff; font-weight:600; }
.ta { color:#a8e6cf; margin-top:.3rem; }
.tr { color:#ffd93d; margin-top:.5rem; border-top:1px solid #0f3460; padding-top:.5rem; }
</style>""", unsafe_allow_html=True)

st.markdown("""<div class="hdr"><h1>🔬 Research Agent</h1>
<p>Tìm tin, Twitter, URL, arXiv, policy — tất cả trong một</p></div>""",
unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Cấu hình")
    prov = st.selectbox("Provider", ["openrouter","openai","anthropic","gemini"])
    ver = st.selectbox("Version", ["v0","v1","v2","v3"], index=3)
    mdl = st.text_input("Model (trống=mặc định)", "")
    st.markdown("---")
    st.markdown("### 🛠️ Tools")
    for t in ["clarify","timeline","social_search","lookup","fetch",
              "format","summarize","send","policy","papers","paper_text"]:
        st.markdown(f"- `{t}`")
    st.markdown("---")
    if st.button("🗑️ Xóa lịch sử", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.markdown("**Nhóm:** Khôi & Nam")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        for tc in msg.get("tool_calls", []):
            a = json.dumps(tc["args"], ensure_ascii=False)
            r = json.dumps(tc.get("result",{}), ensure_ascii=False)[:400]
            st.markdown(f'<div class="tcb"><div class="tn">🔧 {tc["name"]}</div>'
                        f'<div class="ta">{a}</div><div class="tr">{r}</div></div>',
                        unsafe_allow_html=True)

if user_input := st.chat_input("Hỏi gì đó..."):
    st.session_state.messages.append({"role":"user","content":user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        with st.spinner("Đang xử lý..."):
            try:
                sp, oi_tools, av = _load_artifacts(ver)
                provider = make_provider(prov)
                msgs = [{"role":"system","content":sp}]
                for m in st.session_state.messages[-10:]:
                    msgs.append({"role":m["role"],"content":m["content"]})
                resp = provider.complete(msgs, oi_tools, model=mdl or None, temperature=0.0)
                tcd = []
                for c in (resp.tool_calls or []):
                    res = _exec_tool(c.name, c.args)
                    tcd.append({"name":c.name,"args":c.args,"result":res})
                    a = json.dumps(c.args, ensure_ascii=False)
                    r = json.dumps(res, ensure_ascii=False)[:400]
                    st.markdown(f'<div class="tcb"><div class="tn">🔧 {c.name}</div>'
                                f'<div class="ta">{a}</div><div class="tr">{r}</div></div>',
                                unsafe_allow_html=True)
                txt = resp.text or "Đã thực hiện tool call."
                st.markdown(txt)
                st.session_state.messages.append({"role":"assistant","content":txt,"tool_calls":tcd})
            except Exception as exc:
                err = f"❌ {type(exc).__name__}: {exc}"
                st.error(err)
                st.session_state.messages.append({"role":"assistant","content":err})
