# Constitution prompt

Paste this after `/speckit-constitution` in the Copilot chat panel.

---

> This project is an expense policy validator for Finance. Establish these principles:
> policy values such as caps, thresholds and exchange rates must live in a data file
> and never be written into code; every functional requirement must map to at least
> one automated test whose name references the requirement id; the tool uses only
> the Python standard library at runtime unless the plan justifies a dependency;
> money is always handled as Decimal and never as a float; and the tool reports every
> violation in a single pass with exit codes that are specified before implementation.
> The tool must run offline with no API keys or paid services.

---

## Why these five

Each principle closes off a specific way the one-shot validator in demo 01 went wrong.
Hard-coded numbers, untested requirements, floats for money, and stopping at the
first problem are all things a model will do by default unless something tells it
not to. The constitution is that something, and it applies to every feature rather
than being repeated in every prompt.
