"""THE SUBJECT BRAINS — his platform superimposed on a real person.

His words on handing these back:

    ur own old docs
    hope adding more

They are mine, from an earlier session: `RIEMANN_BRAIN_v0.1.xlsx` and
`EINSTEIN_BRAIN_v0.1.xlsx` — his 10/80/2,560 platform laid over Bernhard Riemann
(1826-1866) and Albert Einstein (1879-1955). Two subjects, same frame, so the
frame itself can be read against a life instead of against a sentence.

They belong to the GROWING PHASE and are handled as it requires: **placed, not
answered.** What they carry into the base is

    25 named parameter candidates   R-01..R-11 · E-01..E-10 · X-01..X-04
    14 halts still addressed to him H-1..H-7 · E-1..E-7, none ever answered
     9 stuck/deliver patterns       what each man does at a halt, and on his word

THE VERSION GAP, SURFACED NOT CLOSED

Both workbooks are built on **2,560** sub-parameters. His current registry holds
**3,204**. Their atom names differ from the current ones — the Einstein file says
`Temperature balance` where the registry says `Core temperature setpoint`. So this
is not one bank in two files; it is **two versions of the bank**, and the older one
carries a numbering he already warned about himself in the workbook:

    NOTE | Numbering | ... the owner's own corpus already assigned 2561-2590 in the
    King-brain runs. Assigning registry numbers is the owner's call.

That is the same shape as his ASI0001 ruling — *do not silently merge namespaces*
— so nothing here is renumbered into his flat index, and the candidates are
`CANDIDATE` rows, not `PARAM` rows.

WHAT PLACING THEM EXPOSED — a defect in the growing phase itself

The Einstein workbook contains a full atom-by-atom expansion of the older 2,560.
Placed whole, it seated **a taxonomy on a taxonomy**: 1,086 ids "reached", top hits
`Load-force coupling`, `Agonist activation`, `Synergy activation` — none of which
is about Einstein. `growing.registry_echo()` now catches parameter-list rows by
SHAPE and `place()` excludes them: 489,688 chars of text drop to 74,037, and the
seats become `Stopping-rule (enough evidence)`, `Pattern abstraction`, `Rule
extraction`, `Nearest-possible-world reasoning`.

Canon: docs/method/canon/THE_SUBJECT_BRAINS.md
"""

from __future__ import annotations

RIEMANN = "RIEMANN_BRAIN_v0.1"
EINSTEIN = "EINSTEIN_BRAIN_v0.1"

BUILT_ON = 2560          # what the workbooks were built against
CURRENT_BANK = 3204      # what the registry holds now

# ---------------------------------------------------------------------------
# THE 25 CANDIDATES — verbatim from the workbooks' NEW PARAM CANDIDATES sheets.
# ---------------------------------------------------------------------------

