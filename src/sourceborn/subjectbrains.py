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

# ---------------------------------------------------------------------------
# MORE SUBJECTS — his order: "add more subjects to test cross patterns".
#
# X-02 already carried its own condition: THIRD SUBJECT NEEDED TO TEST. And two
# subjects cannot test a cross-subject law, because the two he has are the same
# TYPE — European, male, theoretical, working mostly alone, dying with the work
# open. A law drawn from those two risks being a law about that type.
#
# So these four are chosen to STRESS the axes, not to agree with them. Each is
# picked because a named law plausibly FAILS on it:
#
#   Ramanujan  no institution and no proofs — his weak channel (rigour) never
#              became a strength, which is what X-01 claims happens
#   Curie      a PARTNERSHIP and an experimentalist — breaks the lone-theorist
#              shape both existing subjects share
#   Faraday    no mathematics ever, continuous release, and he STOPPED WORKING
#              YEARS BEFORE HE DIED — the clean counterexample to X-03
#   Turing     institutions read him correctly and then destroyed him — a
#              category X-02 does not have
#
# Every reading is a READING, at his evidence ladder, and correctable. The axis
# fields are what the law tests read; strike a field and the verdict moves.
# ---------------------------------------------------------------------------

# axis vocabularies — kept small so a verdict is checkable
MISREAD = "MISREAD"                  # institution read the person wrong
READ_CORRECTLY = "READ_CORRECTLY"
USED_THEN_DESTROYED = "USED_THEN_DESTROYED"   # neither of the above

WORKING_AT_DEATH = "WORKING_AT_DEATH"
STOPPED_BEFORE_DEATH = "STOPPED_BEFORE_DEATH"

ROSE = "ROSE"
FELL = "FELL"
FLAT = "FLAT"

GATE = "GATE"                # finishes and withholds (Riemann)
ITERATE = "ITERATE"          # publishes wrong, self-strikes (Einstein)
CONTINUOUS = "CONTINUOUS"    # releases as he goes, no gate and no strike
UNGATED = "UNGATED"          # sends unfinished/unproven freely

SUBJECTS = (
    {"id": "S-01", "name": "Bernhard Riemann", "years": "1826-1866",
     "field": "mathematics", "from_workbook": True,
     "weak_channel": "lecturing / speaking in public",
     "weak_became_strength": True,
     "weak_note": "lecture-fear -> the posthumous lectures became textbooks",
     "institution": MISREAD,
     "institution_note": "read as slow; poverty and shyness taken for capacity",
     "at_death": WORKING_AT_DEATH,
     "death_note": "dies mid-sentence on the mechanics of the ear",
     "loops_continuable": True,
     "constraint": ROSE,
     "constraint_note": "Gauss's imposed habilitation topic; the Berlin debt",
     "release": GATE, "external_memory": "pages (the Nachlass)",
     "worked_with": "alone", "h": "H5"},
    {"id": "S-02", "name": "Albert Einstein", "years": "1879-1955",
     "field": "physics", "from_workbook": True,
     "weak_channel": "speech (late talker) / people-machinery",
     "weak_became_strength": True,
     "weak_note": "late speech -> master aphorist",
     "institution": MISREAD,
     "institution_note": "failed an entrance exam; no academic post for years",
     "at_death": WORKING_AT_DEATH,
     "death_note": "asks for the unified-field notes the day before dying",
     "loops_continuable": True,
     "constraint": ROSE,
     "constraint_note": "the Hilbert race; the Habicht promise",
     "release": ITERATE, "external_memory": "persons (Besso, Born, assistants)",
     "worked_with": "alone, with named sounding-boards", "h": "H5"},
    {"id": "S-03", "name": "Srinivasa Ramanujan", "years": "1887-1920",
     "field": "mathematics", "from_workbook": False,
     "weak_channel": "formal proof and rigour — never trained in it",
     "weak_became_strength": False,
     "weak_note": "IT NEVER BECAME A STRENGTH. He produced results without "
                  "proofs and Hardy had to supply the rigour; the gap stayed a "
                  "gap for life. This is the counterexample X-01 needed.",
     "institution": MISREAD,
     "institution_note": "lost his scholarship and failed college twice on "
                         "non-mathematical subjects; worked as a port clerk",
     "at_death": WORKING_AT_DEATH,
     "death_note": "dead at 32; the 'lost notebook' surfaced in 1976 and is "
                   "still being worked through",
     "loops_continuable": True,
     "constraint": ROSE,
     "constraint_note": "Hardy's binding at Cambridge produced his most "
                        "rigorous work",
     "release": UNGATED, "external_memory": "pages (the notebooks)",
     "worked_with": "alone, then one collaborator", "h": "H4"},
    {"id": "S-04", "name": "Marie Curie", "years": "1867-1934",
     "field": "physics and chemistry", "from_workbook": False,
     "weak_channel": "institutional access (barred from Polish universities)",
     "weak_became_strength": False,
     "weak_note": "access was removed, not converted. She routed around it via "
                  "the clandestine Flying University and then Paris; the "
                  "channel itself never became a strength.",
     "institution": MISREAD,
     "institution_note": "excluded from university in Poland by sex; rejected "
                         "by the French Academy of Sciences in 1911",
     "at_death": WORKING_AT_DEATH,
     "death_note": "died of aplastic anaemia from her own materials; her "
                   "institute ran on and her daughter continued the work",
     "loops_continuable": True,
     "constraint": ROSE,
     "constraint_note": "poverty, exclusion, and a shed for a laboratory",
     "release": CONTINUOUS, "external_memory": "apparatus and a co-worker",
     "worked_with": "PARTNERSHIP (Pierre) — breaks the lone-theorist shape",
     "h": "H4"},
    {"id": "S-05", "name": "Michael Faraday", "years": "1791-1867",
     "field": "physics and chemistry", "from_workbook": False,
     "weak_channel": "mathematics — he never had it",
     "weak_became_strength": False,
     "weak_note": "ROUTED AROUND, NOT CONVERTED. He reached the field concept "
                  "by visual reasoning and Maxwell supplied the mathematics "
                  "afterwards. The weak channel stayed weak to the end.",
     "institution": READ_CORRECTLY,
     "institution_note": "an apprentice bookbinder with no formal education, "
                         "but Davy took him into the Royal Institution at 21 "
                         "and it held him for life. NOT a misreading.",
     "at_death": STOPPED_BEFORE_DEATH,
     "death_note": "his memory and powers declined from the mid-1850s and he "
                   "gave up experimental work years before dying in 1867. THE "
                   "CLEAN COUNTEREXAMPLE TO X-03.",
     "loops_continuable": True,
     "constraint": ROSE,
     "constraint_note": "Davy's binding; the Royal Institution's lecture duties",
     "release": CONTINUOUS,
     "external_memory": "a numbered lifelong laboratory diary",
     "worked_with": "alone, with an assistant", "h": "H4"},
    {"id": "S-06", "name": "Alan Turing", "years": "1912-1954",
     "field": "mathematics and computing", "from_workbook": False,
     "weak_channel": "institutional and social navigation",
     "weak_became_strength": False,
     "weak_note": "never converted; it is what destroyed him.",
     "institution": USED_THEN_DESTROYED,
     "institution_note": "Cambridge and Bletchley used him accurately and at "
                         "full stretch; the state then prosecuted him in 1952 "
                         "and he was dead by 1954. NEITHER misread NOR read "
                         "correctly — a third category X-02 does not have.",
     "at_death": WORKING_AT_DEATH,
     "death_note": "dead at 41 with morphogenesis work in progress; the 1936 "
                   "and 1950 papers were already public and others carried them",
     "loops_continuable": True,
     "constraint": ROSE,
     "constraint_note": "the wartime binding at Bletchley produced his most "
                        "consequential work",
     "release": CONTINUOUS, "external_memory": "pages and machines",
     "worked_with": "teams (Bletchley) — the second break from lone work",
     "h": "H4"},
)

