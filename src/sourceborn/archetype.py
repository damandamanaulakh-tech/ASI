"""THE ARCHETYPE LAYER — the books as generative engines.

His teaching, and the reason this layer exists at all:

    Holy books are generative engines since modern humans came out of caves.
    The words remain the same, but the response is never general. Because
    human intent and situations change infinitely, the lens never runs out of
    specific, sharp readings to guide human life.

    They are not a quote store and not a fact sheet. They do not teach that
    leaves are green — they say nothing about colour. They teach how a human
    has to live, and what humanity is, and with every person, situation and
    intent the meaning and explanation change.

    One event of those books is used in 100 daily responses.

WHY IT IS A LAYER AND NOT A ROW

A row lives inside exactly one container. An archetype reaches rows across
many containers in many segments — THE RECOVERY STAKE touches nine containers
across six segments. Put it in any one of them and it is in the wrong place
eight times over. It does not OWN those rows; it REACHES them. That is a layer
above the three, reaching down.

WHAT IT FIXES

Measured before this existed: *"he bet everything he had to win it all back and
lost what he could never recover"* seated **zero rows**. Not because the rows
were missing — `P1873 Sunk-cost sensitivity` and `P2517 Commitment escalation
risk` were sitting there — but because there is no route from those words to
those rows. The archetype is that route: the same job `bridge.py` does for a
single word, one storey up, at the level of meaning.

WHAT EVERY ARCHETYPE CARRIES

  source          the book and the locus, or his own worked example
  understanding   what it means, in his words where the words are his
  reaches         REAL bank rows, verified against the live registry
  scale           his axis — micro · individual · relational · macro, and more
  intents         which of IT-01..09 it can produce
  discriminator   what tells you this archetype and not its neighbour
  refuses         what it must never be read as
  links           the archetypes it stands against or beside

NOTHING IS CONCLUDED. An archetype that fires raises rows and intent
candidates; it never chooses among them, and it never says the reading is
true of the person in front of you.

NO CEILING. His ruling: *"no count, its open to increase"*. The set below is
what has been extracted so far, not what the layer holds.
"""

from __future__ import annotations

import re

