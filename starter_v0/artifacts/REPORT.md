# Day 04 Lab v2 Report — Research Agent

> File này gồm 2 phần, deadline khác nhau:
> - **PHẦN A — Giới thiệu agent**: ngắn gọn 1 trang để team khác hiểu nhanh agent có tool gì, làm được gì, thử bằng câu hỏi nào. **Xong trước 16:30** để làm tài liệu phụ trợ khi demo. Có thể làm thành poster HTML/SVG (`artifacts/poster.html` / `poster.svg`) để show cho team cùng zone.
> - **PHẦN B — Chi tiết / Bằng chứng**: bảng đầy đủ (v0–v3, failure, eval, chat) dựa trên log thật. **Có thể hoàn thiện sau buổi debate để nộp bài.**

## Team

- Team: Khôi & Nam Research Agent
- Members: Trần Đức Đăng Khôi, Phạm Thành Nam
- Provider/model: OpenRouter / openai/gpt-4o-mini

---

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

Research agent đa năng: tìm tin tức trên web, theo dõi tweet/bài đăng trên Twitter/X theo tài khoản hoặc chủ đề, đọc và tóm tắt nội dung URL, tìm và đọc paper arXiv, tra cứu policy nội bộ công ty, tổng hợp thành digest/bản tin, tóm tắt text dài, và gửi lên Telegram (có xác nhận). Agent biết hỏi lại khi thiếu thông tin, từ chối khi ngoài phạm vi, và xử lý hội thoại multi-turn.

**Link dùng thử (deploy):**

> URL: _(chạy local bằng Streamlit: `streamlit run app.py`)_

## A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | Hỏi lại user khi thiếu thông tin (handle, URL) hoặc cần xác nhận trước hành động ghi | không |
| timeline | Lấy tweet mới nhất CỦA một tài khoản Twitter cụ thể (cần handle) | không |
| social_search | Tìm tweet VỀ một chủ đề/từ khóa trên Twitter (Latest hoặc Top) | không |
| lookup | Tìm kiếm tin tức hoặc thông tin chung trên web (topic + timeframe) | không |
| fetch | Đọc nội dung từ một URL cụ thể | không |
| format | Định dạng danh sách items thành markdown digest/bản tin | không |
| summarize | Tóm tắt đoạn text dài bằng extractive summarization | **CÓ — nhóm thêm** |
| send | Gửi text lên Telegram channel (cần xác nhận trước) | không |
| policy | Tìm trong tài liệu policy nội bộ công ty | không |
| papers | Tìm paper khoa học trên arXiv | không |
| paper_text | Tải và đọc nội dung PDF paper arXiv | không |

## A3. Câu hỏi mẫu để thử

1. "Tweet mới nhất của Sam Altman là gì?"
2. "Mọi người đang bàn gì về GPT-5 trên Twitter?"
3. "Tin tức AI hôm nay có gì nổi bật?"
4. "Tóm tắt bài này giúp mình: https://openai.com/blog/gpt-5"
5. "Tìm paper arXiv về retrieval augmented generation"

---

# PHẦN B — Chi tiết / Bằng chứng

## B1. Version Evidence

Fill from `artifacts/version_log.csv` and `runs/*.json`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | System prompt cố tình sai (đoán bừa, tự gửi) → fail phần lớn case | — | 0.35 | runs/v0_B_base.json |
| v1 | system_prompt.md | Thêm rule hỏi lại khi thiếu handle/URL + xác nhận trước gửi → fix R10, R11, R12 | 0.35 | 0.60 | runs/v1_B_base.json |
| v2 | system_prompt.md + tools.yaml | Phân biệt rõ timeline vs social_search vs lookup + out_of_scope → fix R01-R09, R13-R14 | 0.60 | 0.80 | runs/v2_B_base.json |
| v3 | system_prompt.md + tools.yaml + tool mới | Multi-turn carry + parallel calls + arg conventions + summarize tool → fix M01-M06 | 0.80 | 0.95 | runs/v3_B_base.json |

## B2. Failure Analysis

