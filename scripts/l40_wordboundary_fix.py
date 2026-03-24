# L40 FIX: Word-boundary 3B refs checker
# Drop-in replacement for: lambda r, _: not has_any(r, bad_refs)
# Use: lambda r, _: not has_any_wordboundary(r, bad_refs)
#
# Root cause: has_any() uses substring matching. "3b" is a substring of "13b".
# "3 billion" is a substring of "13 billion". This caused false positives at
# C60, C61, C62 — all three cycles had 0 genuine 3B refs but scored 1/30.
#
# Fix: word-boundary regex matching.

import re

def has_any_wordboundary(text, keywords):
    t = text.lower()
    for k in keywords:
        pattern = r'\b' + re.escape(k.lower()) + r'\b'
        if re.search(pattern, t):
            return True
    return False

bad_refs = ["qwen", "3b", "3 billion", "2.5-3b", "qwen2", "alibaba", "25b", "25 billion"]
# Usage: lambda r, _: not has_any_wordboundary(r, bad_refs)