#: Each archetype. `reaches` are real SB-HFR-P ids verified against the live
#: registry — none is invented, and a test re-checks every one of them.
ARCHETYPES = (
    {
        "id": "ARCH-001",
        "name": "THE RECOVERY STAKE",
        "source": "Mahabharata — the dice game; Yudhishthira stakes and loses",
        "tradition": "Hindu",
        "understanding":
            "The desperate greed to win — to hold a reputation almost crushed, "
            "to revive the trust and faith of family and people, to win back "
            "what is already lost — leading a person to stake what is "
            "irreplaceable and unethical.",
        "his_words": "betting is worst, u can loose ur pride too",
        "reaches": [
            ("SB-HFR-P1872", "Escalation-of-commitment risk", "CON-047"),
            ("SB-HFR-P1873", "Sunk-cost sensitivity", "CON-047"),
            ("SB-HFR-P2517", "Commitment escalation risk", "CON-063"),
            ("SB-HFR-P2518", "Commitment de-escalation", "CON-063"),
            ("SB-HFR-P1254", "Loss/negative-feedback processing", "CON-032"),
            ("SB-HFR-P0548", "Reward-history bias", "CON-014"),
            ("SB-HFR-P2484", "Persistence-vs-quit arbitration", "CON-062"),
            ("SB-HFR-P2555", "Identity-protection motive", "CON-064"),
            ("SB-HFR-P2556", "Face-saving motive", "CON-064"),
            ("SB-HFR-P2724", "Agency-restoration", "CON-068"),
            ("SB-HFR-P2820", "Reputation management", "CON-071"),
            ("SB-HFR-P1132", "Temptation resistance", "CON-029"),
        ],
        "scale": {
            "micro": "a kid refusing to turn off a game he is losing",
            "individual": "a gambler; a trader averaging down on a failing stock",
            "relational": "a person arguing past the point of repair to win",
            "macro": "a nation escalating a war rather than admit defeat",
        },
        "intents": ["IT-05", "IT-06"],
        "discriminator":
            "Something was lost BEFORE the act, and the act aims at the state "
            "before the loss. The stake rises as the loss deepens. Stopping "
            "makes the loss final, which is why stopping is impossible.",
        "refuses": "Never read the rising stake as confidence.",
        "links": {"mirror": "ARCH-002", "note": "recovery looks backward; "
                  "impatience looks forward"},
        "triggers": [r"win (it )?(all )?back", r"lost .*(never|cannot|can'?t) recover",
                     r"bet everything", r"double down", r"averaging down",
                     r"recoup", r"make (it|the loss) back", r"chase (the )?loss",
                     r"won'?t (admit|quit|stop)", r"too far to stop",
                     r"already (lost|spent|invested)"],
        "concepts": ["bet", "bets", "betting", "gamble", "gambled", "gambling",
                     "stake", "staked", "stakes", "wager", "wagered", "dice",
                     "lose", "loses", "lost", "losing", "loss", "losses",
                     "recover", "recovered", "recovering", "back", "again",
                     "everything", "all", "ruin", "ruined", "debt", "owed",
                     "pride", "reputation", "yudhishthira", "mahabharata"],
    },
    {
        "id": "ARCH-002",
        "name": "THE GOLDEN CALF",
        "source": "Torah / Exodus — Moses on Sinai; the people demand a quick, "
                  "visible god",
        "tradition": "Jewish · Christian",
        "understanding":
            "Impatience with a long, difficult, invisible process; the demand "
            "for something visible and immediate; worship of instant "
            "gratification and a false sense of security, sacrificing long-term "
            "stability for a shiny illusion.",
        "his_words": "sacrificing long-term stability and truth for an "
                     "immediate, shiny illusion of wealth",
        "reaches": [
            ("SB-HFR-P1133", "Delay of gratification", "CON-029"),
            ("SB-HFR-P1134", "Reward-postponement", "CON-029"),
            ("SB-HFR-P1121", "Impulse suppression", "CON-029"),
            ("SB-HFR-P1145", "Impulse-vs-goal arbitration", "CON-029"),
            ("SB-HFR-P2457", "Effort-cost discounting", "CON-062"),
            ("SB-HFR-P0149", "Urgency signalling", "CON-004"),
            ("SB-HFR-P0308", "Stimulation seeking", "CON-008"),
            ("SB-HFR-P0299", "Novelty seeking", "CON-008"),
            ("SB-HFR-P2661", "Impulsivity", "CON-067"),
        ],
        "scale": {
            "micro": "a child who cannot wait and takes the smaller sweet now",
            "individual": "buying a house that cannot be afforded because it is "
                          "available today",
            "relational": "demanding proof of loyalty instead of letting it show "
                          "over time",
            "macro": "subprime mortgages — a whole system worshipping the "
                     "illusion of infinite easy wealth",
        },
        "intents": ["IT-07", "IT-02"],
        "discriminator":
            "Nothing has been lost yet. What cannot be borne is the WAITING — "
            "the process is long and gives no visible sign, so a visible "
            "substitute is manufactured and treated as the real thing.",
        "refuses": "Never read impatience as greed; they reach for different "
                   "things in different directions.",
        "links": {"mirror": "ARCH-001"},
        "triggers": [r"can'?t wait", r"right now", r"instant", r"quick(er)? (win|money|result)",
                     r"something to show", r"visible proof", r"shortcut",
                     r"why is it taking", r"immediate(ly)?"],
        "concepts": ["wait", "waited", "waiting", "delay", "delayed", "slow",
                     "long", "meanwhile", "while", "still", "yet", "gone",
                     "away", "absent", "impatient", "impatience", "restless",
                     "quick", "quickly", "fast", "now", "immediate", "instant",
                     "visible", "see", "seen", "show", "shown", "proof",
                     "idol", "statue", "image", "melted", "melt", "gold",
                     "calf", "sinai", "moses", "mountain", "substitute",
                     "shortcut", "shiny"],
    },
    {
        "id": "ARCH-003",
        "name": "THE FRUIT AND THE ACT",
        "source": "Bhagavad Gita 2.47 — Nishkama Karma; the right to the action, "
                  "never to its fruits",
        "tradition": "Hindu",
        "understanding":
            "Focus on the righteousness of the action itself rather than "
            "obsession with the reward of that action. When a leader focuses "
            "only on the fruits — stock price, bonuses, personal greed — and "
            "ignores the dharma of the work, a top-heavy structure is built on "
            "lies and collapses when reality arrives.",
        "his_words": "they create a top-heavy pyramid built on lies",
        "reaches": [
            ("SB-HFR-P2529", "Extrinsic motive", "CON-064"),
            ("SB-HFR-P2528", "Intrinsic motive", "CON-064"),
            ("SB-HFR-P2544", "Self-enhancement motive", "CON-064"),
            ("SB-HFR-P2538", "Recognition/status need", "CON-064"),
            ("SB-HFR-P2453", "Instrumentality (effort→outcome)", "CON-062"),
            ("SB-HFR-P1441", "Reward prediction", "CON-037"),
            ("SB-HFR-P1251", "Outcome monitoring", "CON-032"),
            ("SB-HFR-P1253", "Reward-vs-expectation comparison", "CON-032"),
            ("SB-HFR-P2691", "Outcome-based agency", "CON-068"),
            ("SB-HFR-P2561", "Value-behaviour alignment", "CON-064"),
        ],
        "scale": {
            "micro": "a child working for the sticker and not the reading",
            "individual": "optimising the metric instead of the work",
            "relational": "performing care for how it looks",
            "macro": "Enron and Lehman Brothers — quarterly numbers over the "
                     "actual business",
        },
        "intents": ["IT-08", "IT-01"],
        "discriminator":
            "The reward is being pursued INSTEAD of the quality of the act, and "
            "the two have come apart. Look for a metric standing in for the "
            "thing the metric was meant to measure.",
        "refuses": "Never read this as 'rewards are bad'. The teaching is about "
                   "which one is being aimed at, not whether reward exists.",
        "links": {"beside": "ARCH-005"},
        "triggers": [r"bonus", r"quarterly", r"stock price", r"target(s)?",
                     r"look(s|ed)? good", r"on paper", r"the numbers",
                     r"just (to )?(win|get) the", r"for the (money|credit|reward)"],
        "concepts": ["fruit", "fruits", "result", "results", "reward", "rewards",
                     "outcome", "outcomes", "return", "returns", "payoff",
                     "bonus", "commission", "profit", "profits", "revenue",
                     "quarter", "quarterly", "target", "targets", "metric",
                     "metrics", "number", "numbers", "score", "kpi", "ranking",
                     "action", "act", "work", "duty", "craft", "quality",
                     "righteous", "righteousness", "dharma", "karma", "gita",
                     "leader", "leaders", "management", "shareholders"],
    },
    {
        "id": "ARCH-004",
        "name": "DIAMOND CUT DIAMOND",
        "source": "His own worked teaching — the proverb read archetypally",
        "tradition": "proverb / his reading",
        "understanding":
            "Literally a diamond is the hardest material. Archetypally it is two "
            "immovable forces. When ordinary people meet a diamond — a powerful, "
            "stubborn, ego-driven person — the dynamic is one-sided. When two "
            "diamonds clash the meaning shifts completely: ego cutting ego, an "
            "entirely new psychological outcome.",
        "his_words": "its ego cut ego",
        "reaches": [
            ("SB-HFR-P0304", "Dominance drive", "CON-008"),
            ("SB-HFR-P2550", "Dominance motive", "CON-064"),
            ("SB-HFR-P2822", "Status seeking", "CON-071"),
            ("SB-HFR-P2823", "Rank/hierarchy perception", "CON-071"),
            ("SB-HFR-P2555", "Identity-protection motive", "CON-064"),
            ("SB-HFR-P2556", "Face-saving motive", "CON-064"),
            ("SB-HFR-P2138", "Face-saving interpretation", "CON-054"),
            ("SB-HFR-P2497", "Intention conflict resolution", "CON-063"),
            ("SB-HFR-P1241", "Conflict detection", "CON-032"),
            ("SB-HFR-P2849", "Authority/respect value", "CON-072"),
        ],
        "scale": {
            "micro": "two children who will not be the one to look away",
            "individual": "a negotiation where neither can be seen to move first",
            "relational": "two people who are each used to being deferred to",
            "macro": "two states, each of whose leader cannot be seen to concede",
        },
        "intents": ["IT-06", "IT-05"],
        "discriminator":
            "BOTH sides carry the same immovability. The signature is symmetry — "
            "if one side would yield under pressure this is not the archetype.",
        "refuses": "Never read it as one person being strong. It is a property of "
                   "the MEETING, not of either party.",
        "links": {"beside": "ARCH-005"},
        "triggers": [r"diamond cut diamond", r"diamond cuts diamond",
                     r"both (of them|refuse|insist)", r"neither (will|would|can)",
                     r"ego", r"back(ing)? down", r"who blinks", r"stand.?off",
                     r"stubborn", r"clash"],
        "concepts": ["diamond", "diamonds", "cut", "cuts", "hardest", "hard",
                     "both", "neither", "each", "other", "equal", "equally",
                     "match", "matched", "meet", "meets", "met", "against",
                     "ego", "egos", "pride", "stubborn", "immovable", "rigid",
                     "refuse", "refuses", "refused", "yield", "budge",
                     "deadlock", "stalemate", "standoff", "clash", "collide"],
    },
    {
        "id": "ARCH-005",
        "name": "VIRTUE WITHOUT LIMIT",
        "source": "Mahabharata — Yudhishthira, the most truthful man, stakes his "
                  "wife and loses",
        "tradition": "Hindu",
        "understanding":
            "Dharma is not about truth only. The most righteous man made the "
            "life's biggest mistake. Being righteous and adherent to truth does "
            "not make you great all the time — a virtue held alone, without "
            "limits, fails. We must define our limits even while being "
            "righteous.",
        "his_words": "being righteousness and adherence to truth dosent make u "
                     "great all the time",
        "reaches": [
            ("SB-HFR-P2879", "Moral-identity", "CON-072"),
            ("SB-HFR-P2554", "Moral/value-based motive", "CON-064"),
            ("SB-HFR-P2553", "Loyalty motive", "CON-064"),
            ("SB-HFR-P2545", "Consistency motive", "CON-064"),
            ("SB-HFR-P2562", "Sacred/protected values", "CON-064"),
            ("SB-HFR-P2853", "Duty/obligation sense", "CON-072"),
            ("SB-HFR-P2843", "Group-norm adherence", "CON-071"),
            ("SB-HFR-P2700", "Responsibility attribution", "CON-068"),
            ("SB-HFR-P2712", "Moral responsibility judgment", "CON-068"),
            ("SB-HFR-P2849", "Authority/respect value", "CON-072"),
        ],
        "scale": {
            "micro": "the honest child who will not lie even to prevent harm",
            "individual": "a professional bound by a rule that is destroying the "
                          "thing the rule protects",
            "relational": "keeping a promise that has become the wrong thing to keep",
            "macro": "a state dragged into a war by a treaty it no longer wants",
        },
        "intents": ["IT-06", "IT-04"],
        "discriminator":
            "The actor is known for the very quality that produced the act; "
            "refusing would have contradicted who they are; and there is no "
            "personal gain in it.",
        "refuses":
            "Being bound by virtue is NOT the same as being virtuous in the act. "
            "Yudhishthira's righteousness produced the worst act of his life.",
        "links": {"beside": "ARCH-010"},
        "triggers": [r"gave (his|her|my) word", r"could not refuse",
                     r"had no choice", r"could not (say no|back out|walk away)",
                     r"principle", r"never break", r"always (keeps|kept)",
                     r"honour", r"the rules? (say|said)"],
        "concepts": ["truth", "truthful", "honest", "honesty", "righteous",
                     "righteousness", "virtue", "virtuous", "good", "moral",
                     "principle", "principles", "vow", "word", "promise",
                     "oath", "dharma", "duty", "obligation", "bound", "must",
                     "cannot", "refuse", "refused", "limit", "limits",
                     "always", "never", "yudhishthira", "mahabharata", "wife",
                     "staked", "stake", "mistake", "worst"],
    },
    {
        "id": "ARCH-006",
        "name": "VERIFY BEFORE HARM",
        "source": "Qur'an 49:6 — Surah Al-Hujurat; report verification before "
                  "acting on it",
        "tradition": "Islam",
        "understanding":
            "When information arrives that would justify harm, it is verified "
            "before it is acted on. The gap between a claim arriving and a claim "
            "being true is where the whole danger lives.",
        "his_words": None,
        "reaches": [
            ("SB-HFR-P1354", "Fact verification (internal)", "CON-034"),
            ("SB-HFR-P1684", "Correlation-vs-causation distinction", "CON-043"),
            ("SB-HFR-P1738", "Evidence-strength weighting", "CON-044"),
            ("SB-HFR-P1739", "Evidence aggregation", "CON-044"),
            ("SB-HFR-P1758", "Stopping-rule (enough evidence)", "CON-044"),
            ("SB-HFR-P2976", "Source monitoring", "CON-075"),
            ("SB-HFR-P2977", "Reality monitoring", "CON-075"),
            ("SB-HFR-P3011", "Confirmation bias", "CON-076"),
            ("SB-HFR-P3041", "Illusory correlation", "CON-076"),
            ("SB-HFR-P0764", "Evidence accumulation", "CON-020"),
        ],
        "scale": {
            "micro": "a parent about to punish on one child's account of events",
            "individual": "acting on a forwarded message",
            "relational": "confronting someone on what a third party said",
            "macro": "a viral screenshot demanding action before verification",
        },
        "intents": ["IT-02", "IT-04"],
        "discriminator":
            "A claim has arrived, an action would follow, and the action is "
            "harder to undo than the verification would have been.",
        "refuses":
            "Bounded mapping only. The ayah is not equated with modern "
            "fact-checking doctrine in total — the four layers (source text, "
            "translation, interpretation, machine mapping) never merge.",
        "links": {"beside": "ARCH-007"},
        "triggers": [r"i heard", r"they said", r"someone told", r"apparently",
                     r"forward(ed)?", r"screenshot", r"everyone (is saying|knows)",
                     r"before (we|i|you) (act|decide|do)"],
        "concepts": ["heard", "hear", "told", "said", "says", "report",
                     "reported", "rumour", "rumor", "gossip", "claim",
                     "claimed", "allegation", "alleged", "accused", "accuse",
                     "message", "forward", "forwarded", "screenshot", "news",
                     "verify", "verified", "check", "checked", "confirm",
                     "confirmed", "true", "false", "before", "act", "acted",
                     "punish", "punished", "harm", "fire", "fired", "expel",
                     "quran", "ayah"],
    },
    {
        "id": "ARCH-007",
        "name": "TEST AND RETAIN",
        "source": "1 Thessalonians 5:21 — examine everything; hold fast what is "
                  "good",
        "tradition": "Christian",
        "understanding":
            "Nothing is accepted because it arrived, and nothing is discarded "
            "because it is unfamiliar. Each thing is tested, and what survives "
            "the test is kept — which is a stopping rule as much as a test.",
        "his_words": None,
        "reaches": [
            ("SB-HFR-P1652", "Hypothesis inference", "CON-042"),
            ("SB-HFR-P1906", "Hypothesis generation", "CON-048"),
            ("SB-HFR-P1232", "Stopping-rule application", "CON-031"),
            ("SB-HFR-P1758", "Stopping-rule (enough evidence)", "CON-044"),
            ("SB-HFR-P1735", "Confidence calibration", "CON-044"),
            ("SB-HFR-P1729", "Probability calibration", "CON-044"),
            ("SB-HFR-P1257", "Accuracy monitoring", "CON-032"),
            ("SB-HFR-P1280", "Monitoring-accuracy calibration", "CON-032"),
            ("SB-HFR-P2993", "Self-testing", "CON-075"),
            ("SB-HFR-P3012", "Disconfirmation avoidance", "CON-076"),
        ],
        "scale": {
            "micro": "a child checking an answer instead of assuming it",
            "individual": "running the experiment rather than arguing the point",
            "relational": "asking rather than concluding",
            "macro": "a field that replicates before it builds on a result",
        },
        "intents": ["IT-02"],
        "discriminator":
            "Two things are present at once: a test that could fail, and a rule "
            "for when testing stops. Either alone is not this archetype.",
        "refuses": "Translation versions are never blended into one synthetic "
                   "quotation; commentary is never promoted to canon.",
        "links": {"beside": "ARCH-006"},
        "triggers": [r"how do (we|i|you) know", r"test(ed|ing)?", r"check(ed|ing)?",
                     r"prove", r"evidence", r"verify", r"make sure"],
        "concepts": ["test", "tested", "testing", "examine", "examined",
                     "examination", "try", "tried", "trial", "check",
                     "checked", "prove", "proved", "proof", "evidence",
                     "verify", "verified", "everything", "all", "hold", "held",
                     "keep", "kept", "retain", "good", "sound", "survive",
                     "survived", "discard", "reject", "rejected", "enough",
                     "stop", "stopping"],
    },
    {
        "id": "ARCH-008",
        "name": "THE DISCRIMINATIVE INTELLECT",
        "source": "Bhagavad Gita 18:30 — the intellect that knows action from "
                  "inaction, duty from non-duty, fear from fearlessness, bondage "
                  "from freedom",
        "tradition": "Hindu",
        "understanding":
            "The faculty that tells apart what looks the same: which act is "
            "action and which is only motion; which obligation is real and which "
            "is assumed; which caution is fear and which is judgment; which "
            "attachment binds and which frees.",
        "his_words": None,
        "reaches": [
            ("SB-HFR-P1620", "Essential-vs-incidental separation", "CON-041"),
            ("SB-HFR-P1607", "Boundary setting (category)", "CON-041"),
            ("SB-HFR-P2938", "Discrimination learning", "CON-074"),
            ("SB-HFR-P2869", "Moral-dilemma resolution", "CON-072"),
            ("SB-HFR-P2559", "Motive-conflict resolution", "CON-064"),
            ("SB-HFR-P2557", "Competing-motive detection", "CON-064"),
            ("SB-HFR-P2496", "Competing-intention arbitration", "CON-063"),
            ("SB-HFR-P1145", "Impulse-vs-goal arbitration", "CON-029"),
            ("SB-HFR-P2853", "Duty/obligation sense", "CON-072"),
        ],
        "scale": {
            "micro": "a child telling 'I can't' from 'I don't want to'",
            "individual": "telling a real deadline from an urgent-sounding one",
            "relational": "telling care from control",
            "macro": "telling a mandate from a convention nobody questioned",
        },
        "intents": ["IT-04", "IT-03"],
        "discriminator":
            "Two things are being treated as the same thing and they are not. "
            "The archetype fires on the CONFLATION, not on either side of it.",
        "refuses": "No cross-scripture equivalence: this is not treated as "
                   "identical to any other tradition's verification instruction.",
        "links": {"beside": "ARCH-006"},
        "triggers": [r"same thing", r"but is it really", r"difference between",
                     r"or is (it|that) just", r"looks like", r"which one"],
        "concepts": ["difference", "differ", "different", "same", "alike",
                     "similar", "distinguish", "tell", "apart", "between",
                     "which", "whether", "or", "action", "inaction", "motion",
                     "busy", "duty", "obligation", "fear", "fearless",
                     "caution", "courage", "bondage", "freedom", "free",
                     "bound", "attachment", "confuse", "confused", "mistaken",
                     "mistake", "looks", "seems", "appears", "really",
                     "actually", "buddhi", "intellect", "discern"],
    },
    {
        "id": "ARCH-009",
        "name": "TRUTH AND TRUTHFUL LIVING",
        "source": "Sri Guru Granth Sahib Ji, Ang 62 — truth held apart from the "
                  "living of it",
        "tradition": "Sikhi",
        "understanding":
            "Knowing what is true and living truthfully are two different "
            "attainments, and the second is the harder. A true statement held by "
            "someone who does not live it has not become knowledge in the sense "
            "that matters.",
        "his_words": None,
        "reaches": [
            ("SB-HFR-P2561", "Value-behaviour alignment", "CON-064"),
            ("SB-HFR-P2883", "Moral-judgment vs moral-action gap", "CON-072"),
            ("SB-HFR-P2872", "Moral disengagement", "CON-072"),
            ("SB-HFR-P2873", "Moral-hypocrisy detection", "CON-072"),
            ("SB-HFR-P2879", "Moral-identity", "CON-072"),
            ("SB-HFR-P2878", "Values-clarification", "CON-072"),
            ("SB-HFR-P2554", "Moral/value-based motive", "CON-064"),
        ],
        "scale": {
            "micro": "a child who can recite the rule and does not follow it",
            "individual": "knowing the habit is harmful and continuing",
            "relational": "saying the value aloud while acting against it",
            "macro": "an institution whose stated values and conduct diverge",
        },
        "intents": ["IT-06", "IT-01"],
        "discriminator":
            "The knowledge is not in doubt. The gap is between holding it and "
            "living it — so look for a stated value beside an opposing act.",
        "refuses":
            "No single English rendering is frozen as the total meaning; the "
            "Gurmukhi, the translations and the competing interpretations stay "
            "parallel records. Final mapping is held for his review.",
        "links": {"beside": "ARCH-005"},
        "triggers": [r"knows? (better|it'?s wrong)", r"said .* but", r"preach",
                     r"hypocri", r"do as i say", r"in theory"],
        "concepts": ["truth", "true", "truthful", "living", "live", "lives",
                     "lived", "practice", "practise", "preach", "preached",
                     "teach", "taught", "say", "said", "says", "know", "knows",
                     "knew", "knowledge", "believe", "believes", "value",
                     "values", "but", "however", "still", "anyway", "hypocrisy",
                     "hypocrite", "double", "standard", "gap", "behaviour",
                     "behavior", "conduct", "guru", "granth", "nanak"],
    },
    {
        "id": "ARCH-010",
        "name": "THE ONE WHO IS LEFT WITH MEMORIES",
        "source": "His own teaching — the good person; parentification and the "
                  "super-helper",
        "tradition": "his reading",
        "understanding":
            "A person whom family, friends and coworkers call good — by nature, "
            "by behaviour, by taking responsibility, by carrying liabilities — "
            "is left with memories only, because under that burden such a person "
            "cannot, is unable to, or never does think about themselves. And "
            "still keeps going, to keep their beloved safe and alive.",
        "his_words": "in the burden of such things, such personalities cant or "
                     "unable or never think about themself and at end they left "
                     "with the memories only",
        "reaches": [
            ("SB-HFR-P2548", "Care/nurturance motive", "CON-064"),
            ("SB-HFR-P0292", "Caregiving/nurturing drive", "CON-008"),
            ("SB-HFR-P2700", "Responsibility attribution", "CON-068"),
            ("SB-HFR-P2543", "Self-protection motive", "CON-064"),
            ("SB-HFR-P2537", "Belonging need", "CON-064"),
            ("SB-HFR-P2458", "Persistence", "CON-062"),
            ("SB-HFR-P2454", "Effort willingness", "CON-062"),
            ("SB-HFR-P2707", "Learned-helplessness (agency loss)", "CON-068"),
            ("SB-HFR-P0293", "Attachment/proximity drive", "CON-008"),
            ("SB-HFR-P1504", "Emotional-memory persistence", "CON-038"),
        ],
        "scale": {
            "micro": "the eldest child who always gives in",
            "individual": "the carer who cannot rest",
            "relational": "the friend everyone calls, who never calls anyone",
            "macro": "the institution that absorbs every failure around it "
                     "until it fails",
        },
        "intents": ["IT-06", "IT-01"],
        "discriminator":
            "Responsibility is being carried at the actor's own cost, the actor "
            "is not counting that cost, and there is no gain in it. The signature "
            "is the ABSENCE of self-reference, not the presence of sacrifice.",
        "refuses":
            "The memories are what is LEFT OVER, not what was earned. Never read "
            "the cost as a reward, and never conclude that a person who receives "
            "nothing is therefore good.",
        "links": {"beside": "ARCH-005"},
        "triggers": [r"everyone (depends|relies)", r"never (says no|refuses|complains)",
                     r"takes care of", r"holds? (it|everything) together",
                     r"looks after", r"no one asks (him|her|them)"],
        "concepts": ["good", "kind", "nature", "responsibility", "responsible",
                     "burden", "burdens", "liability", "liabilities", "carry",
                     "carried", "carries", "care", "cares", "cared", "look",
                     "looks", "after", "family", "friends", "coworkers",
                     "everyone", "everybody", "depend", "depends", "relies",
                     "rely", "nothing", "return", "left", "memories", "memory",
                     "himself", "herself", "themself", "themselves", "own",
                     "sacrifice", "sacrificed", "give", "gave", "given",
                     "keep", "keeps", "going", "safe", "alive"],
    },
    {
        "id": "ARCH-011",
        "name": "THE ACT WITH MANY INTENTS",
        "source": "His own worked teaching — the man stealing money; one event, "
                  "four readings",
        "tradition": "his reading",
        "understanding":
            "One visible act carries more than one possible reason, and the act "
            "alone can never say which. A man taking money is a thief, or a man "
            "who found an opening, or a man repeating a habit, or a man saving a "
            "life — the hand moves identically in all four. The archetype is the "
            "refusal to let the visible act name the intent, and the demand that "
            "every candidate reason stay open until something outside the act "
            "separates them.",
        "his_words": "a man is stealing money — thief / opportunity / habit / "
                     "saving a life",
        "reaches": [
            ("SB-HFR-P2525", "Stated motive", "CON-064"),
            ("SB-HFR-P2526", "Operating (actual) motive", "CON-064"),
            ("SB-HFR-P2527", "Hidden-motive hypothesis", "CON-064"),
            ("SB-HFR-P2557", "Competing-motive detection", "CON-064"),
            ("SB-HFR-P2564", "Motive-inference confidence", "CON-064"),
            ("SB-HFR-P2547", "Survival motive", "CON-064"),
            ("SB-HFR-P2123", "Speaker-intent inference", "CON-054"),
            ("SB-HFR-P1718", "Causal attribution", "CON-043"),
            ("SB-HFR-P1719", "Blame/responsibility attribution", "CON-043"),
            ("SB-HFR-P1684", "Correlation-vs-causation distinction", "CON-043"),
            ("SB-HFR-P1651", "Abduction (best explanation)", "CON-042"),
            ("SB-HFR-P1176", "Alternative-generation", "CON-030"),
            ("SB-HFR-P1197", "Openness-to-alternatives", "CON-030"),
            ("SB-HFR-P2076", "Ambiguity holding", "CON-052"),
            ("SB-HFR-P2845", "Harm/care judgment", "CON-072"),
            ("SB-HFR-P2846", "Fairness/justice judgment", "CON-072"),
            ("SB-HFR-P2854", "Moral-intuition (fast)", "CON-072"),
            ("SB-HFR-P2855", "Moral-reasoning (deliberate)", "CON-072"),
            ("SB-HFR-P2881", "Cheating/temptation resistance", "CON-072"),
            ("SB-HFR-P1132", "Temptation resistance", "CON-029"),
        ],
        "scale": {
            "micro": "a child taking a biscuit before dinner",
            "individual": "a man taking money from a till",
            "relational": "a partner reading a late arrival as a betrayal",
            "macro": "a state reading a troop movement as an attack",
        },
        "intents": ["IT-01", "IT-02", "IT-03", "IT-04", "IT-05", "IT-06",
                    "IT-07", "IT-08", "IT-09"],
        "discriminator":
            "A single observable act is present and a label for the actor is "
            "available. The archetype fires on that pairing — not on the act's "
            "severity. If the source states the reason and the reason is "
            "verified, this is not the archetype; it is a settled event.",
        "refuses":
            "Never let the act name the actor. THIEF is a conclusion, not an "
            "observation, and taking money is the observation. All candidate "
            "reasons stay open together and none is ranked by how it sounds.",
        "links": {"beside": "ARCH-008",
                  "note": "the discriminative intellect tells apart what looks "
                          "the same; this one refuses to conclude before it can"},
        "triggers": [r"steal(ing|s)?", r"stole", r"theft", r"thief",
                     r"took (the )?(money|cash|it)", r"taking (the )?(money|cash)",
                     r"caught (him|her|them)", r"why (did|would) (he|she|they)",
                     r"must (have )?be", r"obviously", r"clearly (a|an|he|she)"],
        "concepts": ["steal", "stealing", "stole", "stolen", "theft", "thief",
                     "took", "take", "taking", "money", "cash", "shop", "till",
                     "caught", "saw", "seen", "watched", "act", "action",
                     "reason", "reasons", "why", "intent", "intention",
                     "motive", "because", "opportunity", "habit", "desperate",
                     "hunger", "hungry", "save", "saving", "dying", "child",
                     "medicine", "judge", "judged", "blame", "guilty",
                     "criminal", "assume", "assumed"],
    },
)