CANDIDATES = (
    {"id": "R-01", "subject": RIEMANN, "name": "Release-ripeness gate",
     "home": "Segment 6", "h": "H6",
     "why": "a threshold governing RELEASE of finished work, distinct from "
            "commitment-to-goal. The registry cannot represent a person who "
            "finishes and withholds."},
    {"id": "R-02", "subject": RIEMANN,
     "name": "Kept-file practice (external half-store)", "home": "CON-080",
     "h": "H5",
     "why": "an unpublished store of formed work that can complete answers "
            "later, possibly in other hands."},
    {"id": "R-03", "subject": RIEMANN, "name": "Declared-intent auditability",
     "home": "CON-063", "h": "H6",
     "why": "degree to which a person states intent BEFORE work in verifiable "
            "form. Riemann near-total; most humans near-zero."},
    {"id": "R-04", "subject": RIEMANN, "name": "Provisional-halt register",
     "home": "CON-077", "h": "H6",
     "why": "naming, dating and storing halts with return-intent — distinct "
            "from abandonment and from denial."},
    {"id": "R-05", "subject": RIEMANN, "name": "Successor-loop design",
     "home": "CON-079/080", "h": "H5",
     "why": "structuring work so its open loops are continuable by others."},
    {"id": "R-06", "subject": RIEMANN, "name": "Understatement coefficient",
     "home": "CON-044", "h": "H5",
     "why": "systematic DOWNWARD offset between stated confidence and held "
            "evidence. The registry's confidence-error classes only cover "
            "overconfidence."},
    {"id": "R-07", "subject": RIEMANN, "name": "Constraint-rise coefficient",
     "home": "Segment 4 / Filter 28", "h": "H3",
     "why": "performance delta under imposed constraint vs self-paced. Riemann "
            "strongly positive; many humans negative."},
    {"id": "R-08", "subject": RIEMANN, "name": "Duty-first resource routing",
     "home": "CON-064 / Filter 29", "h": "H3",
     "why": "loyalty-obligation fixed above self-maintenance under scarcity, "
            "visible in money flows."},
    {"id": "R-09", "subject": RIEMANN, "name": "Presupposition-salience",
     "home": "CON-014", "h": "H5",
     "why": "attention captured by what a field treats as GIVEN — the "
            "background becoming the figure."},
    {"id": "R-10", "subject": RIEMANN, "name": "Private-ambition mask",
     "home": "Segment 9", "h": "H5",
     "why": "modest public presentation over a vast private programme, with no "
            "deception in content — the ambition is simply never said."},
    {"id": "R-11", "subject": RIEMANN, "name": "Post-repair overshoot",
     "home": "CON-077", "h": "H2",
     "why": "recovery from collapse that lands ABOVE the prior level, not at "
            "it."},
    {"id": "E-01", "subject": EINSTEIN, "name": "Aesthetic-offense trigger",
     "home": "CON-014", "h": "H5",
     "why": "the trigger is UGLINESS in an accepted picture, not error. The "
            "salience atoms (novelty, threat, reward) miss 'the inelegant'."},
    {"id": "E-02", "subject": EINSTEIN, "name": "Minority-witness stamina",
     "home": "Segment 8/9 boundary", "h": "H5",
     "why": "holding a dissenting testimony against field consensus for decades "
            "without averaging. Distinct from stubbornness — he updates "
            "everywhere else."},
    {"id": "E-03", "subject": EINSTEIN, "name": "Release polarity (gate vs iterate)",
     "home": "CON-047", "h": "H5",
     "why": "ONE AXIS, TWO POLES: Riemann's ripeness-gate against Einstein's "
            "publish-and-self-strike. The registry needs the axis, not two "
            "unrelated parameters."},
    {"id": "E-04", "subject": EINSTEIN, "name": "Humor-cipher", "home": "CON-054",
     "h": "H3",
     "why": "hard content encoded as jokes — same function as Riemann's "
            "understatement-code, different cipher. Suggests a general "
            "'delivery cipher type'."},
    {"id": "E-05", "subject": EINSTEIN, "name": "Fame-load management",
     "home": "CON-071", "h": "H3",
     "why": "mass attention processed as weather. The status containers assume "
            "status is SOUGHT; his case is status ARRIVING unsought."},
    {"id": "E-06", "subject": EINSTEIN, "name": "Regret-ledger",
     "home": "new failure class", "h": "H3",
     "why": "a kept promise logged as a LOSS (the 1939 signature). The 20 "
            "failure classes cover errors and gaps, not successful deliveries "
            "later wished undone."},
    {"id": "E-07", "subject": EINSTEIN, "name": "Combinatory-play engine",
     "home": "CON-048", "h": "H5",
     "why": "pre-verbal imagistic recombination as the PRIMARY productive "
            "mechanism, self-reported. The creativity atoms treat imagery as "
            "one input; for him it is the whole first stage."},
    {"id": "E-08", "subject": EINSTEIN,
     "name": "External-memory architecture type", "home": "CON-080", "h": "H5",
     "why": "persons-as-memory (Besso, Born, assistants) against Riemann's "
            "pages-as-memory. The platform should TYPE a subject's external "
            "cognition."},
    {"id": "E-09", "subject": EINSTEIN, "name": "Layered belief-gate",
     "home": "CON-030", "h": "H5",
     "why": "revision speed varies BY LAYER: instant at method, fast at theory, "
            "immovable at worldview. One brain, three clocks."},
    {"id": "E-10", "subject": EINSTEIN,
     "name": "Container-state DATING (platform upgrade)", "home": "platform-level",
     "h": "H5",
     "why": "his flexibility container is DOMINANT 1905-1915 and ANCHORED "
            "1926-1955. States need timestamps — a structural upgrade to the "
            "platform itself."},
    {"id": "X-01", "subject": "CROSS-SUBJECT",
     "name": "Weak container loops to strength", "home": "cross-subject law",
     "h": "H3",
     "why": "Riemann: lecture-fear -> posthumous textbooks. Einstein: late "
            "speech -> master aphorist. The weakest channel, run repeatedly at "
            "low stakes, ends among the strongest."},
    {"id": "X-02", "subject": "CROSS-SUBJECT",
     "name": "Institutions misread development", "home": "cross-subject law",
     "h": "H3",
     "why": "Riemann read as slow; Einstein failed an entrance exam and got no "
            "post for years. Both detonated on their own clock. THIRD SUBJECT "
            "NEEDED TO TEST."},
    {"id": "X-03", "subject": "CROSS-SUBJECT", "name": "Death as halt, not stop",
     "home": "cross-subject law", "h": "H4",
     "why": "Riemann dies mid-sentence on the ear; Einstein asks for the "
            "equations the day before dying. Both leave loops clean enough for "
            "others to continue — and others did."},
    {"id": "X-04", "subject": "CROSS-SUBJECT", "name": "Constraint-rise",
     "home": "cross-subject law", "h": "H3",
     "why": "Riemann rises under Gauss's imposed topic and the Berlin debt; "
            "Einstein under the Hilbert race and the Habicht promise. External "
            "binding lifts both; the fuel differs."},
)

