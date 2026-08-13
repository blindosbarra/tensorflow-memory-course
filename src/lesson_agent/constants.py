"""Single source of truth for the Gemini model name used by every agent.

Decided 2026-08-11 (see `reports/SDD-lesson-agent-2026-08-11.md` section 2.5):
the user asked for "the most recent Gemini Flash" for all five agents, not a
flash/pro split. Model names move fast — bump this one string when a newer
Flash ships, instead of hunting five call sites.
"""

MODEL = "gemini-3.6-flash"
