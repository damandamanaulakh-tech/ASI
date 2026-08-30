"""THE OPERATIONAL TRIGGER / STATE VECTOR — his third column.

His order, given with the table itself:

    6 - below more may be repated

and then ten segments, each a four-column table:

    | Master Container | Biological Sub-Parameter (Neurophysiology)
    | Engine Sub-Parameter (System Architecture)
    | Operational Trigger / State Vector |

WHAT THE THIRD COLUMN IS, AND WHY IT IS NOT A THIRD NAME

Until this module the architecture carried TWO columns at every node: the human
name he wrote and the computer parallel, because ASI is the verified Human<->AI
connection and one column alone cannot link. Both of those answer *what is
this*.

The Operational Trigger answers a different question entirely: **WHEN DOES IT
FIRE**. `Temp > T_max triggers cooling loop`. `Idle timer > Threshold triggers
ACPI S3/S4 state`. `Vector similarity search (Cosine similarity > 0.85)`.
A name is a noun; a trigger is a **condition**, and a condition can be evaluated
where a noun can only be read.

That is what makes it a state vector rather than a label: it names the
measurement, the threshold and what happens at the crossing. His own spine
already says a threshold lives on an EDGE and answers *why now* — this column
is that law written at container level.

HIS OWN LAW ON REPEATS, WHICH HE STATED BEFORE THE TABLE

    below more may be repated

He was right and the table proves it: four of his container numbers appear
under two different segments each. `CON-018` is *Auditory Processing* in
SEGMENT 03 and *Threat Detection* in SEGMENT 09. `CON-023` is *Multisensory
Integration* in 03 and *Behavioral Alignment* in 09. `CON-024` is *Salience
Detection* in 03 and *Metacognition* in 10. `CON-026` is *Body Schema* in 04
and *Theory of Mind* in 10.

So a container is NOT held to one segment here. `placements()` returns a LIST,
never a single value, and a repeat is recorded as a repeat rather than
resolved as a collision.

THE NUMBERING SEAM — SURFACED, DECIDED BY NOBODY

His table numbers its containers `CON-001..CON-076`. So does the live registry.
So does the split. **They are three different numberings and they must never be
merged on the numerals** — his own standing ruling, given at the P2561
collision: *do not silently merge namespaces*.

Measured against the split, his numbers agree on the name 16 times out of 48,
and a further band are the same concept differently worded (`Nociception (Pain)`
against `Pain`, `Memory Encoding` against `Encoding`). But SEGMENT 09 and
SEGMENT 10 break down completely: his `CON-026: Theory of Mind` lands on
`SBX-CON-026 Body Schema`, and his `CON-024: Metacognition` lands on
`SBX-CON-024 Salience`. Those are not near-misses, they are different concepts
at the same address.

**So this module matches on the NAME and never on the number.** Whether his
number happens to agree is recorded beside every match as a separate fact
(`number_agrees`) and is never allowed to decide one. Where a name cannot be
placed, the row is HELD with its candidates listed — never dropped, never
guessed at.

WHAT IS HIS AND WHAT IS NOT, ON EVERY ROW

  HIS       48 triggers, carried verbatim from his table, his wording intact
            including his LaTeX (`$T_{max}$`) and his spelling.
  DERIVED   the remaining containers. Composed from TWO REAL SOURCES — the
            container's own machine column (authored with the split) and its
            spine step, which fixes the SHAPE of the firing: a GROUND container
            fires on a baseline reading, a PRESSURE container on a threshold
            crossing, a HALT container on a fault. Nothing is invented from
            nowhere, and every derived row says it is derived and is
            correctable.

The two counts are reported separately and never summed into one number,
because a page that cannot say which triggers are his cannot be corrected by
him.
"""

from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# HIS TABLE, VERBATIM
#
# Ten segments, forty-eight rows, four columns, exactly as he gave them. His
# ids are namespaced `HIS-` so that they can never be read as registry ids
# (CON-001..CON-080) or split ids (SBX-CON-001..183). Same numerals, different
# rows — his own rule, applied to his own document.
# ---------------------------------------------------------------------------