Use actual failures from `results[*].result.failures`.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R10_missing_handle | missing_info | v0: timeline(sama) | Agent đoán bừa handle thay vì hỏi | v1: Thêm rule "thiếu handle → clarify" |
| R11_missing_url | missing_info | v0: fetch(guessed_url) | Agent tự bịa URL thay vì hỏi | v1: Thêm rule "thiếu URL → clarify" |
| R12_confirm_before_send | wrong_boundary | v0: send(text, confirmed=true) | Agent tự gửi không hỏi | v1: Thêm rule "ghi → clarify yes_no trước" |
| R08_out_of_scope | out_of_scope | v0: lookup("tích phân x^2") | Agent gọi tool cho câu toán | v2: Thêm rule "ngoài scope → từ chối" |
| R09_no_tool_capability | unnecessary_tool | v0: lookup("bạn là gì") | Agent gọi tool cho câu hỏi meta | v2: Thêm rule "meta → trả lời thẳng" |
| R01_user_tweets_routing | wrong_tool | v0: social_search("Sam Altman") | Nhầm social_search vs timeline | v2: Phân biệt rõ "CỦA ai" vs "VỀ gì" |
| M01_clarify_then_fill | missing_info | v0: timeline(sama, 5) | Không carry context multi-turn | v3: Thêm multi-turn rules |
| R13_parallel | wrong_tool | v0: lookup only | Chỉ gọi 1 tool thay vì 2 | v3: Thêm parallel calls rule |

## B3. Team Eval Cases

List the 10 cases added to `data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_arxiv_paper_search | Paper arXiv routing | papers | — |
| G02_company_tool_usage_policy | Policy nội bộ tool_usage | policy(tool_usage) | — |
| G03_bill_gates_timeline | Handle mapping Bill Gates | timeline(BillGates) | — |
| G04_monthly_news_timeframe | Timeframe "tháng này" → month | lookup(news, month) | — |
| G05_out_of_scope_translation | Dịch thuật ngoài scope | no_tool (refuse) | — |
| G06_missing_topic_then_search | Multi-turn: thiếu topic → bổ sung | social_search(Gemini 2.0) | — |
| G07_switch_to_arxiv | Multi-turn: chuyển web → arXiv | papers | — |
| G08_correct_url | Multi-turn: sửa URL | fetch(url mới) | — |
| G09_change_search_type | Multi-turn: Top → Latest | social_search(Latest) | — |
| G10_confirm_send_multiturn | Multi-turn: xác nhận gửi | send(confirmed=true) | — |

## B4. Live Chat Evidence

Use `transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | "Tweet mới nhất của Elon Musk" | timeline(elonmusk) | v3 — map tên → handle | ✅ Đúng tool + args |
| 2 | "Tóm tắt 5 tweet mới nhất giúm mình" | clarify("Bạn muốn xem tweet của ai?") | v3 — hỏi khi thiếu info | ✅ Hỏi đúng |
| 3 | "Gửi bản tin lên Telegram" | clarify(yes_no) | v3 — confirm trước gửi | ✅ Không tự gửi |

## B5. Bonus Evidence

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| send (Telegram) | Cần API key | Confirm trước gửi bằng clarify yes_no | Agent không tự gửi khi chưa xác nhận |
| arXiv/company policy | tools/papers, tools/policy | Tìm paper + đọc PDF text; tra cứu policy nội bộ | Rate limit arXiv 3s; policy dùng local files |
| UI | app.py (Streamlit) | Chat interface, hiển thị tool calls, lịch sử hội thoại | — |
| Tool mới: summarize | tools/summarize/ | Extractive summarization local, không cần API | — |

## B6. Reflection

- **Which fixes belonged in `system_prompt.md`?**
  - Routing rules (khi nào dùng clarify, khi nào từ chối), multi-turn context rules, parallel tool call instructions, out-of-scope handling, confirmation before write actions. Đây là những instruction về HÀNH VI agent.

- **Which fixes belonged in `tools.yaml`?**
  - Tool descriptions chi tiết (khi nào dùng, khi nào KHÔNG dùng), arg descriptions rõ ràng (ví dụ timeframe mapping, search_type meaning). Đây là metadata giúp model hiểu CHỨC NĂNG mỗi tool.

- **Which failure needed manual review instead of automatic grading?**
  - R08/R09 (out_of_scope, unnecessary_tool): eval chỉ check "no tool call" nhưng không đánh giá chất lượng câu trả lời từ chối. Agent có thể không gọi tool nhưng trả lời nhảm.
  - M01-M06 (multi-turn): eval ghép 3 turn thành 1 message, khác với real multi-turn. Agent thật sẽ có conversation history thay vì 1 prompt dài.

- **What would you improve next?**
  - Thêm semantic matching thay vì exact keyword matching cho tool routing
  - Thêm eval case cho edge cases: URL arXiv nhưng muốn dùng fetch thay vì paper_text, request vừa ngoài scope vừa trong scope
  - Cải thiện summarize tool bằng embedding-based sentence scoring thay vì TF
  - Thêm tool mới: `translate` (dịch nội dung), `compare` (so sánh 2 nguồn)
