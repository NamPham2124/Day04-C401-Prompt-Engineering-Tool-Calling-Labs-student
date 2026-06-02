from __future__ import annotations

import re
from typing import Any


def _split_sentences(text: str) -> list[str]:
    """Split text into sentences using basic punctuation rules."""
    # Split on sentence-ending punctuation followed by space or end of string
    raw = re.split(r'(?<=[.!?。])\s+', text.strip())
    return [s.strip() for s in raw if s.strip()]


def _score_sentence(sentence: str, word_freq: dict[str, int]) -> float:
    """Score a sentence by sum of word frequencies (extractive importance)."""
    words = re.findall(r'\w+', sentence.lower())
    if not words:
        return 0.0
    return sum(word_freq.get(w, 0) for w in words) / len(words)


def summarize_text(text: str = "", max_sentences: int = 5) -> dict[str, Any]:
    """Extractive summarization: pick the most important sentences."""
    if not text or not text.strip():
        return {
            "tool": "summarize",
            "summary": "",
            "word_count": 0,
            "original_length": 0,
        }

    original_length = len(text)
    max_sentences = max(1, min(int(max_sentences or 5), 20))

    sentences = _split_sentences(text)
    if not sentences:
        return {
            "tool": "summarize",
            "summary": text[:500],
            "word_count": len(text.split()),
            "original_length": original_length,
        }

    # Build word frequency map (simple TF)
    stopwords = {
        "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
        "has", "he", "in", "is", "it", "its", "of", "on", "or", "that",
        "the", "to", "was", "were", "will", "with",
        "là", "và", "của", "các", "có", "được", "cho", "với", "từ",
        "trong", "này", "đã", "để", "một", "không", "những", "về",
        "theo", "khi", "như", "bị", "ra", "lên", "đến", "sẽ",
    }
    all_words = re.findall(r'\w+', text.lower())
    word_freq: dict[str, int] = {}
    for w in all_words:
        if w not in stopwords and len(w) > 1:
            word_freq[w] = word_freq.get(w, 0) + 1

    # Score and rank sentences
    scored = [(i, s, _score_sentence(s, word_freq)) for i, s in enumerate(sentences)]
    scored.sort(key=lambda x: x[2], reverse=True)

    # Pick top sentences, then re-order by original position
    top = scored[:max_sentences]
    top.sort(key=lambda x: x[0])

    summary = " ".join(s for _, s, _ in top)
    return {
        "tool": "summarize",
        "summary": summary,
        "word_count": len(summary.split()),
        "original_length": original_length,
        "sentence_count": len(top),
    }