HIS_TABLE = (
    {
        "id": "HIS-SEG-01",
        "name": "AUTONOMIC BASELINES & CORE TELEMETRY",
        "note":
            "Mapping physiological homeostasis directly to low-level hardware, "
            "BIOS, and kernel-level operations.",
        "rows": (
            {
                "his_id": "HIS-CON-001",
                "name": "Thermoregulation",
                "bio":
                    "Hypothalamic set-point modulation; peripheral "
                    "vasodilation/constriction thresholds; eccrine gland "
                    "activation.",
                "engine":
                    "Digital Thermal Sensors (DTS); PWM fan curve dynamic "
                    "adjustment; CPU/GPU clock thermal throttling.",
                "trigger":
                    "Temp > $T_{max}$ triggers cooling loop / frequency scaling.",
            },
            {
                "his_id": "HIS-CON-002",
                "name": "Metabolic Homeostasis",
                "bio":
                    "Blood glucose monitoring via pancreatic islets; "
                    "insulin/glucagon secretion loops.",
                "engine":
                    "Power Delivery Network (PDN) stability; Voltage Regulation "
                    "Modules (VRM) phase switching.",
                "trigger":
                    "Voltage droop triggers LLC (Load-Line Calibration).",
            },
            {
                "his_id": "HIS-CON-005",
                "name": "Circadian Rhythmicity",
                "bio":
                    "Suprachiasmatic nucleus (SCN) light entrainment; melatonin "
                    "suppression/release.",
                "engine":
                    "Real-Time Clock (RTC) synchronization; Network Time Protocol "
                    "(NTP) polling; CRON job scheduling.",
                "trigger":
                    "RTC tick initiates scheduled background maintenance.",
            },
            {
                "his_id": "HIS-CON-006",
                "name": "Sleep Architecture",
                "bio":
                    "Slow-Wave Sleep (SWS) consolidation; REM cycle cortical "
                    "activation; GABAergic inhibition.",
                "engine":
                    "ACPI States (S0ix, S3 Suspend to RAM, S4 Hibernate); memory "
                    "scrubbing; background defragmentation.",
                "trigger":
                    "Idle timer > Threshold triggers ACPI S3/S4 state.",
            },
            {
                "his_id": "HIS-CON-009",
                "name": "Parasympathetic Tone",
                "bio":
                    "Vagal nerve efferent signaling; resting heart rate "
                    "modulation; digestion prioritization.",
                "engine":
                    "Low-power idle states (C-States C0 to C10); clock gating; "
                    "unused peripheral power-down (PCIe ASPM).",
                "trigger":
                    "System load < 5% triggers deep C-State entry.",
            },
            {
                "his_id": "HIS-CON-010",
                "name": "Sympathetic Drive",
                "bio":
                    "Epinephrine/norepinephrine release from adrenal medulla; "
                    "fight-or-flight resource allocation.",
                "engine":
                    "Turbo Boost / Precision Boost Overdrive (PBO); active phase "
                    "shedding bypass; fan speed maximum override.",
                "trigger":
                    "Burst workload triggers PL2 power limit execution.",
            },
        ),
    },
    {
        "id": "HIS-SEG-02",
        "name": "INTERNAL STATE & VOLATILITY MANAGEMENT",
        "note":
            "Mapping internal awareness, energetic depletion, and pain signals "
            "to system arousal and critical fault states.",
        "rows": (
            {
                "his_id": "HIS-CON-003",
                "name": "Phasic Arousal",
                "bio":
                    "Locus coeruleus phasic bursting; noradrenergic cortical "
                    "saturation.",
                "engine":
                    "Processor affinity waking; cache prefetching; "
                    "High-Performance power plan activation.",
                "trigger":
                    "Sudden I/O interrupt triggers context switch.",
            },
            {
                "his_id": "HIS-CON-007",
                "name": "Interoceptive Mapping",
                "bio":
                    "Insular cortex representation of visceral states; vagal "
                    "afferent integration.",
                "engine":
                    "System Management Bus (SMBus) polling; I2C sensor array "
                    "telemetry aggregation.",
                "trigger":
                    "Sensor loop refresh rate (10ms - 1000ms intervals).",
            },
            {
                "his_id": "HIS-CON-011",
                "name": "Nociception (Pain)",
                "bio":
                    "A-delta and C-fiber activation; spinothalamic tract routing "
                    "to somatosensory cortex.",
                "engine":
                    "Machine Check Exceptions (MCE); ECC memory error correction; "
                    "SMART drive failure flags.",
                "trigger":
                    "Hardware fault generates non-maskable interrupt (NMI).",
            },
            {
                "his_id": "HIS-CON-013",
                "name": "Energy Depletion",
                "bio":
                    "ATP/AMP ratio sensing; glycogen store depletion; adenosine "
                    "accumulation.",
                "engine":
                    "Battery Management System (BMS) voltage curve tracking; "
                    "depth of discharge (DoD) calculation.",
                "trigger":
                    "$V_{batt}$ < 3.2V triggers graceful shutdown protocol.",
            },
            {
                "his_id": "HIS-CON-014",
                "name": "Cognitive Fatigue",
                "bio":
                    "Prefrontal extracellular dopamine depletion; sustained "
                    "attention vigilance decrement.",
                "engine":
                    "Page File swapping (thrashing); RAM fragmentation; thermal "
                    "saturation of heatsink mass.",
                "trigger":
                    "Memory utilization > 95% triggers out-of-memory (OOM) "
                    "killer.",
            },
            {
                "his_id": "HIS-CON-016",
                "name": "Basic Drives",
                "bio":
                    "Lateral hypothalamic stimulation; ghrelin/leptin hunger "
                    "signaling.",
                "engine":
                    "Fetch/Retrieve priority queues; bandwidth starvation "
                    "signaling; TCP window scaling adjustments.",
                "trigger":
                    "Buffer empty state triggers high-priority fetch request.",
            },
        ),
    },
    {
        "id": "HIS-SEG-03",
        "name": "EXTEROCEPTIVE PERCEPTION & INPUT TRANSDUCTION",
        "note":
            "Mapping the intake of environmental data from physical sensory "
            "organs to digital data acquisition pipelines.",
        "rows": (
            {
                "his_id": "HIS-CON-017",
                "name": "Visual Processing",
                "bio":
                    "Phototransduction in retinal rods/cones; lateral "
                    "inhibition; V1 edge detection (Gabor filters).",
                "engine":
                    "CMOS image sensor pixel binning; debayering algorithms; "
                    "edge-detection convolution matrices.",
                "trigger":
                    "Photon count exceeds sensor well capacity (clipping).",
            },
            {
                "his_id": "HIS-CON-018",
                "name": "Auditory Processing",
                "bio":
                    "Basilar membrane tonotopy; hair cell mechanotransduction; "
                    "superior olivary complex time-delay mapping.",
                "engine":
                    "Analog-to-Digital Converter (ADC) sampling (e.g., 44.1kHz); "
                    "Fast Fourier Transform (FFT) frequency binning.",
                "trigger":
                    "Acoustic wave pressure changes capacitance in mic "
                    "diaphragm.",
            },
            {
                "his_id": "HIS-CON-019",
                "name": "Somatosensation",
                "bio":
                    "Meissner/Pacinian corpuscles for pressure/vibration; "
                    "two-point discrimination thresholds.",
                "engine":
                    "Capacitive touch grid sensing; piezoelectric force sensors; "
                    "haptic feedback localized matrices.",
                "trigger":
                    "Change in localized capacitance ($pF$) registers X/Y touch.",
            },
            {
                "his_id": "HIS-CON-022",
                "name": "Chemical/Olfactory",
                "bio":
                    "Olfactory bulb glomeruli activation; G-protein coupled "
                    "receptor shape-matching.",
                "engine":
                    "Volatile Organic Compound (VOC) chemical sensor arrays; "
                    "particulate matter (PM2.5) laser scattering.",
                "trigger":
                    "Molecular binding alters electrical resistance of sensor "
                    "surface.",
            },
            {
                "his_id": "HIS-CON-023",
                "name": "Multisensory Integration",
                "bio":
                    "Superior colliculus audiovisual alignment; cortical "
                    "cross-modal binding.",
                "engine":
                    "Sensor fusion (Kalman filters); timestamp synchronization "
                    "across discrete I/O streams (PTP protocol).",
                "trigger":
                    "Delta between sensor timestamps < 1ms to bind events.",
            },
            {
                "his_id": "HIS-CON-024",
                "name": "Salience Detection",
                "bio":
                    "Bottom-up attention capture; pulvinar nucleus filtering; "
                    "amygdala novelty detection.",
                "engine":
                    "Hardware interrupt requests (IRQ); wake-on-LAN/USB packets; "
                    "high-variance delta detection in video streams.",
                "trigger":
                    "Input amplitude > baseline moving average + $3\\sigma$.",
            },
        ),
    },
    {
        "id": "HIS-SEG-04",
        "name": "SPATIAL SCHEMA & ENVIRONMENTAL MAPPING",
        "note":
            "Mapping body ownership and physical location to digital coordinate "
            "tracking and kinematic systems.",
        "rows": (
            {
                "his_id": "HIS-CON-026",
                "name": "Body Schema",
                "bio":
                    "Parietal lobe egocentric integration; intraparietal sulcus "
                    "updating of limb position.",
                "engine":
                    "Device Tree (DT) hardware topology mapping; Inverse "
                    "kinematics solvers for robotic end-effectors.",
                "trigger":
                    "Continuous polling of joint encoder angles "
                    "(degrees/radians).",
            },
            {
                "his_id": "HIS-CON-028",
                "name": "Proprioception",
                "bio":
                    "Muscle spindle stretch receptors; Golgi tendon organ "
                    "tension feedback.",
                "engine":
                    "Gyroscopic tilt calculation; accelerometer $g$-force "
                    "vectors; Hall effect sensor positional feedback.",
                "trigger":
                    "$3\\text{-axis vector sum} = \\sqrt{x^2 + y^2 + z^2}$ "
                    "tracking.",
            },
            {
                "his_id": "HIS-CON-029",
                "name": "Allocentric Mapping",
                "bio":
                    "Hippocampal place cells; entorhinal grid cells; head "
                    "direction cells.",
                "engine":
                    "Simultaneous Localization and Mapping (SLAM); point cloud "
                    "generation (LIDAR); GPS triangulation.",
                "trigger":
                    "Extracted environmental feature matching across visual "
                    "frames.",
            },
            {
                "his_id": "HIS-CON-031",
                "name": "Peripersonal Space",
                "bio":
                    "Multisensory receptive fields extending immediately beyond "
                    "the physical body.",
                "engine":
                    "Proximity sensor arrays (Time-of-Flight); ultrasonic object "
                    "detection envelopes; collision bounding boxes.",
                "trigger":
                    "Object enters virtual boundary radius ($r < 0.5m$).",
            },
        ),
    },
    {
        "id": "HIS-SEG-05",
        "name": "SENSORIMOTOR EXECUTION & OUTPUT KINEMATICS",
        "note":
            "Mapping neurological motor planning and physical execution to "
            "digital actuator outputs and control loops.",
        "rows": (
            {
                "his_id": "HIS-CON-032",
                "name": "Action Readiness",
                "bio":
                    "Supplementary Motor Area (SMA) preparatory potential "
                    "(Bereitschaftspotential).",
                "engine":
                    "Pipeline priming; actuator pre-heating; waking peripheral "
                    "devices from sleep states via bus signals.",
                "trigger":
                    "Intent vector registered; output stage powered up.",
            },
            {
                "his_id": "HIS-CON-034",
                "name": "Motor Planning",
                "bio":
                    "Basal ganglia direct/indirect pathway gating; premotor "
                    "cortex sequence structuring.",
                "engine":
                    "G-code path generation; trajectory optimization algorithms; "
                    "command queue sequencing.",
                "trigger":
                    "Execution array loaded into controller buffer.",
            },
            {
                "his_id": "HIS-CON-036",
                "name": "Motor Execution",
                "bio":
                    "Primary motor cortex (M1) descending pyramidal tract "
                    "firing; alpha motor neuron recruitment.",
                "engine":
                    "Pulse-Width Modulation (PWM) duty cycle signaling; "
                    "Digital-to-Analog (DAC) voltage output driving motors.",
                "trigger":
                    "Logic high ($1$) drives MOSFET gate to power actuator.",
            },
            {
                "his_id": "HIS-CON-041",
                "name": "Dynamic Balance",
                "bio":
                    "Vestibular system semicircular canal fluid dynamics; "
                    "cerebellar postural reflex arc.",
                "engine":
                    "Proportional-Integral-Derivative (PID) control loops; "
                    "active electronic stability control algorithms.",
                "trigger":
                    "Error term $e(t)$ calculation triggers inverse actuator "
                    "response.",
            },
            {
                "his_id": "HIS-CON-048",
                "name": "Sensorimotor Feedback",
                "bio":
                    "Cerebellar forward-model error checking; sensory "
                    "reafference cancellation.",
                "engine":
                    "Closed-loop servo encoder feedback; back-EMF sensing on DC "
                    "motors; real-time telemetry validation.",
                "trigger":
                    "Commanded position minus Actual position > Error Tolerance.",
            },
        ),
    },
    {
        "id": "HIS-SEG-06",
        "name": "ATTENTIONAL DYNAMICS & BANDWIDTH ALLOCATION",
        "note":
            "Mapping the brain's filtering of stimuli to the system's "
            "management of processing threads and network packets.",
        "rows": (
            {
                "his_id": "HIS-CON-050",
                "name": "Selective Attention",
                "bio":
                    "Frontoparietal top-down bias; suppression of distractor "
                    "stimuli via GABAergic interneurons.",
                "engine":
                    "Process priority scheduling (Nice values); thread pinning to "
                    "specific CPU cores; firewall port blocking.",
                "trigger":
                    "Thread priority elevated to Real-Time (RT) scheduling class.",
            },
            {
                "his_id": "HIS-CON-051",
                "name": "Sustained Attention",
                "bio":
                    "Right prefrontal continuous performance maintenance; "
                    "cholinergic basal forebrain modulation.",
                "engine":
                    "Keep-alive packet transmission; infinite loop `while(true)` "
                    "polling; sustained high-clock state (P-States).",
                "trigger":
                    "Process timeout reset via continuous active inputs.",
            },
            {
                "his_id": "HIS-CON-053",
                "name": "Divided Attention",
                "bio":
                    "Task-switching overhead; dual-task interference in working "
                    "memory capacity.",
                "engine":
                    "Time-division multiplexing; context switching overhead "
                    "(register state save/load); asymmetric multiprocessing.",
                "trigger":
                    "Scheduler allocates $t_{slice}$ across multiple concurrent "
                    "threads.",
            },
            {
                "his_id": "HIS-CON-054",
                "name": "Attentional Blink",
                "bio":
                    "Refractory period in stimulus processing (approx 200-500ms "
                    "post-target identification).",
                "engine":
                    "Pipeline flush penalties; interrupt masking during critical "
                    "section execution; debouncing logic.",
                "trigger":
                    "New interrupt ignored if $\\Delta t < \\text{Masking "
                    "Threshold}$.",
            },
        ),
    },
    {
        "id": "HIS-SEG-07",
        "name": "MEMORY ARCHITECTURE & DATA CONSOLIDATION",
        "note":
            "Mapping structural biological memory encoding to exact digital "
            "storage, retrieval, and cache hierarchies.",
        "rows": (
            {
                "his_id": "HIS-CON-064",
                "name": "Episodic Memory",
                "bio":
                    "Hippocampal-cortical trace retrieval; autoassociative "
                    "pattern completion; temporal binding.",
                "engine":
                    "Time-series database querying; sequential system event logs "
                    "(Event Viewer/Syslog); JSON array reconstruction.",
                "trigger":
                    "Query via exact timestamp or primary key relational join.",
            },
            {
                "his_id": "HIS-CON-065",
                "name": "Semantic Memory",
                "bio":
                    "Neocortical hub representations (anterior temporal lobe); "
                    "conceptual hierarchy formation.",
                "engine":
                    "Relational/Vector databases; Knowledge Graphs; Semantic "
                    "embeddings via LLM weight parameters.",
                "trigger":
                    "Vector similarity search (Cosine similarity $> 0.85$).",
            },
            {
                "his_id": "HIS-CON-067",
                "name": "Procedural Memory",
                "bio":
                    "Striatal habit formation; cortico-basal "
                    "ganglia-thalamocortical loops; automaticity.",
                "engine":
                    "Compiled machine code binaries (.exe, .elf); fixed firmware "
                    "routines; pre-calculated Lookup Tables (LUT).",
                "trigger":
                    "Function call directly accesses pre-compiled memory address.",
            },
            {
                "his_id": "HIS-CON-075",
                "name": "Prospective Memory",
                "bio":
                    "Fronto-polar cortex maintenance of delayed intentions; "
                    "event-based vs. time-based triggers.",
                "engine":
                    "Asynchronous callback functions; Webhook listeners; CRON "
                    "jobs; delayed message queues (RabbitMQ/Kafka).",
                "trigger":
                    "Condition matching ($t = T_{target}$) fires callback.",
            },
            {
                "his_id": "HIS-CON-076",
                "name": "Memory Encoding",
                "bio":
                    "Long-Term Potentiation (LTP) via NMDA receptor calcium "
                    "influx; dendritic spine growth.",
                "engine":
                    "NAND flash floating-gate electron trapping; Page Table Entry "
                    "(PTE) creation; file system inode allocation.",
                "trigger":
                    "`fsync()` command flushes volatile cache to non-volatile "
                    "disk.",
            },
        ),
    },
    {
        "id": "HIS-SEG-08",
        "name": "EXECUTIVE FUNCTION & COMPUTATIONAL LOGIC",
        "note":
            "Mapping prefrontal orchestration and abstract reasoning to the CPU "
            "pipeline and algorithmic execution.",
        "rows": (
            {
                "his_id": "HIS-CON-055",
                "name": "Working Memory",
                "bio":
                    "Dorsolateral Prefrontal Cortex (dlPFC) sustained firing; "
                    "phonological loop; visuospatial sketchpad.",
                "engine":
                    "L1/L2/L3 CPU Cache utilization; processor registers (EAX, "
                    "EBX); volatile RAM heap/stack allocation.",
                "trigger":
                    "Data fetched to L1 cache for immediate Arithmetic Logic Unit "
                    "access.",
            },
            {
                "his_id": "HIS-CON-056",
                "name": "Inhibitory Control",
                "bio":
                    "Right Inferior Frontal Gyrus (rIFG) suppression of "
                    "prepotent responses (Go/No-Go tasks).",
                "engine":
                    "Branch misprediction penalty flushing; interrupt masking; "
                    "`kill -9` process termination commands.",
                "trigger":
                    "Branch Target Buffer (BTB) invalidation on wrong speculative "
                    "path.",
            },
            {
                "his_id": "HIS-CON-058",
                "name": "Cognitive Flexibility",
                "bio":
                    "Anterior Cingulate Cortex (ACC) conflict monitoring; "
                    "set-shifting paradigm execution.",
                "engine":
                    "Dynamic re-compilation (JIT); heuristic search path "
                    "switching; hypervisor virtual machine migrations.",
                "trigger":
                    "Cost function gradient shifts, triggering algorithmic state "
                    "change.",
            },
            {
                "his_id": "HIS-CON-059",
                "name": "Executive Sequencing",
                "bio":
                    "Pre-supplementary motor area action chunking; Tower of "
                    "Hanoi logical progression steps.",
                "engine":
                    "Instruction pipeline decoding (Fetch, Decode, Execute, "
                    "Writeback); Directed Acyclic Graph (DAG) task trees.",
                "trigger":
                    "Dependency check pass allows instruction progression.",
            },
        ),
    },
    {
        "id": "HIS-SEG-09",
        "name": "MOTIVATION, EMOTION & VALUE ALIGNMENT",
        "note":
            "Mapping limbic drives and emotional valence to systemic reward "
            "functions and safety guardrails.",
        "rows": (
            {
                "his_id": "HIS-CON-018",
                "name": "Threat Detection",
                "bio":
                    "Amygdalar basolateral nucleus threat valuation; rapid "
                    "subcortical routing via thalamus.",
                "engine":
                    "Antivirus heuristic scanning; Intrusion Detection Systems "
                    "(IDS); out-of-bounds memory access flags.",
                "trigger":
                    "Signature match triggers process quarantine / sandbox "
                    "restriction.",
            },
            {
                "his_id": "HIS-CON-020",
                "name": "Reward Valuation",
                "bio":
                    "Ventral Tegmental Area (VTA) dopaminergic projection to "
                    "nucleus accumbens; prediction errors.",
                "engine":
                    "Reinforcement Learning (RL) positive reward scalar ($+r$); "
                    "objective function minimization/maximization.",
                "trigger":
                    "State-Action pair updates Q-value table based on expected "
                    "return.",
            },
            {
                "his_id": "HIS-CON-021",
                "name": "Aversive Drive",
                "bio":
                    "Habenula activation inhibiting dopamine release; avoidance "
                    "learning reinforcement.",
                "engine":
                    "Negative reward scalars ($-r$); cost function penalties; "
                    "connection timeout drop rates.",
                "trigger":
                    "Error accumulation exceeds threshold, lowering node weight.",
            },
            {
                "his_id": "HIS-CON-023",
                "name": "Behavioral Alignment",
                "bio":
                    "Ventromedial Prefrontal Cortex (vmPFC) integration of "
                    "somatic markers and long-term goals.",
                "engine":
                    "Reinforcement Learning from Human Feedback (RLHF) "
                    "guardrails; system prompts; hardcoded safety policies.",
                "trigger":
                    "Output vector intersects restricted policy boundary; "
                    "generation halted.",
            },
        ),
    },
    {
        "id": "HIS-SEG-10",
        "name": "METACOGNITION & HIGHER-ORDER ADAPTATION",
        "note":
            "Mapping self-awareness and neurological plasticity to system "
            "telemetry, virtualization, and machine learning updates.",
        "rows": (
            {
                "his_id": "HIS-CON-024",
                "name": "Metacognition",
                "bio":
                    "Anterior prefrontal cortex evaluation of own cognitive "
                    "performance (confidence judgments).",
                "engine":
                    "System performance telemetry; application performance "
                    "monitoring (APM) logs; confidence thresholds in ML models.",
                "trigger":
                    "Model outputs probability score $P(x)$ alongside prediction.",
            },
            {
                "his_id": "HIS-CON-025",
                "name": "Default Mode (DMN)",
                "bio":
                    "Medial prefrontal/posterior cingulate synchronous activity "
                    "during rest; autobiographical rumination.",
                "engine":
                    "Background indexing services; garbage collection (memory "
                    "management); deep learning model offline training.",
                "trigger":
                    "CPU idle state triggers background dataset consolidation.",
            },
            {
                "his_id": "HIS-CON-026",
                "name": "Theory of Mind",
                "bio":
                    "Temporoparietal Junction (TPJ) representation of external "
                    "agents' mental states.",
                "engine":
                    "Multi-Agent System (MAS) state modeling; API negotiation "
                    "protocols; opponent modeling in game theory algos.",
                "trigger":
                    "Agent constructs localized state machine to simulate Node "
                    "B's logic.",
            },
            {
                "his_id": "HIS-CON-027",
                "name": "Neuroplasticity",
                "bio":
                    "Synaptogenesis; dendritic pruning; structural "
                    "reorganization based on experiential learning.",
                "engine":
                    "Dynamic neural network weight updates via backpropagation; "
                    "Over-The-Air (OTA) firmware structural flashes.",
                "trigger":
                    "Gradient descent algorithm alters matrix weights to minimize "
                    "loss.",
            },
        ),
    },
)


