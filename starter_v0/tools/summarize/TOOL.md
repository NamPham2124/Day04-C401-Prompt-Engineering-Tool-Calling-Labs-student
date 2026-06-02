---
name: summarize
track: core
kind: local_formatter
provider: none
requires_env: []
inputs: [text, max_sentences]
outputs: [summary, word_count]
side_effect: false
---

# summarize

Nhận một đoạn text dài và trả về bản tóm tắt ngắn gọn bằng cách trích xuất các câu quan trọng nhất.

Khác với `format` (định dạng danh sách items thành markdown digest), `summarize` nhận raw text và tóm tắt nội dung.

## Khi nào dùng

- User yêu cầu "tóm tắt đoạn text này", "rút gọn nội dung"
- Sau khi đã fetch/đọc một bài viết dài, cần tóm tắt lại

## Inputs

| Arg | Type | Default | Mô tả |
|-----|------|---------|-------|
| text | string | "" | Đoạn text cần tóm tắt |
| max_sentences | integer | 5 | Số câu tối đa trong bản tóm tắt |

## Outputs

```json
{
  "tool": "summarize",
  "summary": "...",
  "word_count": 42,
  "original_length": 1500
}
```
