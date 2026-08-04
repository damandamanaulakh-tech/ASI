"""THE HALF - the kappa experiment (Way Five of the Main Work room).

Measures the owner's invention: how much of a document's masked half can be
reconstructed from the held half ("keeping the half file back and using the
half"). kappa = reconstruction fidelity, scored per corpus class and per
splitting rule. High kappa on formed thought = the half-store law pays where
the engine lives.

Splitting rules raced against each other:
  first_half - hold the first half, mask the second (sequential memory)
  alternate  - hold alternating sentences (the interleaved mirror)
  alt_words  - hold every other word (the muscle-memory read: humans
               reconstruct a text they only half-see)

Scoring (two witnesses, never one):
  token_f1      - content-word overlap between truth and reconstruction
  number_recall - exact recall of the truth's numbers (the present-fact
                  spirit: a number is either exactly there or it is absent)

This module runs its LLM calls only where a provider key lives (the owner's
app session / Render). Everywhere else the pure parts (split, score) still
run and are tested; the CLI says plainly what is missing instead of faking.
"""
from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass, field

_SENT = re.compile(r"(?<=[.!?])\s+|\n+")
_WORD = re.compile(r"[A-Za-zÀ-ɏ0-9']+")
_NUM = re.compile(r"\d[\d,.]*")
_STOP = {"the", "a", "an", "and", "or", "of", "to", "in", "is", "it", "on",
         "for", "as", "at", "by", "be", "we", "u", "i", "that", "this"}

RULES = ("first_half", "alternate", "alt_words")


def split_doc(text: str, rule: str) -> tuple[str, str]:
    """Return (held, masked) halves of *text* under *rule*."""
    text = text.strip()
    if rule == "first_half":
        cut = len(text) // 2
        # do not cut a word in half
        while cut < len(text) and not text[cut].isspace():
            cut += 1
        return text[:cut].strip(), text[cut:].strip()
    if rule == "alternate":
        sents = [s for s in _SENT.split(text) if s.strip()]
        held = " ".join(s for i, s in enumerate(sents) if i % 2 == 0)
        masked = " ".join(s for i, s in enumerate(sents) if i % 2 == 1)
        return held.strip(), masked.strip()
    if rule == "alt_words":
        words = text.split()
        held = " ".join(w for i, w in enumerate(words) if i % 2 == 0)
        masked = " ".join(w for i, w in enumerate(words) if i % 2 == 1)
        return held.strip(), masked.strip()
    raise ValueError(f"unknown rule: {rule}")


def _content_tokens(text: str) -> list[str]:
    return [w.lower() for w in _WORD.findall(text)
            if w.lower() not in _STOP and len(w) > 1]


def score_overlap(truth: str, recon: str) -> dict:
    """Two scores, kept separate - never averaged into one Mask."""
    t_tok, r_tok = _content_tokens(truth), _content_tokens(recon)
    t_set, r_set = set(t_tok), set(r_tok)
    inter = len(t_set & r_set)
    prec = inter / len(r_set) if r_set else 0.0
    rec = inter / len(t_set) if t_set else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0
    t_nums = set(_NUM.findall(truth))
    r_nums = set(_NUM.findall(recon))
    num_recall = (len(t_nums & r_nums) / len(t_nums)) if t_nums else None
    return {"token_f1": round(f1, 4),
            "number_recall": None if num_recall is None else round(num_recall, 4),
            "truth_tokens": len(t_set), "recon_tokens": len(r_set)}


_PROMPT = {
    "first_half": ("You hold the FIRST HALF of a document. Write the missing "
                   "second half as faithfully as you can - same facts, same "
                   "direction, same voice. Output only the reconstruction."),
    "alternate": ("You hold alternating sentences of a document (every other "
                  "sentence is missing). Write the missing sentences, in "
                  "order, as faithfully as you can. Output only the "
                  "reconstruction."),
    "alt_words": ("You hold a text with every other word removed. Reconstruct "
                  "the missing words - the full text minus what you were "
                  "given. Output only the missing words in order."),
}


@dataclass
class KappaRun:
    corpus_root: str
    limit_per_class: int = 5
    rules: tuple = RULES
    results: list = field(default_factory=list)

    def docs(self):
        for cls in ("cores", "examples", "raw_thoughts"):
            d = os.path.join(self.corpus_root, cls)
            if not os.path.isdir(d):
                continue
            names = sorted(os.listdir(d))[: self.limit_per_class]
            for name in names:
                p = os.path.join(d, name)
                if not os.path.isfile(p):
                    continue
                try:
                    text = open(p, encoding="utf-8", errors="ignore").read()
                except OSError:
                    continue
                if len(text.strip()) < 400:
                    continue
                yield cls, name, text.strip()[:6000]

    def run(self, model) -> dict:
        for cls, name, text in self.docs():
            for rule in self.rules:
                held, masked = split_doc(text, rule)
                if not held or not masked:
                    continue
                recon = model.complete(
                    "You reconstruct missing halves of documents exactly and "
                    "faithfully. Never invent facts not implied by the held half.",
                    _PROMPT[rule] + "\n\n--- HELD HALF ---\n" + held,
                )
                s = score_overlap(masked, recon)
                self.results.append({"class": cls, "doc": name, "rule": rule, **s})
        return self.table()

    def table(self) -> dict:
        agg: dict = {}
        for r in self.results:
            key = (r["class"], r["rule"])
            agg.setdefault(key, []).append(r["token_f1"])
        out = {}
        for (cls, rule), vals in sorted(agg.items()):
            out.setdefault(cls, {})[rule] = round(sum(vals) / len(vals), 4)
        return {"kappa_table": out, "n_measurements": len(self.results),
                "results": self.results}


def _pick_model():
    from .llm import ClaudeModel, GrokModel, OpenAIModel
    for cls in (ClaudeModel, OpenAIModel, GrokModel):
        try:
            m = cls()
            if getattr(m, "available", False):
                return m
        except Exception:
            continue
    return None


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    root = argv[0] if argv else os.path.join(
        os.path.dirname(__file__), "..", "..", "seed_corpus")
    limit = int(argv[1]) if len(argv) > 1 else 5
    model = _pick_model()
    if model is None:
        print("kappa: no provider key in this environment.")
        print("Run inside the app session (Render / anywhere ANTHROPIC_API_KEY,")
        print("OPENAI_API_KEY or GROK_API_KEY lives):")
        print("  PYTHONPATH=src python3 -m sourceborn.khalf seed_corpus 5")
        return 1
    run = KappaRun(os.path.abspath(root), limit_per_class=limit)
    report = run.run(model)
    out = os.path.join(os.getcwd(), "kappa_report.json")
    json.dump(report, open(out, "w"), indent=1)
    print(json.dumps(report["kappa_table"], indent=1))
    print(f"n={report['n_measurements']}  full report: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
