"""The learner: who they are, what they already know, and how they want to be taught.

Before this module the agents had exactly one implicit audience, hardcoded
into `math_agent`'s prompt: *"uno studente che sa programmare ma non ha una
formazione matematica avanzata"*. Every learner got the same document. This
is the missing input — a `LearnerProfile` is seeded into ADK session state
under `{learner_profile}` and every agent's instruction reads it, so the same
notebook produces a different explanation for a beginner and for someone who
already ships models.

Two design notes worth keeping:

- **Levels are rendered as instructions, not as adjectives.** Telling a model
  "the student is a beginner" moves the output much less than telling it
  "do not assume they have seen a gradient before; define every term the
  first time". `Level.briefing` therefore returns a paragraph of concrete
  behaviour, not a label.
- **The profile is personal, so it is git-ignored.** It lives in
  `.learner/profile.json` (see `settings.LEARNER_DIR`), not in
  `course/progress.yaml`, which is committed and tracks *authoring* state.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
import json
from pathlib import Path
from typing import TypeVar

from lesson_agent import settings

PROFILE_FILENAME = "profile.json"

_E = TypeVar("_E", bound=Enum)


class Level(str, Enum):
    """How much machine-learning ground the learner has already covered."""

    PRINCIPIANTE = "principiante"
    INTERMEDIO = "intermedio"
    AVANZATO = "avanzato"

    @property
    def label(self) -> str:
        return {
            Level.PRINCIPIANTE: "Principiante — primo contatto con ML",
            Level.INTERMEDIO: "Intermedio — ho gia' addestrato qualche modello",
            Level.AVANZATO: "Avanzato — lavoro con ML, voglio i dettagli",
        }[self]

    @property
    def briefing(self) -> str:
        """The behavioural instruction handed to the agents for this level."""

        return {
            Level.PRINCIPIANTE: (
                "Lo studente e' alle prime armi con il machine learning. Non "
                "dare per scontato nessun termine tecnico: la prima volta che "
                "usi una parola come 'gradiente', 'embedding', 'overfitting' o "
                "'batch', spiegala in una riga prima di usarla. Parti sempre "
                "dall'intuizione e da un esempio concreto, e solo dopo passa "
                "alla definizione precisa. Preferisci frasi brevi. Se un "
                "dettaglio e' vero ma non serve per capire questa lezione, "
                "omettilo invece di aggiungere una parentesi."
            ),
            Level.INTERMEDIO: (
                "Lo studente ha gia' addestrato qualche modello e conosce il "
                "vocabolario di base (training, validation, loss, overfitting). "
                "Non rispiegare questi termini. Concentrati su cosa rende "
                "diverso il caso di questa lezione, sulle scelte di "
                "progettazione e sui punti dove ci si sbaglia facilmente. "
                "Puoi usare notazione matematica standard senza scusarti, ma "
                "spiega sempre cosa significa ogni simbolo la prima volta."
            ),
            Level.AVANZATO: (
                "Lo studente lavora con il machine learning e non ha bisogno di "
                "introduzioni. Salta le basi. Vai diretto ai dettagli che "
                "contano: perche' questa formulazione e non un'altra, quali "
                "sono i compromessi, cosa si rompe a scala maggiore, come si "
                "collega alla letteratura citata nelle fonti. Segnala "
                "esplicitamente le semplificazioni che il notebook fa per "
                "motivi didattici e cosa si userebbe davvero in produzione."
            ),
        }[self]


class Comfort(str, Enum):
    """Self-declared confidence on one axis (math, Python)."""

    POCA = "poca"
    MEDIA = "media"
    SOLIDA = "solida"

    @property
    def label(self) -> str:
        return {Comfort.POCA: "Poca", Comfort.MEDIA: "Media", Comfort.SOLIDA: "Solida"}[self]


class Depth(str, Enum):
    """How long an answer the learner wants."""

    SINTETICO = "sintetico"
    STANDARD = "standard"
    APPROFONDITO = "approfondito"

    @property
    def label(self) -> str:
        return {
            Depth.SINTETICO: "Sintetico — vai al punto",
            Depth.STANDARD: "Standard",
            Depth.APPROFONDITO: "Approfondito — voglio i dettagli",
        }[self]

    @property
    def briefing(self) -> str:
        return {
            Depth.SINTETICO: (
                "Sii conciso. Ogni sezione al massimo due paragrafi brevi. "
                "Taglia tutto cio' che non serve a rispondere."
            ),
            Depth.STANDARD: (
                "Lunghezza normale: abbastanza da capire davvero, senza "
                "riempitivi."
            ),
            Depth.APPROFONDITO: (
                "Vai a fondo: aggiungi il passaggio intermedio, il caso "
                "limite, il collegamento con le altre lezioni. Resta comunque "
                "ancorato al materiale fornito — approfondire non significa "
                "inventare."
            ),
        }[self]


_MATH_BRIEFING = {
    Comfort.POCA: (
        "Sul lato matematico lo studente si sente insicuro: introduci ogni "
        "formula prima a parole, spiega cosa significa ogni simbolo, e mostra "
        "il calcolo su numeri reali presi dagli output del notebook prima di "
        "generalizzare."
    ),
    Comfort.MEDIA: (
        "Lo studente regge la notazione matematica standard ma la deriva "
        "lentamente: mostra i passaggi, non saltarli, ma non serve rispiegare "
        "somme e prodotti scalari."
    ),
    Comfort.SOLIDA: (
        "Lo studente e' a suo agio con la matematica: usa pure la notazione "
        "compatta e concentrati sul significato e sui compromessi, non sui "
        "passaggi algebrici."
    ),
}

_PYTHON_BRIEFING = {
    Comfort.POCA: (
        "Sul lato codice lo studente e' agli inizi: commenta riga per riga i "
        "passaggi non ovvi, e spiega cosa fa ogni chiamata di libreria e cosa "
        "restituisce."
    ),
    Comfort.MEDIA: (
        "Lo studente conosce Python ma non necessariamente le librerie usate "
        "qui: spiega le API (pandas, NumPy, Keras...) e gli idiomi, non la "
        "sintassi del linguaggio."
    ),
    Comfort.SOLIDA: (
        "Lo studente e' un programmatore Python esperto: niente spiegazioni di "
        "sintassi o di API comuni. Commenta solo le scelte non ovvie, le "
        "insidie e il perche' del design."
    ),
}


@dataclass(frozen=True)
class LearnerProfile:
    """Everything the agents know about the person they are teaching."""

    level: Level = Level.PRINCIPIANTE
    math_comfort: Comfort = Comfort.POCA
    python_comfort: Comfort = Comfort.MEDIA
    depth: Depth = Depth.STANDARD
    background: str = ""
    goals: str = ""
    known_topics: list[str] = field(default_factory=list)

    def briefing(self) -> str:
        """The full learner briefing injected into every agent's instruction.

        This is the text that lands in session state under `learner_profile`
        and is pulled in by each agent's `{learner_profile}` placeholder.
        """

        parts = [
            "## Chi stai insegnando",
            f"Livello dichiarato: **{self.level.value}**.",
            self.level.briefing,
            _MATH_BRIEFING[self.math_comfort],
            _PYTHON_BRIEFING[self.python_comfort],
            self.depth.briefing,
        ]
        if self.background.strip():
            parts.append(
                "Background dichiarato dallo studente (usalo per scegliere le "
                f"analogie): {self.background.strip()}"
            )
        if self.goals.strip():
            parts.append(
                "Obiettivo dichiarato dallo studente (dai piu' spazio a cio' "
                f"che lo serve): {self.goals.strip()}"
            )
        if self.known_topics:
            topics = ", ".join(self.known_topics)
            parts.append(
                f"Argomenti che lo studente dichiara di conoscere gia': {topics}. "
                "Non rispiegarli da zero: richiamali in una riga e vai avanti."
            )
        return "\n\n".join(parts)

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        # Enum members serialise as their `.value` (they are str subclasses,
        # but asdict keeps the member itself for frozen dataclasses).
        for key in ("level", "math_comfort", "python_comfort", "depth"):
            data[key] = str(getattr(self, key).value)
        return data

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> LearnerProfile:
        """Rebuild a profile from JSON, falling back to defaults per field.

        Tolerant on purpose: a profile written by an older version of the app
        (or hand-edited) should degrade to defaults rather than crash the GUI
        on startup.
        """

        def _enum(enum_cls: type[_E], key: str, default: _E) -> _E:
            try:
                return enum_cls(data.get(key))
            except ValueError:
                return default

        topics = data.get("known_topics") or []
        return cls(
            level=_enum(Level, "level", Level.PRINCIPIANTE),
            math_comfort=_enum(Comfort, "math_comfort", Comfort.POCA),
            python_comfort=_enum(Comfort, "python_comfort", Comfort.MEDIA),
            depth=_enum(Depth, "depth", Depth.STANDARD),
            background=str(data.get("background") or ""),
            goals=str(data.get("goals") or ""),
            known_topics=[str(t) for t in topics] if isinstance(topics, list) else [],
        )


def profile_path(learner_dir: Path | None = None) -> Path:
    """Where the profile lives.

    `learner_dir` resolves at *call* time, not at import: binding
    `settings.LEARNER_DIR` as a default argument would freeze it at module
    import and make the directory impossible to redirect in tests.
    """

    return (learner_dir or settings.LEARNER_DIR) / PROFILE_FILENAME


def load_profile(learner_dir: Path | None = None) -> LearnerProfile:
    """Read the saved profile, or return defaults if there isn't one yet."""

    path = profile_path(learner_dir)
    if not path.exists():
        return LearnerProfile()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return LearnerProfile()
    return LearnerProfile.from_dict(data if isinstance(data, dict) else {})


def save_profile(profile: LearnerProfile, learner_dir: Path | None = None) -> Path:
    path = profile_path(learner_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(profile.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    return path