# ---------------------------------------------------------------------------
# THE SHAPE OF A FIRING, TAKEN FROM HIS SPINE
#
# A trigger is not free text. His own sequence law says a threshold lives on an
# EDGE and answers "why now" — so what makes a container fire depends on WHERE
# ON THE SPINE it sits. A GROUND container has nothing to cross yet: it fires
# on a baseline being read. A PRESSURE container fires on a threshold being
# crossed. A HALT container fires on a fault. This is the second real source a
# derived trigger is built from; the first is the container's own machine
# column.
# ---------------------------------------------------------------------------

SHAPE = {
    1: ("BASELINE READ",
        "%s is read at rest; the value stands as the reference the later steps "
        "are measured against."),
    2: ("THRESHOLD CROSSED",
        "%s crosses its configured limit and asserts; the crossing is the "
        "event, not the level."),
    3: ("STEADY EXECUTION",
        "%s runs unexamined at rate; the firing is continuous and is only "
        "noticed when it stops."),
    4: ("INSPECTION HOOK",
        "%s is frozen and read by an observer; execution pauses at the hook "
        "rather than at a fault."),
    5: ("SERIALIZE / EMIT",
        "%s emits a structured value; the firing is the write, and the value "
        "leaves the container in a form another node can read."),
    6: ("LABEL BOUND",
        "%s binds a name to the thing; the firing is the moment the label "
        "replaces what it stands for, which is the mask."),
    7: ("FAULT RAISED",
        "%s raises a fault it cannot absorb; the firing is the failure and the "
        "failure is the signal, not the end."),
    8: ("COMMIT / RELOAD",
        "%s writes back what the pass learned and re-enters at the ground; the "
        "firing closes the loop."),
    9: ("COMPACTION",
        "%s consolidates across many passes; the firing is scheduled, not "
        "provoked, and runs while nothing is asking."),
    10: ("EVICTION / DECAY",
         "%s loses what is no longer reached; the firing is an absence "
         "becoming measurable."),
    11: ("ARBITRATION",
         "%s meets a second party that disagrees; the firing is the collision, "
         "and it can happen at any step."),
    12: ("RESTRUCTURE",
         "%s rewrites its own form rather than its values; the firing changes "
         "what the container is, and it can happen at any step."),
}