HOLDS = "HOLDS"
FAILS = "FAILS"
UNKNOWN = "UNKNOWN"

# Each law says WHICH field decides it, so a verdict is computed and a struck
# field moves it. The falsifier is what a FAIL means, in his terms.
CROSS_LAWS = (
    {"id": "X-01", "name": "Weak container loops to strength",
     "reads": "weak_became_strength",
     "holds_when": "the weakest channel ends among the strongest",
     "falsifier": "a subject whose weakest channel stays weak or is routed "
                  "around instead of converted"},
    {"id": "X-02", "name": "Institutions misread development",
     "reads": "institution",
     "holds_when": "the institution read the person wrong",
     "falsifier": "a subject an institution read correctly — or one it read "
                  "correctly and then destroyed, which the law has no word for"},
    {"id": "X-03", "name": "Death as halt, not stop",
     "reads": "at_death",
     "holds_when": "the work is still moving when the person stops",
     "falsifier": "a subject who stopped working well before dying"},
    {"id": "X-04", "name": "Constraint-rise",
     "reads": "constraint",
     "holds_when": "external binding lifts performance",
     "falsifier": "a subject whose performance fell under imposed constraint"},
)


def _verdict(law: dict, subj: dict) -> dict:
    """Read one law on one subject FROM THE FIELDS. Never typed per-pair."""
    f = law["reads"]
    v = subj.get(f)
    if v is None:
        return {"verdict": UNKNOWN, "why": "the axis is not read for this subject"}
    if f == "weak_became_strength":
        return {"verdict": HOLDS if v else FAILS,
                "why": subj.get("weak_note", "")}
    if f == "institution":
        if v == MISREAD:
            return {"verdict": HOLDS, "why": subj.get("institution_note", "")}
        return {"verdict": FAILS, "why": subj.get("institution_note", ""),
                "new_category": v if v == USED_THEN_DESTROYED else None}
    if f == "at_death":
        return {"verdict": HOLDS if v == WORKING_AT_DEATH else FAILS,
                "why": subj.get("death_note", "")}
    if f == "constraint":
        return {"verdict": HOLDS if v == ROSE else FAILS,
                "why": subj.get("constraint_note", "")}
    return {"verdict": UNKNOWN, "why": "no reader for this axis"}


