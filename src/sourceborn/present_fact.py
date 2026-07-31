"""Present-fact hard rule — moving numbers are never answered from memory.

Born from a real failure the owner caught on the live app: asked for TCS's
current share price, the system answered 2431 while the market said 2362.
The number came from model memory — a stale rendering of the world served as
the world. The evidence tag said "no live source", but the USER READS THE
NUMBER, not the tag.

So: for PRESENT-FACT asks — quantities that move (market prices, rates,
scores, weather, "current/today/now/latest" anything) — the rule is hard:

    no live witness  ->  NO NUMBER LEAVES THE ENGINE. The answer itself is
                         the refusal, stating exactly what is missing.
    one live witness ->  the number may be shown, timestamped to its source,
                         capped at Medium (a price is one witness away from
                         wrong), with a verify-before-acting line.

This is Filter 5 (Fact) upgraded from annotation to a block, for the class
of facts where staleness is indistinguishable from falsehood.
"""

from __future__ import annotations

# quantities that are only ever true "as of now"
_MARKET = ("price", "share price", "stock price", "quote", "ltp", "nav",
           "market cap", "nifty", "sensex", "dow", "nasdaq", "crypto",
           "bitcoin", "exchange rate", "rate of", "usd", "inr", "eur",
           "gold rate", "silver rate")
_TIME = ("current", "today", "todays", "today's", "right now", "now",
         "latest", "live", "at the moment", "as of")
_OTHER_MOVING = ("score", "weather", "temperature", "traffic", "stock",
                 "trading at", "trading price")


def is_present_fact(text: str) -> bool:
    """Does this ask want a quantity that moves with the clock?

    Market quantities qualify on their own (a price is ALWAYS a present
    fact). Other moving quantities qualify when a time marker is present.
    """
    low = f" {text.lower()} "
    if any(m in low for m in _MARKET):
        return True
    has_time = any(t in low for t in _TIME)
    return has_time and any(o in low for o in _OTHER_MOVING)


def refusal(ask: str) -> str:
    """The answer that leaves the engine when it has no eyes on a moving fact.
    Deterministic — model prose is NOT used, because a model's memory of a
    price is exactly the thing being refused."""
    return (
        "Direct answer: I cannot tell you this number, because it moves and I "
        "have no live source connected right now — and a remembered number "
        "shown as current is indistinguishable from a wrong one.\n"
        "What I refuse to do: state a price/rate/score from model memory. "
        "That is how a stale figure gets dressed as today's fact.\n"
        "What would give me eyes: a live-data key set on the server "
        "(TAVILY_API_KEY or a market-data feed), or paste the current figure "
        "from your broker/exchange and I will work with it as YOUR witness, "
        "tagged to you.\n"
        f"Falsifier: a live quote for “{ask[:80]}” from your "
        "screen — which is exactly the witness this answer is missing."
    )


def verify_note(source_hint: str = "one live source") -> str:
    return (f"\n\nCaution: this figure rests on {source_hint} — a single "
            f"witness. Prices move and feeds lag; verify on your "
            f"broker/exchange before acting. Confidence capped at Medium.")