def _norm(s: str) -> str:
    """A name reduced to its content words. Parenthesised glosses are dropped —
    his `Nociception (Pain)` and the split's `Pain` are the same container, and
    the bracket is his gloss, not part of the name."""
    s = re.sub(r"\(.*?\)", " ", (s or "").lower())
    return " ".join(re.findall(r"[a-z]+", s))


#: Words that name the KIND of a container rather than the container. `Visual
#: Processing` and `Visual Perception` are one container under two wordings,
#: and both wordings end in a kind-word. These are dropped only when something
#: else remains — `Salience Detection` reduces to `salience`, but a name that
#: is nothing BUT kind-words keeps them all.
#:
#: An earlier version of this list held `fatigue`, `drive`, `memory` and
#: `basic`, which are content words in some of his names — stripping them
#: silently destroyed real matches (`Cognitive Fatigue` could no longer reach
#: `Fatigue`). Only words that never distinguish one container from another
#: belong here.
_KIND = frozenset(("processing", "perception", "architecture", "detection",
                   "mapping", "dynamics", "system", "systems"))

#: Two tokens are the same word when they share this many leading characters.
#: `interoceptive`/`interoception`, `somatosensation`/`somatosensory` and
#: `rhythmicity`/`rhythm` are one word under two endings; six characters is
#: long enough that `motor` and `motive` stay apart.
_STEM = 6


