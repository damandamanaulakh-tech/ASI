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

import re

# Quotes that are only ever true "as of now". These are matched on WORD
# boundaries, not as substrings: "price" as a bare substring also fires on
# "price elasticity" and "rate of" on "rate of change", and refusing to
# explain a concept because it contains the word 'price' is the opposite of
# the point. A lone "price"/"rate" needs a market word beside it to count.
_MARKET = (r"share price", r"stock price", r"market price", r"spot price",
           r"quote", r"ltp", r"nav", r"market cap", r"nifty", r"sensex",
           r"dow jones", r"nasdaq", r"crypto", r"bitcoin", r"exchange rate",
           r"gold rate", r"silver rate", r"interest rate", r"repo rate",
           r"usd", r"inr", r"eur")
# a bare price/rate word only counts when something TRADED is beside it.
# Without this, "rate of change" and "price elasticity" get refused as if
# they were quotes, which would make the engine useless for explanation.
_QUOTE_WORD = r"(price|rate|quote|value|worth)"
_ASSET = (r"(share|shares|stock|stocks|equity|equities|bond|fund|index|"
          r"gold|silver|oil|crude|dollar|rupee|euro|yen|pound|commodity|"
          r"ticker|coin|token)")
_BARE_QUOTE = re.compile(
    rf"\b{_QUOTE_WORD}\b[^.]{{0,25}}\b{_ASSET}\b|"
    rf"\b{_ASSET}\b[^.]{{0,25}}\b{_QUOTE_WORD}\b")
_TIME = (r"current", r"currently", r"today", r"todays", r"today's",
         r"right now", r"now", r"latest", r"live", r"at the moment", r"as of")
_OTHER_MOVING = (r"score", r"weather", r"temperature", r"traffic", r"stock",
                 r"stocks", r"trading at", r"trading price", r"market")
# a time-marked ask that wants a NUMBER back, even if it names no market word:
# "what is the current population", "how much is X today"
_WANTS_NUMBER = re.compile(
    r"\bhow (much|many|high|low|big)\b|\bwhat (is|are|was) the (current|"
    r"latest|today'?s|live)\b.{0,40}\b(number|count|total|population|level|"
    r"figure|amount|size|reading)\b")


def _has_word(low: str, words) -> bool:
    return any(re.search(rf"\b{w}\b", low) for w in words)


def is_present_fact(text: str) -> bool:
    """Does this ask want a quantity that moves with the clock?

    Named market quotes qualify on their own (a share price is ALWAYS a
    present fact). Bare price/rate words qualify only in a market context, so
    "price elasticity" and "rate of change" stay explainable. Other moving
    quantities, and time-marked asks that want a number back, qualify when a
    time marker is present.
    """
    low = f" {text.lower()} "
    if _has_word(low, _MARKET):
        return True
    if _BARE_QUOTE.search(low):
        return True
    has_time = _has_word(low, _TIME)
    if not has_time:
        return False
    # with a time marker, a bare quote word IS a quote ("the price today")
    return (_has_word(low, _OTHER_MOVING)
            or _has_word(low, ("price", "rate", "quote"))
            or bool(_WANTS_NUMBER.search(low)))


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
