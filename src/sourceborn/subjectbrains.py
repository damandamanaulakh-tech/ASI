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

SINGLE = "SINGLE"            # one release in a lifetime
USED_WITHOUT_CREDIT = "USED_WITHOUT_CREDIT"   # a fourth institution setting
TAKEN_NOT_HANDED = "TAKEN_NOT_HANDED"         # loops continued without consent

# What a candidate READS. Application is computed from these fields; a candidate
# with no field for a subject is reported NOT READ, never invented.
NOT_READ = "NOT READ"

CANDIDATE_AXIS = {
    "R-01": "release", "R-02": "external_memory", "R-05": "loops_continuable",
    "R-06": "claim_vs_evidence", "R-07": "constraint", "R-10": "ambition_public",
    "E-01": "trigger_kind", "E-02": "held_against_consensus", "E-03": "release",
    "E-04": "delivery_cipher", "E-05": "fame", "E-07": "first_stage",
    "E-08": "external_memory",
    "X-01": "weak_became_strength", "X-02": "institution", "X-03": "at_death",
    "X-04": "constraint",
}

SUBJECTS = (
    {"id": "S-01", "name": "Bernhard Riemann", "years": "1826-1866",
     "field": "mathematics", "from_workbook": True, "h": "H5",
     "weak_channel": "lecturing in public", "weak_became_strength": True,
     "weak_note": "lecture-fear -> the posthumous lectures became textbooks",
     "institution": MISREAD,
     "institution_note": "read as slow; poverty and shyness taken for capacity",
     "at_death": WORKING_AT_DEATH,
     "death_note": "dies mid-sentence on the mechanics of the ear",
     "loops_continuable": True, "constraint": ROSE,
     "constraint_note": "Gauss's imposed habilitation topic; the Berlin debt",
     "release": GATE, "external_memory": "pages",
     "claim_vs_evidence": "UNDER", "ambition_public": "PRIVATE",
     "trigger_kind": "THE PRESUPPOSED", "held_against_consensus": False,
     "delivery_cipher": "UNDERSTATEMENT", "fame": "POSTHUMOUS",
     "first_stage": "GEOMETRIC IMAGE",
     "worked_with": "alone"},
    {"id": "S-02", "name": "Albert Einstein", "years": "1879-1955",
     "field": "physics", "from_workbook": True, "h": "H5",
     "weak_channel": "speech / people-machinery", "weak_became_strength": True,
     "weak_note": "late speech -> master aphorist",
     "institution": MISREAD,
     "institution_note": "failed an entrance exam; no academic post for years",
     "at_death": WORKING_AT_DEATH,
     "death_note": "asks for the unified-field notes the day before dying",
     "loops_continuable": True, "constraint": ROSE,
     "constraint_note": "the Hilbert race; the Habicht promise",
     "release": ITERATE, "external_memory": "persons",
     "claim_vs_evidence": "LEVEL", "ambition_public": "PUBLIC",
     "trigger_kind": "UGLINESS", "held_against_consensus": True,
     "delivery_cipher": "HUMOUR", "fame": "ARRIVED UNSOUGHT",
     "first_stage": "IMAGE",
     "worked_with": "alone, with named sounding-boards"},
    {"id": "S-03", "name": "Srinivasa Ramanujan", "years": "1887-1920",
     "field": "mathematics", "from_workbook": False, "h": "H4",
     "weak_channel": "formal proof and rigour", "weak_became_strength": False,
     "weak_note": "never became a strength — Hardy supplied the rigour and the "
                  "gap stayed a gap for life",
     "institution": MISREAD,
     "institution_note": "lost his scholarship, failed college twice on "
                         "non-mathematical subjects, worked as a port clerk",
     "at_death": WORKING_AT_DEATH,
     "death_note": "dead at 32; the 'lost notebook' surfaced in 1976 and is "
                   "still being worked through",
     "loops_continuable": True, "constraint": ROSE,
     "constraint_note": "Hardy's binding at Cambridge produced his most "
                        "rigorous work",
     "release": UNGATED, "external_memory": "pages",
     "claim_vs_evidence": "OVER", "ambition_public": "PRIVATE",
     "trigger_kind": "PATTERN", "held_against_consensus": False,
     "delivery_cipher": "NONE", "fame": "ARRIVED UNSOUGHT",
     "first_stage": "NUMBER",
     "worked_with": "alone, then one collaborator"},
    {"id": "S-04", "name": "Marie Curie", "years": "1867-1934",
     "field": "physics and chemistry", "from_workbook": False, "h": "H4",
     "weak_channel": "institutional access", "weak_became_strength": False,
     "weak_note": "access was routed around via the clandestine Flying "
                  "University, never converted",
     "institution": MISREAD,
     "institution_note": "barred from university in Poland by sex; rejected by "
                         "the French Academy of Sciences in 1911",
     "at_death": WORKING_AT_DEATH,
     "death_note": "died of aplastic anaemia from her own materials; her "
                   "institute ran on and her daughter continued the work",
     "loops_continuable": True, "constraint": ROSE,
     "constraint_note": "poverty, exclusion, and a shed for a laboratory",
     "release": CONTINUOUS, "external_memory": "apparatus",
     "claim_vs_evidence": "UNDER", "ambition_public": "PRIVATE",
     "trigger_kind": "AN ANOMALOUS MEASUREMENT",
     "held_against_consensus": True,
     "delivery_cipher": "NONE", "fame": "ARRIVED UNSOUGHT",
     "first_stage": "MEASUREMENT",
     "worked_with": "PARTNERSHIP (Pierre)"},
    {"id": "S-05", "name": "Michael Faraday", "years": "1791-1867",
     "field": "physics and chemistry", "from_workbook": False, "h": "H4",
     "weak_channel": "mathematics", "weak_became_strength": False,
     "weak_note": "routed around, not converted — he reached the field concept "
                  "visually and Maxwell supplied the mathematics after",
     "institution": READ_CORRECTLY,
     "institution_note": "an apprentice bookbinder with no formal education, but "
                         "Davy took him into the Royal Institution at 21 and it "
                         "held him for life",
     "at_death": STOPPED_BEFORE_DEATH,
     "death_note": "memory and powers declined from the mid-1850s; he gave up "
                   "experimental work years before dying in 1867",
     "loops_continuable": True, "constraint": ROSE,
     "constraint_note": "Davy's binding; the Royal Institution's lecture duties",
     "release": CONTINUOUS, "external_memory": "pages",
     "claim_vs_evidence": "UNDER", "ambition_public": "PRIVATE",
     "trigger_kind": "AN UNEXPLAINED EFFECT", "held_against_consensus": True,
     "delivery_cipher": "NONE", "fame": "ARRIVED UNSOUGHT",
     "first_stage": "IMAGE",
     "worked_with": "alone, with an assistant"},
    {"id": "S-06", "name": "Alan Turing", "years": "1912-1954",
     "field": "mathematics and computing", "from_workbook": False, "h": "H4",
     "weak_channel": "institutional and social navigation",
     "weak_became_strength": False,
     "weak_note": "never converted; it is what destroyed him",
     "institution": USED_THEN_DESTROYED,
     "institution_note": "Cambridge and Bletchley used him accurately and at "
                         "full stretch; the state prosecuted him in 1952 and he "
                         "was dead by 1954",
     "at_death": WORKING_AT_DEATH,
     "death_note": "dead at 41 with morphogenesis work in progress; the 1936 and "
                   "1950 papers were already public and others carried them",
     "loops_continuable": True, "constraint": ROSE,
     "constraint_note": "the wartime binding at Bletchley produced his most "
                        "consequential work",
     "release": CONTINUOUS, "external_memory": "pages and machines",
     "claim_vs_evidence": "LEVEL", "ambition_public": "PRIVATE",
     "trigger_kind": "A FORMAL QUESTION", "held_against_consensus": True,
     "delivery_cipher": "NONE", "fame": "POSTHUMOUS",
     "first_stage": "MECHANISM",
     "worked_with": "teams (Bletchley)"},
    {"id": "S-07", "name": "Nikola Tesla", "years": "1856-1943",
     "field": "electrical engineering", "from_workbook": False, "h": "H3",
     "weak_channel": "money and business", "weak_became_strength": False,
     "weak_note": "never converted — he died in a hotel room in debt",
     "institution": MISREAD,
     "institution_note": "left Edison, lost backing repeatedly, ended without an "
                         "institution at all",
     "at_death": WORKING_AT_DEATH,
     "death_note": "still announcing work at the end; his papers were seized "
                   "after his death",
     "loops_continuable": True, "constraint": ROSE,
     "constraint_note": "under Westinghouse's binding he delivered the AC system",
     "release": CONTINUOUS, "external_memory": "apparatus",
     "claim_vs_evidence": "OVER",
     "claim_note": "announced work he never demonstrated — the OVER pole his "
                   "understatement candidate has no room for",
     "ambition_public": "PUBLIC", "trigger_kind": "A MACHINE SEEN WHOLE",
     "held_against_consensus": True, "delivery_cipher": "SPECTACLE",
     "fame": "SOUGHT", "first_stage": "IMAGE",
     "worked_with": "alone, with backers"},
    {"id": "S-08", "name": "Ada Lovelace", "years": "1815-1852",
     "field": "mathematics and computing", "from_workbook": False, "h": "H3",
     "weak_channel": "position — no post was possible for her",
     "weak_became_strength": False,
     "weak_note": "routed around through a translator's notes, not converted",
     "institution": MISREAD,
     "institution_note": "no institutional position was available to her at all; "
                         "she published under initials",
     "at_death": STOPPED_BEFORE_DEATH,
     "death_note": "ill through her final year, dead at 36",
     "loops_continuable": True, "constraint": ROSE,
     "constraint_note": "the commissioned translation was the binding that "
                        "produced the Notes",
     "release": SINGLE,
     "release_note": "ONE release in a lifetime — a setting neither his gate nor "
                     "his iterate can hold",
     "external_memory": "pages", "claim_vs_evidence": "UNDER",
     "ambition_public": "PRIVATE", "trigger_kind": "A MACHINE'S LIMIT",
     "held_against_consensus": False, "delivery_cipher": "UNDERSTATEMENT",
     "fame": "POSTHUMOUS", "first_stage": "SYMBOL",
     "worked_with": "one collaborator"},
    {"id": "S-09", "name": "Ludwig van Beethoven", "years": "1770-1827",
     "field": "music — NOT a science", "from_workbook": False, "h": "H4",
     "weak_channel": "hearing", "weak_became_strength": True,
     "weak_note": "deafness, and the late works composed inside it are the ones "
                  "held highest. The strongest case FOR X-01 and it comes from "
                  "outside science entirely.",
     "institution": READ_CORRECTLY,
     "institution_note": "patrons supported him early; recognised in his lifetime",
     "at_death": WORKING_AT_DEATH,
     "death_note": "the late quartets were his last work; he died in 1827 with "
                   "the form still moving",
     "loops_continuable": True, "constraint": ROSE,
     "constraint_note": "commissions bound him and he rose under them",
     "release": CONTINUOUS, "external_memory": "pages (the sketchbooks)",
     "claim_vs_evidence": "LEVEL", "ambition_public": "PUBLIC",
     "trigger_kind": "A FORM THAT WILL NOT CLOSE",
     "held_against_consensus": True,
     "cipher_note": "the late quartets were called incomprehensible and he did "
                    "not bend",
     "delivery_cipher": "NONE", "fame": "ARRIVED SOUGHT",
     "first_stage": "SOUND",
     "worked_with": "alone, with copyists"},
    {"id": "S-10", "name": "Vincent van Gogh", "years": "1853-1890",
     "field": "painting — NOT a science", "from_workbook": False, "h": "H4",
     "weak_channel": "selling, and social standing",
     "weak_became_strength": False,
     "weak_note": "never converted — he sold almost nothing in his life",
     "institution": MISREAD,
     "institution_note": "no dealer, no academy, almost no sales in a decade of "
                         "work",
     "at_death": WORKING_AT_DEATH,
     "death_note": "painting until weeks before his death at 37",
     "loops_continuable": True, "constraint": ROSE,
     "constraint_note": "Theo's stipend was the binding that made the decade "
                        "possible",
     "release": CONTINUOUS, "external_memory": "persons (Theo, the letters)",
     "claim_vs_evidence": "UNDER", "ambition_public": "PRIVATE",
     "trigger_kind": "A COLOUR RELATION", "held_against_consensus": True,
     "delivery_cipher": "NONE", "fame": "POSTHUMOUS", "first_stage": "IMAGE",
     "worked_with": "alone, one witness by letter"},
    {"id": "S-11", "name": "Rosalind Franklin", "years": "1920-1958",
     "field": "chemistry and crystallography", "from_workbook": False, "h": "H4",
     "weak_channel": "control over her own data",
     "weak_became_strength": False,
     "weak_note": "never converted — the data moved without her consent",
     "institution": USED_WITHOUT_CREDIT,
     "institution_note": "her measurements were used without her agreement and "
                         "the credit went elsewhere. A FOURTH institution "
                         "setting: not misread, not read correctly, not used "
                         "then destroyed — used and uncredited.",
     "at_death": WORKING_AT_DEATH,
     "death_note": "working on virus structure until weeks before dying at 37",
     "loops_continuable": True,
     "successor": TAKEN_NOT_HANDED,
     "successor_note": "the loop WAS continued — but taken, not handed. His R-05 "
                       "successor-loop candidate assumes the handing.",
     "constraint": ROSE,
     "constraint_note": "rose under the demands of the technique itself",
     "release": GATE,
     "release_note": "she withheld until the evidence was sufficient — the same "
                     "pole as Riemann, and it cost her the claim",
     "external_memory": "pages and photographic plates",
     "claim_vs_evidence": "UNDER", "ambition_public": "PRIVATE",
     "trigger_kind": "AN IMAGE THAT DOES NOT RESOLVE",
     "held_against_consensus": True, "delivery_cipher": "NONE",
     "fame": "POSTHUMOUS", "first_stage": "IMAGE",
     "worked_with": "a laboratory, badly"},
    {"id": "S-12", "name": "Emmy Noether", "years": "1882-1935",
     "field": "mathematics", "from_workbook": False, "h": "H4",
     "weak_channel": "the right to hold a post",
     "weak_became_strength": False,
     "weak_note": "routed around — she lectured for years under another man's "
                  "name on the timetable",
     "institution": USED_WITHOUT_CREDIT,
     "institution_note": "unpaid and unlisted, lecturing under Hilbert's name; "
                         "later expelled outright",
     "at_death": WORKING_AT_DEATH,
     "death_note": "died suddenly after surgery at 53 with the school she "
                   "founded still running",
     "loops_continuable": True, "constraint": ROSE,
     "constraint_note": "rose under exclusion and then under exile",
     "release": CONTINUOUS,
     "external_memory": "persons (her students carried the ideas)",
     "claim_vs_evidence": "UNDER",
     "claim_note": "she gave results away and let others publish them",
     "ambition_public": "PRIVATE", "trigger_kind": "A STRUCTURE UNDER A RESULT",
     "held_against_consensus": False, "delivery_cipher": "NONE",
     "fame": "POSTHUMOUS", "first_stage": "STRUCTURE",
     "worked_with": "students"},
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


def cross_test(law_id: str = "", kill: bool = False) -> dict:
    """Test the cross-subject laws against every subject.

    HIS INSTRUCTION, AND IT REVERSES WHAT I HAD APPLIED:

        nothing needs to kill for now, add everything and generate

    So `kill` is OFF by default. A subject that reads differently is no longer a
    counterexample that ends the law — it is **another SETTING of it**, kept and
    named. That is his standing rule doing the work instead: keep adding, not
    removing. The killing pass is still here and still correct; it runs only when
    he asks for it (`kill=True`), and the earlier kill reading is preserved in
    canon rather than erased."""
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
        settings = {}
        for r in rows:
            settings.setdefault(r["verdict"], []).append(r["name"])
        out.append({
            "law": law["id"], "name": law["name"],
            "settings_found": sorted(settings),
            "by_setting": settings,
            "kept_alive": not kill,
            "holds_when": law["holds_when"],
            "falsifier": law["falsifier"],
            "rows": rows,
            "counts": {"subjects": len(rows), "holds": len(holds),
                       "fails": len(fails), "unknown": len(unknown)},
            "killed_as_stated": bool(fails) and kill,
            "killed_by": [r["name"] for r in fails] if kill else [],
            "status": (("KILLED AS STATED — %s" % ", ".join(r["name"]
                                                            for r in fails))
                       if fails else
                       ("SURVIVES %d of %d, untested elsewhere"
                        % (len(holds), len(rows))))
                      if kill else
                      ("ALIVE — %d hold, %d read the other way, and the other "
                       "way is kept as a second setting rather than a kill"
                       % (len(holds), len(fails))),
            "needs_a_new_category": newcat,
            "narrow_to": ("holds on %s and reads the other way on %s"
                          % (", ".join(r["name"] for r in holds) or "none",
                             ", ".join(r["name"] for r in fails)))
                         if fails and holds else None,
            "deleted": 0,
        })
    survived = [o for o in out if not o["killed_as_stated"]]
    return {
        "kill": kill,
        "his_instruction": "nothing needs to kill for now, add everything and "
                           "generate",
        "subjects": len(SUBJECTS),
        "new_subjects": sum(1 for s in SUBJECTS if not s["from_workbook"]),
        "laws_tested": len(out),
        "laws": out,
        "survived": [o["law"] for o in survived],
        "killed_as_stated": [o["law"] for o in out if o["killed_as_stated"]],
        "law": ("one clean counterexample falsifies a cross-subject law as "
                "stated. Holding on most subjects is not holding." if kill else
                "a subject that reads the other way is a SECOND SETTING, not a "
                "death. Keep adding, not removing."),
        "refuses": "the added subjects were chosen to STRESS these laws, not to "
                   "agree with them — but on his word nothing is killed for now, "
                   "so a stress result becomes a setting instead of an ending.",
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
        "candidate_cells": len(CANDIDATES) * len(SUBJECTS),
        "variants_generated": generate_variants()["variants_generated"],
        "killed": 0,
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


# ---------------------------------------------------------------------------
# APPLY THE CANDIDATES — his order: "apply on candidates / nothing needs to kill
# for now, add everything and generate".
# ---------------------------------------------------------------------------

def apply_candidates(subjects=None) -> dict:
    """Every candidate read on every subject. 25 x 12.

    A candidate with no axis for a subject is reported NOT READ. That is an
    absence, not a zero and not a guess — the one thing this must never do is
    fill 300 cells by inventing them."""
    subs = list(subjects or SUBJECTS)
    grid, per_candidate = [], []
    for c in CANDIDATES:
        axis = CANDIDATE_AXIS.get(c["id"])
        cells = []
        for s in subs:
            if not axis:
                cells.append({"subject": s["id"], "name": s["name"],
                              "setting": NOT_READ,
                              "why": "no axis is read for this candidate yet"})
                continue
            v = s.get(axis, NOT_READ)
            if isinstance(v, bool):
                v = "YES" if v else "NO"
            cells.append({"subject": s["id"], "name": s["name"],
                          "axis": axis, "setting": str(v),
                          "note": s.get(axis.split("_")[0] + "_note", "")})
        read = [x for x in cells if x["setting"] != NOT_READ]
        settings = sorted({x["setting"] for x in read})
        grid.append({"candidate": c["id"], "name": c["name"], "axis": axis,
                     "cells": cells})
        per_candidate.append({
            "candidate": c["id"], "name": c["name"], "axis": axis,
            "read": len(read), "not_read": len(cells) - len(read),
            "settings": settings, "distinct_settings": len(settings),
            "is_an_axis": len(settings) > 1,
            "poles": {v: [x["name"] for x in read if x["setting"] == v]
                      for v in settings},
        })
    return {
        "candidates": len(CANDIDATES), "subjects": len(subs),
        "cells": len(CANDIDATES) * len(subs),
        "cells_read": sum(p["read"] for p in per_candidate),
        "cells_not_read": sum(p["not_read"] for p in per_candidate),
        "with_an_axis": sum(1 for p in per_candidate if p["axis"]),
        "without_an_axis": sum(1 for p in per_candidate if not p["axis"]),
        "became_an_axis": [p["candidate"] for p in per_candidate
                           if p["is_an_axis"]],
        "single_valued": [p["candidate"] for p in per_candidate
                          if p["axis"] and not p["is_an_axis"]],
        "per_candidate": per_candidate,
        "grid": grid,
        "law": "a candidate read across many subjects stops being a property and "
               "becomes an AXIS with named settings.",
        "refuses": "a candidate with no axis is NOT READ, never invented. 8 of "
                   "the 25 have no reader yet and say so.",
    }


def generate_variants(subjects=None) -> dict:
    """GENERATE. Every distinct setting of every candidate becomes a named
    variant — added, never chosen, never killed.

    This is his mechanic exactly: the candidate was one thing; read across
    subjects it becomes N things. Nothing is removed to make room for them."""
    ap = apply_candidates(subjects)
    variants = []
    for p in ap["per_candidate"]:
        if not p["axis"] or not p["settings"]:
            continue
        for v in p["settings"]:
            who = p["poles"][v]
            variants.append({
                "id": "%s::%s" % (p["candidate"], v.replace(" ", "_")),
                "from_candidate": p["candidate"],
                "candidate_name": p["name"],
                "axis": p["axis"],
                "setting": v,
                "subjects": who,
                "support": len(who),
                "new_to_his_candidate": p["distinct_settings"] > 1,
                "is_parameter": False,
                "canonical": False,
                "chosen": False,
            })
    by_cand = {}
    for v in variants:
        by_cand.setdefault(v["from_candidate"], 0)
        by_cand[v["from_candidate"]] += 1
    # An "axis" whose every setting has support 1 is not an axis — it is an
    # uncategorised free-text field wearing an axis's clothes. E-01 does this:
    # twelve subjects, twelve triggers, no two alike. Flagged, not hidden.
    singleton = []
    for p2 in ap["per_candidate"]:
        if not p2["axis"] or p2["distinct_settings"] < 2:
            continue
        if all(len(w) == 1 for w in p2["poles"].values()):
            singleton.append({"candidate": p2["candidate"], "name": p2["name"],
                              "settings": p2["distinct_settings"],
                              "why": "every subject is its own setting, so no "
                                     "category has formed yet — this reads as a "
                                     "free-text field, not an axis"})
    return {
        "candidates_in": ap["with_an_axis"],
        "variants_generated": len(variants),
        "variants": variants,
        "per_candidate": by_cand,
        "widest": sorted(by_cand.items(), key=lambda kv: -kv[1])[:6],
        "parameters_created": 0,
        "killed": 0,
        "not_yet_an_axis": singleton,
        "variants_from_singleton_fields": sum(x["settings"] for x in singleton),
        "law": "more subjects -> more settings -> more variants. Nothing is "
               "removed to make room.",
        "his_words": "nothing needs to kill for now, add everything and generate",
    }


def grow_variants(root: str) -> dict:
    """Append every generated variant. Appends only."""
    from . import growth as G
    have = {(r.get("kind"), r.get("name")) for r in G.load(root)}
    g = generate_variants()
    added = []
    for v in g["variants"]:
        nm = "%s — %s = %s" % (v["from_candidate"], v["axis"], v["setting"])
        if (G.CANDIDATE, nm) in have:
            continue
        added.append(G.add(root, G.CANDIDATE, nm,
                           surfaced_by="applied across %d subjects"
                                       % len(SUBJECTS),
                           module="subjectbrains",
                           detail="%s | held by: %s" % (v["candidate_name"],
                                                        ", ".join(v["subjects"])),
                           extra={"variant_of": v["from_candidate"],
                                  "axis": v["axis"], "setting": v["setting"],
                                  "support": v["support"],
                                  "is_parameter": False}))
    return {"added": len(added), "rows": added, "counts": G.counts(root),
            "parameters_created": 0, "killed": 0,
            "law": g["law"]}