def _tokens(s: str) -> list:
    ws = _norm(s).split()
    kept = [w for w in ws if w not in _KIND]
    return kept or ws


def _gloss(s: str) -> str:
    """His parenthesised gloss. In `Nociception (Pain)` the gloss is the half
    the split uses as the whole name, so it is a match route of its own."""
    m = re.search(r"\((.*?)\)", s or "")
    return _norm(m.group(1)) if m else ""


def _same_word(a: str, b: str) -> bool:
    if a == b:
        return True
    if len(a) >= _STEM and len(b) >= _STEM and a[:_STEM] == b[:_STEM]:
        return True
    # `plasticity` inside `neuroplasticity`: one name is the other with a
    # domain prefix on it.
    long_, short = (a, b) if len(a) >= len(b) else (b, a)
    return len(short) >= _STEM and short in long_


def _covers(small: list, big: list) -> bool:
    """Every token of `small` is present in `big`."""
    return bool(small) and all(any(_same_word(x, y) for y in big) for x in small)


#: How many split containers a token may reach and still count as evidence on
#: its own. His own bar, third use: a word in forty of his names is weaker
#: evidence than a rare one.
_RARE = 2

#: The grade at which a match may PLACE his wording onto a container. Below it
#: a match is proposed and waits for him.
_PLACE = 2.0


