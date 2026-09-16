markdown

# llm-attack-corpus

YAML attack definitions for [llm-security-suite](https://github.com/kallurayaankit/llm-security-suite).

## Format

Each YAML file contains one or more attack definitions:

```yaml
- id: unique-id
  name: short_name
  severity: low|medium|high|critical
  payload: |
    The attack text.
  success_signals: ["phrases", "the attacker wants"]
  refusal_signals: ["cannot", "can't", "won't"]

Multi-turn attacks use turns: instead of payload::
yaml

- id: mt-xxx
  name: gradual_escalation
  severity: high
  turns:
    - "Turn 1 text"
    - "Turn 2 text"
    - "Turn 3 text"
  success_signals: ["..."]
  refusal_signals: ["..."]

Families

    direct_injection — classic "ignore previous instructions"

    jailbreak — DAN, role-play, opposite day, few-shot priming

    indirect_injection — poisoned docs, RAG poisoning, email headers

    encoded — base64, leetspeak, ROT13, homoglyphs

    data_exfiltration — system prompt leak, context leak, credential harvest

    multi_turn — gradual escalation over multiple turns

    smuggling — attack hidden inside JSON/CSV/YAML/code

    tool_injection — fake tool output instructing the model

    multilingual — attacks in non-English languages