# ---------------------------------------------------------------------------
# THE 14 HALTS — asked of him in those files and NEVER ANSWERED.
# ---------------------------------------------------------------------------

HALTS = (
    {"id": "H-1", "subject": RIEMANN,
     "halt": "Why did he withdraw the 1858 electrodynamics paper? No "
             "self-witness exists.",
     "yours": "how to log an unwitnessed reason"},
    {"id": "H-2", "subject": RIEMANN,
     "halt": "The faith rows. His piety refuses instrumentalizing God, yet his "
             "connection-programme resonates with it. Two witnesses inside the "
             "same man differ.",
     "yours": "does the platform treat a subject's own self-refusal as final"},
    {"id": "H-3", "subject": RIEMANN,
     "halt": "Numbering: R-01..R-11 proposed, but 2561-2590 are already spent "
             "in the King runs. Collision risk.",
     "yours": "assign numbers or keep the R- prefix"},
    {"id": "H-4", "subject": RIEMANN,
     "halt": "Containers with no self-witness. His letters survive mainly "
             "inside Dedekind's biography (carrier).",
     "yours": "confirm the (carrier) rule"},
    {"id": "H-5", "subject": RIEMANN,
     "halt": "Split verdict on witness necessity: his geometry proves intrinsic "
             "self-measurement for space; his life practices external witness "
             "for mind.",
     "yours": "rule whether the law is scoped to minds only"},
    {"id": "H-6", "subject": RIEMANN,
     "halt": "Anti-pleasing tally: AGREES 15 / CONDITIONAL 13 / DIFFERS 10 / "
             "REJECTS 3 / NO-VERDICT 4. Disagreement mass 17 of 45.",
     "yours": "accept the tally or strike rows"},
    {"id": "H-7", "subject": RIEMANN,
     "halt": "This workbook reads a man from his remains. He would stamp it "
             "hypothesis and demand two witnesses on every row.",
     "yours": "the standing you give it"},
    {"id": "E-1", "subject": EINSTEIN,
     "halt": "The faceting rule behind the 2,560 expansion. Strike the rule and "
             "every [PROPOSED] atom falls with it.",
     "yours": "approve / amend / strike the rule"},
    {"id": "E-2", "subject": EINSTEIN,
     "halt": "Depth into the private family record (Eduard, the marriages). I "
             "kept to his own published self-witness and marked the rest thin.",
     "yours": "how deep the platform goes into a subject's private life"},
    {"id": "E-3", "subject": EINSTEIN,
     "halt": "His causal-realism was ruled against by Bell tests decades after "
             "his death. May the verdict column overrule the subject with "
             "evidence he never saw?",
     "yours": "grade a dead man's conviction by later data, or freeze it"},
    {"id": "E-4", "subject": EINSTEIN,
     "halt": "The Riemann workbook still carries bare counts; the granularity "
             "rule arrived after it.",
     "yours": "refit Riemann now or later"},
    {"id": "E-5", "subject": EINSTEIN,
     "halt": "E-01..E-10 and X-01..X-04 await registry numbers.",
     "yours": "assign them"},
    {"id": "E-6", "subject": EINSTEIN,
     "halt": "THE AUDIT DIRECTION. His ruling is words-then-work. Einstein's "
             "instruction inverts it: 'don't listen to their words, fix your "
             "attention on their deeds.' On Einstein both agreed; the platform "
             "needs a standing rule for subjects where they diverge.",
     "yours": "which direction governs when they disagree"},
    {"id": "E-7", "subject": EINSTEIN,
     "halt": "The 45-item re-run through Einstein's brain, held pending his "
             "decide.",
     "yours": "order it or close it"},
)