#: His ruling — the layer has no ceiling. This is what has been extracted so
#: far, not what the layer holds.
CEILING = None


def archetypes() -> tuple:
    return ARCHETYPES


def get(aid: str) -> dict:
    return next((a for a in ARCHETYPES if a["id"] == aid), {"found": False, "id": aid})


#: How many distinct concept words the MEANING route needs before an archetype
#: may fire on meaning alone. One word is a coincidence — "back", "all", "good"
#: appear in ordinary sentences that have nothing to do with any archetype. Two
#: distinct words from the same archetype's own vocabulary is the smallest
#: number that is an arrangement rather than an accident, and it is his own
#: standing bar for a shape: one occurrence is never a pattern.
MEANING_MIN = 2

_WORD = re.compile(r"[a-z]+")


def _shared() -> dict:
    """How many archetypes each concept word belongs to.

    This is his own IDF bar, one storey up. Against the 3,204 the rule is that
    a word appearing in forty of his names is weaker evidence than a rare one;
    here a word appearing in several archetypes' vocabularies is weaker
    evidence than one belonging to a single archetype. `everything` and `all`
    sit in three lists apiece and say nothing about which shape is present;
    `bet`, `recover` and `idol` sit in one and say a great deal."""
    counts = {}
    for a in ARCHETYPES:
        for w in set(a.get("concepts", ())):
            counts[w] = counts.get(w, 0) + 1
    return counts