def cross_test(law_id: str = "") -> dict:
    """Test the cross-subject laws against every subject.

    A law is not graded on how often it holds. His discipline is the survivor
    stage: **one clean counterexample falsifies the law as stated.** A law with a
    FAIL comes back KILLED AS STATED, with the subject that killed it named, and
    what it would have to be narrowed to in order to survive. Nothing is deleted."""
    laws = [l for l in CROSS_LAWS if not law_id or l["id"] == law_id]
    out = []
    for law in laws:
        rows = []
        for s in SUBJECTS:
            v = _verdict(law, s)
            rows.append({"subject": s["id"], "name": s["name"],
                         "verdict": v["verdict"], "why": v["why"],
                         "new_category": v.get("new_category"),
                         "h": s["h"], "from_workbook": s["from_workbook"]})
        holds = [r for r in rows if r["verdict"] == HOLDS]
        fails = [r for r in rows if r["verdict"] == FAILS]
        unknown = [r for r in rows if r["verdict"] == UNKNOWN]
        newcat = sorted({r["new_category"] for r in rows if r["new_category"]})
        out.append({
            "law": law["id"], "name": law["name"],
            "holds_when": law["holds_when"],
            "falsifier": law["falsifier"],
            "rows": rows,
            "counts": {"subjects": len(rows), "holds": len(holds),
                       "fails": len(fails), "unknown": len(unknown)},
            "killed_as_stated": bool(fails),
            "killed_by": [r["name"] for r in fails],
            "status": ("KILLED AS STATED — %s" % ", ".join(r["name"]
                                                           for r in fails))
                      if fails else
                      ("SURVIVES %d of %d, untested elsewhere"
                       % (len(holds), len(rows))),
            "needs_a_new_category": newcat,
            "narrow_to": ("holds on %s and fails on %s — it is a law about a "
                          "TYPE of subject, not about subjects"
                          % (", ".join(r["name"] for r in holds) or "none",
                             ", ".join(r["name"] for r in fails)))
                         if fails and holds else None,
            "deleted": 0,
        })
    survived = [o for o in out if not o["killed_as_stated"]]
    return {
        "subjects": len(SUBJECTS),
        "new_subjects": sum(1 for s in SUBJECTS if not s["from_workbook"]),
        "laws_tested": len(out),
        "laws": out,
        "survived": [o["law"] for o in survived],
        "killed_as_stated": [o["law"] for o in out if o["killed_as_stated"]],
        "law": "one clean counterexample falsifies a cross-subject law as stated. "
               "Holding on most subjects is not holding.",
        "refuses": "the new subjects were chosen to STRESS these laws, not to "
                   "agree with them. A law that survives a stress set has earned "
                   "something; a law that survives a set picked to flatter it has "
                   "not.",
        "nothing_deleted": True,
        "his_call": "narrowing a killed law, or striking it, is his — not mine.",
    }


def release_poles() -> dict:
    """E-03 said ONE AXIS, TWO POLES. Six subjects show four."""
    by = {}
    for s in SUBJECTS:
        by.setdefault(s["release"], []).append(s["name"])
    return {
        "poles_in_his_candidate": [GATE, ITERATE],
        "poles_found": sorted(by),
        "by_pole": by,
        "his_candidate_was": "E-03 Release polarity — one axis, two poles "
                             "(Riemann's gate against Einstein's self-strike)",
        "finding": "the axis needs at least four settings, not two: %s"
                   % ", ".join(sorted(by)),
        "note": "CONTINUOUS (Faraday, Curie, Turing) is neither a gate nor a "
                "self-strike, and UNGATED (Ramanujan) sends unproven work "
                "freely. Reported as an amendment to his own candidate, not "
                "applied to it.",
    }


def lone_worker_check() -> dict:
    """Both workbook subjects worked essentially alone. Does the shape hold?"""
    modes = {}
    for s in SUBJECTS:
        modes.setdefault(s["worked_with"], []).append(s["name"])
    solo = [s["name"] for s in SUBJECTS if s["worked_with"].startswith("alone")]
    return {
        "by_mode": modes,
        "alone": solo,
        "not_alone": [s["name"] for s in SUBJECTS
                      if not s["worked_with"].startswith("alone")],
        "finding": "the two workbook subjects are both lone theorists, so every "
                   "law drawn from them alone was at risk of being a law about "
                   "lone theorists. Curie worked in a partnership and Turing in "
                   "teams; both still show constraint-rise, which is evidence "
                   "X-04 is not an artefact of solitude.",
    }


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
    ct = cross_test()
    return {
        "subjects": len(SUBJECTS),
        "subjects_from_workbooks": sum(1 for s in SUBJECTS if s["from_workbook"]),
        "subjects_added_to_test": ct["new_subjects"],
        "cross_laws": len(CROSS_LAWS),
        "cross_laws_survived": ct["survived"],
        "cross_laws_killed_as_stated": ct["killed_as_stated"],
        "release_poles_found": len(release_poles()["poles_found"]),
        "release_poles_he_named": 2,
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