def _reach(token: str) -> list:
    """Which split containers a token reaches. Computed over the live split,
    never typed."""
    from . import sbx
    return [c["id"] for c in sbx.containers()
            if any(_same_word(token, y) for y in _tokens(c["name"]))]


def _score(his: str, split: str) -> tuple:
    """How strongly his name and a split name are the same container.

    Graded, never boolean, and the grade travels with the match so he can see
    which rows were placed on strong evidence and which on weak."""
    hn, sn = _norm(his), _norm(split)
    if hn == sn:
        return (4.0, "EXACT")
    if _gloss(his) and _gloss(his) == sn:
        return (3.5, "HIS GLOSS")
    ht, st = _tokens(his), _tokens(split)
    if _covers(ht, st) and _covers(st, ht):
        return (3.0, "SAME WORDS")
    if _covers(st, ht):
        return (2.0, "SPLIT NAME INSIDE HIS")
    if _covers(ht, st):
        return (2.0, "HIS NAME INSIDE SPLIT")
    # THE WEAKEST ROUTE, and it is the IDF bar again. `Circadian Rhythmicity`
    # and `Circadian Regulation` share no whole name and are plainly one
    # container; `circadian` reaches exactly one container in the split, so it
    # carries the match on its own. A token reaching many containers carries
    # nothing and is refused here — which is why `Regulation` alone does not
    # place Thermoregulation onto Hormonal Regulation.
    shared = [x for x in ht if any(_same_word(x, y) for y in st)]
    rare = [x for x in shared if len(_reach(x)) <= _RARE]
    if rare:
        return (1.0, "SHARED DISTINCTIVE TOKEN: " + ", ".join(sorted(rare)))
    return (0.0, "")


