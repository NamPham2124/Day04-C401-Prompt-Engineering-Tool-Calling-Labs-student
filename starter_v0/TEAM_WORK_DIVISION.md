# Phân Công Công Việc — Day 04 Lab v2

## Thông tin nhóm

| Thành viên | Vai trò |
|---|---|
| **Trần Đức Đăng Khôi** | Prompt Engineering + Tool Development |
| **Phạm Thành Nam** | Eval Engineering + UI/Report |

---

## Chi tiết phân công

### 🔵 Trần Đức Đăng Khôi — Prompt Engineering & Tool Development

| STT | Công việc | File liên quan | Trạng thái |
|-----|-----------|---------------|------------|
| 1 | Phân tích baseline v0 — đọc run JSON, xác định failures | `runs/v0_B_base.json` | ✅ Xong |
| 2 | Tối ưu `system_prompt.md` v1 — thêm rule clarify khi thiếu info + confirm trước send | `artifacts/system_prompt.md` | ✅ Xong |
| 3 | Tối ưu `system_prompt.md` v2 — thêm routing chi tiết (timeline vs social_search vs lookup) | `artifacts/system_prompt.md` | ✅ Xong |
| 4 | Tối ưu `system_prompt.md` v3 — multi-turn + parallel + arg conventions | `artifacts/system_prompt.md` | ✅ Xong |
| 5 | Tạo tool mới: `summarize` — TOOL.md + tool.py | `tools/summarize/TOOL.md`, `tools/summarize/tool.py` | ✅ Xong |
| 6 | Đăng ký tool mới vào registry | `tools/__init__.py` | ✅ Xong |
| 7 | Chạy eval v1, v2, v3 — phân tích kết quả | `runs/*.json` | ⏳ Cần API key |
| 8 | Live chat 3 turns — ghi transcript | `transcripts/*.json` | ⏳ Cần API key |

**Tóm tắt:** Khôi chịu trách nhiệm **vòng lặp tối ưu prompt** (giả thuyết → sửa → chạy → đo) và **phát triển tool mới**. Đây là phần core của lab — evidence-driven optimization.

---

### 🟢 Phạm Thành Nam — Eval Engineering & UI/Report

| STT | Công việc | File liên quan | Trạng thái |
|-----|-----------|---------------|------------|
| 1 | Tối ưu `tools.yaml` — viết lại description chi tiết cho từng tool | `artifacts/tools.yaml` | ✅ Xong |
| 2 | Viết 5 single-turn eval cases | `data/eval_group.json` (G01–G05) | ✅ Xong |
| 3 | Viết 5 multi-turn eval cases | `data/eval_group.json` (G06–G10) | ✅ Xong |
| 4 | Chạy eval group cases | `runs/*_group_*.json` | ⏳ Cần API key |
| 5 | Xây dựng Streamlit UI | `app.py` | ✅ Xong |
| 6 | Điền `version_log.csv` | `artifacts/version_log.csv` | ✅ Xong |
| 7 | Hoàn thiện REPORT.md — Phần A (trước 16:30) | `artifacts/REPORT.md` | ✅ Xong |
| 8 | Hoàn thiện REPORT.md — Phần B (chi tiết) | `artifacts/REPORT.md` | ✅ Xong |

**Tóm tắt:** Nam chịu trách nhiệm **eval cases** (thiết kế test coverage), **tool declarations** (tools.yaml), **UI**, và **documentation** (report + version log).

---

## Bảng tổng hợp

| Hạng mục | Khôi | Nam |
|----------|:----:|:---:|
| System prompt (v1→v3) | ✅ | |
| Tools.yaml (descriptions) | | ✅ |
| Tool mới: summarize | ✅ | |
| tools/__init__.py registry | ✅ | |
| 10 eval cases (eval_group.json) | | ✅ |
| Chạy eval base (v0→v3) | ✅ | |
| Chạy eval group | | ✅ |
| Live chat + transcript | ✅ | |
| Streamlit UI (app.py) | | ✅ |
| version_log.csv | | ✅ |
| REPORT.md Phần A | | ✅ |
| REPORT.md Phần B | ✅ (failure analysis) | ✅ (reflection) |

---

## Timeline

| Thời gian | Khôi | Nam |
|-----------|------|-----|
| 15:00–15:30 | Chạy baseline v0 + phân tích | Setup UI skeleton + viết tools.yaml |
| 15:30–16:00 | Sửa prompt v1 + tạo tool summarize | Viết 10 eval cases + chạy eval |
| 16:00–16:30 | Sửa prompt v2, v3 + chạy eval | Hoàn thiện REPORT Phần A + UI |
| 16:30–17:00 | Team showdown / demo | Team showdown / demo |
| 17:00–17:30 | Live chat + transcript + failure analysis | Hoàn thiện REPORT Phần B + version_log |

---

## Ghi chú

- Cả hai cần có API keys để chạy eval thật (OPENROUTER_API_KEY, TAVILY_API_KEY, etc.)
- Sau mỗi lần chạy eval, cập nhật `version_log.csv` với metric thật từ run JSON
- Cập nhật REPORT.md Phần B với dữ liệu thật sau khi chạy eval