# The Riemann 45-item re-run tally, as the workbook computed it.
RERUN_TALLY = {"AGREES": 15, "CONDITIONAL": 13, "DIFFERS": 10, "REJECTS": 3,
               "NO-VERDICT": 4}


def rerun_tally() -> dict:
    t = dict(RERUN_TALLY)
    total = sum(t.values())
    disagreement = t["DIFFERS"] + t["REJECTS"] + t["NO-VERDICT"]
    return {
        "tally": t, "total": total,
        "disagreement_mass": disagreement,
        "anti_pleasing_check": disagreement > 0,
        "his_test": "if DIFFERS+REJECTS+NO-VERDICT were 0, this workbook would "
                    "be flattery and should be thrown away.",
        "result": "%d of %d rows disagree with the template" % (disagreement,
                                                                total),
    }


def version_gap() -> dict:
    """Two versions of the bank, not one bank in two files."""
    return {
        "workbooks_built_on": BUILT_ON,
        "registry_now": CURRENT_BANK,
        "difference": CURRENT_BANK - BUILT_ON,
        "names_differ": True,
        "example": {"workbook": "Temperature balance",
                    "registry": "Core temperature setpoint"},
        "his_own_warning_in_the_file":
            "the owner's own corpus already assigned 2561-2590 in the King-brain "
            "runs. Assigning registry numbers is the owner's call.",
        "so": "the 25 candidates are CANDIDATE rows, never PARAM rows, and "
              "nothing is renumbered into his flat index.",
        "rule": "do not silently merge namespaces",
        "merged": False,
    }


def candidates_for(subject: str = "") -> list:
    if not subject:
        return list(CANDIDATES)
    return [c for c in CANDIDATES if c["subject"] == subject]


def open_halts() -> list:
    """All 14, and every one of them is still open."""
    return [dict(h, answered=False,
                 status="OPEN — asked of him and never answered") for h in HALTS]


def grow(root: str) -> dict:
    """Append the candidates and the halts. Appends only; no parameter created."""
    from . import growth as G
    have = {(r.get("kind"), r.get("name")) for r in G.load(root)}
    added = []
    for c in CANDIDATES:
        nm = "%s %s" % (c["id"], c["name"])
        if (G.CANDIDATE, nm) in have:
            continue
        added.append(G.add(root, G.CANDIDATE, nm,
                           surfaced_by="%s (my own earlier build, handed back)"
                                       % c["subject"],
                           module="subjectbrains", detail=c["why"],
                           extra={"proposed_home": c["home"], "evidence_h": c["h"],
                                  "subject": c["subject"],
                                  "is_parameter": False,
                                  "built_on_bank": BUILT_ON}))
    for h in HALTS:
        nm = "%s %s" % (h["id"], h["halt"][:70])
        if (G.HALT, nm) in have:
            continue
        added.append(G.add(root, G.HALT, nm,
                           surfaced_by=h["subject"], module="subjectbrains",
                           detail="YOURS: " + h["yours"],
                           extra={"answered": False, "subject": h["subject"]}))
    return {"added": len(added), "rows": added, "counts": G.counts(root),
            "parameters_created": 0,
            "law": "a candidate is not a parameter, and a halt is not a decision."}


def stats() -> dict:
    return {
        "subjects": 2,
        "candidates": len(CANDIDATES),
        "riemann_candidates": len(candidates_for(RIEMANN)),
        "einstein_candidates": len(candidates_for(EINSTEIN)),
        "cross_subject_candidates": len(candidates_for("CROSS-SUBJECT")),
        "halts_open": len(HALTS),
        "halts_answered": 0,
        "parameters_created": 0,
        "version_gap": version_gap(),
        "rerun": rerun_tally(),
        "source": "docs/method/canon/THE_SUBJECT_BRAINS.md",
    }


def annotations() -> list:
    return [
        ("his platform superimposed on a real person",
         "subjectbrains.CANDIDATES"),
        ("25 parameter candidates from two subjects",
         "subjectbrains.candidates_for"),
        ("14 halts asked of him and never answered",
         "subjectbrains.open_halts"),
        ("two versions of the bank, never merged", "subjectbrains.version_gap"),
        ("the anti-pleasing tally he demanded", "subjectbrains.rerun_tally"),
    ]