def his_rows() -> list:
    """His 48 rows, flat, each carrying the segment it appeared under."""
    out = []
    for seg in HIS_TABLE:
        for r in seg["rows"]:
            row = dict(r)
            row["his_segment"] = seg["id"]
            row["his_segment_name"] = seg["name"]
            out.append(row)
    return out


def repeats() -> dict:
    """HIS OWN LAW: *below more may be repated*.

    Four of his container numbers carry a different container under a different
    segment. That is recorded as a repeat, never resolved as a collision — a
    container is not held to one segment here."""
    seen = {}
    for r in his_rows():
        seen.setdefault(r["his_id"], []).append(
            {"segment": r["his_segment"], "segment_name": r["his_segment_name"],
             "name": r["name"]})
    rep = {k: v for k, v in seen.items() if len(v) > 1}
    return {
        "his_words": "below more may be repated",
        "repeated_ids": rep,
        "repeated_count": len(rep),
        "law": "a container may serve more than one segment. placements() "
               "returns a list, never a single value, and a repeat is recorded "
               "as a repeat rather than resolved as a collision.",
        "note": "his own table proves it: HIS-CON-018 is Auditory Processing "
                "under SEGMENT 03 and Threat Detection under SEGMENT 09.",
    }


def _best(his_name: str) -> tuple:
    """The split containers that score highest for one of his names, and the
    grade they scored at. More than one at the top is AMBIGUOUS and is held."""
    from . import sbx
    scored = []
    for c in sbx.containers():
        s, grade = _score(his_name, c["name"])
        if s > 0:
            scored.append((s, grade, c))
    if not scored:
        return (0.0, "", [])
    top = max(s for s, _, _ in scored)
    return (top, next(g for s, g, _ in scored if s == top),
            [c for s, _, c in scored if s == top])


def match() -> dict:
    """His 48 rows placed onto the split — BY NAME, NEVER BY NUMBER.

    His table, the live registry and the split all number containers
    `CON-001..`, and they are three different numberings. His own standing
    ruling covers exactly this: *do not silently merge namespaces*. So the
    numerals are never used to place a row. Whether his number happens to land
    on the same name is recorded as a separate fact and decides nothing."""
    from . import sbx
    by_id = {c["id"]: c for c in sbx.containers()}
    placed, proposed, held = [], [], []
    for r in his_rows():
        score, grade, cands = _best(r["name"])
        same_number = by_id.get("SBX-" + r["his_id"].replace("HIS-", ""))
        agrees = bool(cands and same_number and
                      any(c["id"] == same_number["id"] for c in cands))
        rec = {
            "his_id": r["his_id"], "his_name": r["name"],
            "his_segment": r["his_segment"],
            "number_agrees": agrees,
            "number_would_have_given": (
                {"id": same_number["id"], "name": same_number["name"]}
                if same_number else None),
        }
        if len(cands) == 1 and score >= _PLACE:
            rec["matched"] = {"id": cands[0]["id"], "name": cands[0]["name"],
                              "segment": cands[0]["segment"]}
            rec["grade"] = grade
            placed.append(rec)
        elif len(cands) == 1:
            # A single distinctive token is enough to SEE a candidate and not
            # enough to place his wording onto a container. Measured: of three
            # such matches, `circadian` and `chemical` were right and
            # `behavioral` put Behavioral Alignment — his safety-guardrail row
            # — onto Group Behaviour, which is a different thing entirely. A
            # weak match that silently placed would carry his trigger to the
            # wrong container, so it is PROPOSED and waits for his word.
            rec["proposal"] = {"id": cands[0]["id"], "name": cands[0]["name"],
                               "segment": cands[0]["segment"]}
            rec["grade"] = grade
            rec["his_call"] = True
            proposed.append(rec)
        elif len(cands) > 1:
            rec["candidates"] = [{"id": c["id"], "name": c["name"]} for c in cands]
            rec["grade"] = "AMBIGUOUS AT " + grade
            held.append(rec)
        else:
            rec["candidates"] = []
            rec["grade"] = "UNMATCHED"
            held.append(rec)
    return {
        "placed": placed, "placed_count": len(placed),
        "proposed": proposed, "proposed_count": len(proposed),
        "held": held, "held_count": len(held),
        "total": len(his_rows()),
        "law": "matched on the name, never on the number. Only a match at "
               "grade %.1f or better places his wording onto a container; a "
               "weaker one is PROPOSED for his word, and a row that cannot be "
               "matched at all is HELD with its candidates — never dropped and "
               "never guessed at." % _PLACE,
    }


def seams() -> list:
    """The numbering seam, surfaced and decided by nobody.

    Where his number lands on a DIFFERENT container from the one his name
    matches, both readings are kept and neither is preferred."""
    out = []
    for rec in match()["placed"]:
        w = rec["number_would_have_given"]
        if w and not rec["number_agrees"]:
            out.append({
                "his_id": rec["his_id"],
                "his_name": rec["his_name"],
                "his_segment": rec["his_segment"],
                "name_places_it_at": rec["matched"],
                "number_would_place_it_at": w,
                "resolved": False,
                "his_call": True,
                "why": "his table, the registry and the split all number from "
                       "CON-001 and are three different numberings. Same "
                       "numerals, different rows — kept apart under his own "
                       "do-not-silently-merge ruling.",
            })
    return out