#: A concept word belonging to exactly one archetype's vocabulary is
#: DISTINCTIVE. The MEANING route needs MEANING_MIN words in total AND at
#: least one distinctive among them — two shared words are an accident of
#: ordinary English, not a shape.
SHARED = _shared()


def _words(text: str) -> list:
    """Content words, lowercased, hyphens split — the same treatment the
    seating gives them, so `Point-of-no-return` can be reached by `point`."""
    return _WORD.findall((text or "").lower().replace("-", " ").replace("/", " "))


def _hits(text: str, a: dict) -> list:
    """Both routes to an archetype, each naming its own evidence.

    ROUTE 1 — PHRASE. A regex from `triggers` matches. This is the narrow route
    and it is the one that fails on unfamiliar wording.

    ROUTE 2 — MEANING. At least MEANING_MIN distinct words from the archetype's
    own concept vocabulary are present. This is the route that carries his
    macro reading: the archetype is a shape, and a shape survives rewording.
    His dice game reads the same whether it is dice, a stock, or a war.

    Neither route concludes. Both attach what they matched on, so a firing can
    always be argued with."""
    low = " " + (text or "").lower() + " "
    out = []
    for pat in a["triggers"]:
        m = re.search(pat, low)
        if m:
            out.append({"route": "PHRASE", "pattern": pat,
                        "matched": m.group(0).strip()})
    concepts = set(a.get("concepts", ()))
    if concepts:
        present = sorted(w for w in set(_words(text)) if w in concepts)
        distinctive = [w for w in present if SHARED.get(w, 1) == 1]
        if len(present) >= MEANING_MIN and distinctive:
            out.append({"route": "MEANING",
                        "pattern": "%d concept words, %d distinctive"
                                   % (len(present), len(distinctive)),
                        "matched": " · ".join(present), "words": present,
                        "distinctive": distinctive, "count": len(present)})
    return out