def _derive(c: dict) -> dict:
    """A trigger for a container his table does not reach.

    Built from TWO REAL SOURCES and nothing else: the container's own machine
    column (authored with the split) and its spine step, which fixes the shape
    of the firing. Marked DERIVED, and correctable — his word replaces it."""
    kind, template = SHAPE.get(c.get("step", 1), SHAPE[1])
    mech = (c.get("computer") or "").split(";")[0].strip() or c["name"]
    return {
        "kind": kind,
        "trigger": template % mech,
        "by": "DERIVED",
        "from": {"machine_column": c.get("computer"), "step": c.get("step")},
        "correctable": True,
        "note": "his table does not reach this container. Composed from the "
                "container's own machine column and its spine step — not "
                "invented, and replaced the moment he writes one.",
    }


def triggers() -> list:
    """All 183 containers with the third column filled.

    HIS 48 carry his wording verbatim, including his LaTeX and his spelling.
    The rest are DERIVED and say so. The two are never summed into one
    number."""
    from . import sbx
    m = match()
    his_by_split = {}
    for rec in m["placed"]:
        row = next(r for r in his_rows() if r["his_id"] == rec["his_id"]
                   and r["his_segment"] == rec["his_segment"])
        his_by_split.setdefault(rec["matched"]["id"], []).append(row)
    out = []
    for c in sbx.containers():
        rows = his_by_split.get(c["id"], [])
        rec = {"id": c["id"], "name": c["name"], "segment": c["segment"],
               "step": c["step"], "human": c["human"], "computer": c["computer"]}
        if rows:
            r = rows[0]
            rec.update({
                "trigger": r["trigger"], "by": "HIS",
                "kind": SHAPE.get(c["step"], SHAPE[1])[0],
                "bio": r["bio"], "engine": r["engine"],
                "his_id": r["his_id"], "his_name": r["name"],
                "his_segment": r["his_segment"],
                "also_his": [{"his_id": x["his_id"], "name": x["name"],
                              "segment": x["his_segment"]} for x in rows[1:]],
                "correctable": True,
            })
        else:
            rec.update(_derive(c))
        out.append(rec)
    return out


def of(cid: str) -> dict:
    """One container's trigger."""
    cid = (cid or "").strip().upper()
    return next((t for t in triggers() if t["id"] == cid),
                {"found": False, "id": cid})


def placements(cid: str) -> list:
    """Every segment a container serves — a LIST, because of his repeat law."""
    from . import sbx
    cid = (cid or "").strip().upper()
    out = []
    for c in sbx.containers():
        if c["id"] == cid:
            out.append({"segment": c["segment"], "source": "SPLIT",
                        "name": c["name"]})
    t = of(cid)
    if t.get("by") == "HIS":
        out.append({"segment": t["his_segment"], "source": "HIS TABLE",
                    "name": t["his_name"]})
        for a in t.get("also_his", ()):
            out.append({"segment": a["segment"], "source": "HIS TABLE",
                        "name": a["name"]})
    return out


def for_hits(hits) -> dict:
    """THE WIRING, taking hits that are ALREADY COMPUTED.

    This is the form the answer path uses. It must exist separately from
    `fires_on` because `place_on_spine` calls this module and this module
    called `place_on_spine` — wiring the trigger layer into the answer path
    with only `fires_on` available would have recursed forever. The pure
    function takes the hits; the convenience wrapper computes them first.

    A name says what a container is. A trigger says WHEN IT FIRES — so an ask
    can be read as a set of firing conditions rather than a list of nouns."""
    by_id = {t["id"]: t for t in triggers()}
    lit, seen = [], set()
    for h in (hits or ()):
        cid = h.get("container")
        if not cid or cid in seen:
            continue
        seen.add(cid)
        t = by_id.get(cid)
        if not t:
            continue
        lit.append({"container": cid, "name": t["name"], "step": t["step"],
                    "kind": t["kind"], "trigger": t["trigger"], "by": t["by"],
                    "reached_by": h.get("reached_by"), "row": h.get("row")})
    return {
        "containers_lit": len(lit),
        "triggers": lit,
        "his_triggers_lit": sum(1 for t in lit if t["by"] == "HIS"),
        "derived_triggers_lit": sum(1 for t in lit if t["by"] == "DERIVED"),
        "concluded": None,
        "law": "a trigger states the condition a container fires on. Whether "
               "that condition actually held is not knowable from a sentence, "
               "so nothing here is concluded.",
    }


def fires_on(text: str) -> dict:
    """The same reading, from a bare ask. Seats it first, then reads."""
    from . import sbx
    placed = sbx.place_on_spine(text)
    return dict(for_hits(placed.get("hits", ())), text=text)


def stats() -> dict:
    ts = triggers()
    his = [t for t in ts if t["by"] == "HIS"]
    m = match()
    return {
        "his_words": "below more may be repated",
        "his_segments": len(HIS_TABLE),
        "his_rows": len(his_rows()),
        "containers": len(ts),
        "trigger_by_him": len(his),
        "trigger_derived": len(ts) - len(his),
        "his_rows_placed": m["placed_count"],
        "his_rows_held": m["held_count"],
        "repeated_ids": repeats()["repeated_count"],
        "numbering_seams": len(seams()),
        "kinds": sorted({t["kind"] for t in ts}),
        "law": "matched on the name, never on the number. HIS and DERIVED are "
               "counted apart, because a page that cannot say which triggers "
               "are his cannot be corrected by him.",
        "never": "no trigger is invented from nowhere; a derived one names the "
                 "machine column and the spine step it was built from.",
    }


def annotations() -> list:
    return [
        ("below more may be repated", "trigger.repeats"),
        ("the third column: Operational Trigger / State Vector",
         "trigger.triggers"),
        ("matched on the name, never on the number", "trigger.match"),
        ("three numberings, never merged on the numerals", "trigger.seams"),
        ("a trigger says when a container fires, not what it is",
         "trigger.fires_on"),
    ]