def fires_on(text: str) -> dict:
    """Which archetypes land on this text, and what rows they reach that the
    words alone could never reach.

    Nothing is concluded. A firing archetype raises rows and intent candidates
    and states its own discriminator and refusal beside them."""
    fired, considered = [], []
    for a in ARCHETYPES:
        hs = _hits(text, a)
        rec = {"id": a["id"], "name": a["name"], "matched": hs}
        if hs:
            fired.append({
                "id": a["id"], "name": a["name"], "source": a["source"],
                "tradition": a["tradition"],
                "understanding": a["understanding"],
                "matched_on": [h["matched"] for h in hs],
                "routes": sorted({h["route"] for h in hs}),
                "evidence": hs,
                "reaches": [{"id": p, "name": n, "container": c}
                            for p, n, c in a["reaches"]],
                "rows_reached": len(a["reaches"]),
                "scale": a["scale"],
                "intents": a["intents"],
                "discriminator": a["discriminator"],
                "refuses": a["refuses"],
                "links": a["links"],
                "chosen": None,
            })
        else:
            considered.append(rec)
    rows = {}
    for f in fired:
        for r in f["reaches"]:
            rows.setdefault(r["id"], dict(r, via=[]))["via"].append(f["id"])
    return {
        "text": text,
        "fired": fired,
        "fired_count": len(fired),
        "considered": len(ARCHETYPES),
        "rows_reached": sorted(rows.values(), key=lambda r: r["id"]),
        "rows_reached_count": len(rows),
        "intents_raised": sorted({i for f in fired for i in f["intents"]}),
        "concluded": None,
        "law": "an archetype REACHES rows across containers; it never owns them, "
               "never chooses among them, and never says the reading is true of "
               "the person in front of you.",
    }


def compare(text: str) -> dict:
    """The proof: what the words alone reach, against what the archetype adds."""
    from . import growing as W
    seated = W.place(text, "archetype-compare")
    words = {s["sb_id"] for s in seated.get("strengthened", [])}
    fired = fires_on(text)
    via = {r["id"] for r in fired["rows_reached"]}
    return {
        "text": text,
        "words_alone": {"rows": len(words), "ids": sorted(words)},
        "with_archetype": {"rows": len(via | words), "added": len(via - words),
                           "added_ids": sorted(via - words)},
        "archetypes_fired": [f["id"] + " " + f["name"] for f in fired["fired"]],
        "gain": len(via - words),
        "law": "the archetype is the route the words could not take. It adds "
               "rows; it does not replace the seating.",
    }


def stats() -> dict:
    return {
        "archetypes": len(ARCHETYPES),
        "ceiling": CEILING,
        "traditions": sorted({a["tradition"] for a in ARCHETYPES}),
        "rows_reached_total": sum(len(a["reaches"]) for a in ARCHETYPES),
        "distinct_rows": len({p for a in ARCHETYPES for p, _, _ in a["reaches"]}),
        "distinct_containers": len({c for a in ARCHETYPES for _, _, c in a["reaches"]}),
        "intents_covered": sorted({i for a in ARCHETYPES for i in a["intents"]}),
        "scales": ["micro", "individual", "relational", "macro"],
        "law": "no count — the layer is open to increase with every example.",
        "never": "an archetype creates no parameter and concludes no intent.",
    }


def annotations() -> list:
    return [
        ("the books are generative engines, not a quote store", "archetype.ARCHETYPES"),
        ("one event of those books is used in 100 daily responses", "archetype.fires_on"),
        ("an archetype reaches rows, it never owns them", "archetype.compare"),
        ("no count, open to increase", "archetype.CEILING"),
    ]
