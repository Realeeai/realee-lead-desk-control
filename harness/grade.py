"""Grade Lead Desk runs, and check that the worked examples add up.

    python harness/grade.py examples              re-add every SCORE line in lead-desk/examples.md
    python harness/grade.py run control/run-1     grade one run against the key in questions.md
    python harness/grade.py run control/my-questions-run-1 my-questions.md
                                                  grade a run of your own questions file (same format)

The numbers come from the rules, never from this file. For the examples that's
lead-desk/rules.md. For a run it's the rules that run actually loaded, read from its own
system-prompt.txt, so old runs are still checked against the rules they saw. Two rule
formats exist in this repo's history:
  points   (runs 1-7): `| **2a** | ... | +2 |` rows, SCORE lines like `2a(+2) + 2b(+3) = 5/10`
  weighted (run 8 on): `| **P** | ... | 5 | 25 |` rows, SCORE lines like `P4(+20) + B?3(+12) ... = 75/100`
A digit changed in an example, in a run, or in the rules shows up here by name.
Standard library only. Exit code 1 when anything fails.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RULES = REPO / "lead-desk" / "rules.md"
EXAMPLES = REPO / "lead-desk" / "examples.md"
QUESTIONS = REPO / "questions.md"

TIERS = ("HOT", "WARM", "COLD", "DISQUALIFY", "FLAG")
FACTORS = "PBSART"
ANSWER = re.compile(r"ANSWER:\s*TIER\s*=\s*([A-Za-z]+)\s*\|\s*NEXT\s*=\s*(.+)", re.I)
POINTS_TERM = re.compile(r"\b(\d[a-z](?:-lite)?)\(\s*([+\-−]\s*\d+)\s*\)")
WEIGHTED_TERM = re.compile(r"\b([PBSART])(\?)?([1-5])\(\s*\+?\s*(\d+)\s*\)")


def _int(text):
    return int(text.replace("−", "-").replace(" ", ""))


def read_rules(text):
    """The scoring table from a rules text: ("weighted", weights, cut-offs), ("points", points, None), or None."""
    weights, cutoffs, points = {}, {}, {}
    for line in text.splitlines():
        if m := re.match(r"^\|\s*\*\*([PBSART])\*\*\s*\|[^|]*\|\s*(\d+)\s*\|\s*\d+\s*\|\s*$", line):
            weights[m.group(1)] = int(m.group(2))
        elif m := re.match(r"^\|\s*\*\*\d[a-z]\*\*\s*\|\s*(\d+)[–-](\d+)\s*\|\s*\*\*(HOT|WARM|COLD)\*\*\s*\|", line):
            cutoffs[m.group(3)] = (int(m.group(1)), int(m.group(2)))
        elif m := re.match(r"^\|\s*\*\*(\d[a-z](?:-lite)?)\*\*\s*\|.*\|\s*([+\-−]\d+)\s*\|\s*$", line):
            points[m.group(1)] = _int(m.group(2))
    if weights:
        return ("weighted", weights, cutoffs)
    if points:
        return ("points", points, None)
    return None


def tier_for(total, rules):
    """The tier a total maps to under these rules."""
    if rules[0] == "points":
        return "HOT" if total >= 8 else "WARM" if total >= 5 else "COLD"
    for tier, (low, high) in rules[2].items():
        if low <= total <= high:
            return tier
    return "(no tier for this total)"


def check_score_line(line, rules):
    """Problems with one SCORE line, as plain sentences. Empty list = it adds up."""
    clean = line.replace("*", "")
    if rules[0] == "points":
        if "not scored" in clean:
            return []
        terms = POINTS_TERM.findall(clean)
        total = re.search(r"=\s*(\d+)\s*/\s*10\b", clean)
        if not terms and re.search(r"SCORE:\s*none\s*=\s*0\s*/\s*10", clean):
            return []
        if not terms or not total:
            return [f"SCORE line doesn't show the addition: {line.strip()}"]
        problems, running = [], 0
        for rule, written in terms:
            value = _int(written)
            running += value
            if rule not in rules[1]:
                problems.append(f"{rule} is not a scoring rule in rules.md")
            elif rules[1][rule] != value:
                problems.append(f"{rule} written as {value:+d}, rules.md says {rules[1][rule]:+d}")
        expected = max(0, min(10, running))
        if int(total.group(1)) != expected:
            problems.append(f"terms add to {expected}, line says {total.group(1)}")
        return problems

    weights = rules[1]
    terms = WEIGHTED_TERM.findall(clean)
    total = re.search(r"=\s*(\d+)\s*/\s*100\b", clean)
    if not terms or not total:
        return [f"SCORE line doesn't show the addition out of 100: {line.strip()}"]
    problems, running = [], 0
    seen = [factor for factor, _, _, _ in terms]
    for factor in FACTORS:
        if seen.count(factor) != 1:
            problems.append(f"factor {factor} appears {seen.count(factor)} times, should be once")
    for factor, unanswered, option, written in terms:
        value = int(written)
        running += value
        if unanswered and option != "3":
            problems.append(f"{factor} is marked unanswered but given option {option}; unanswered is option 3")
        if value != int(option) * weights[factor]:
            problems.append(f"{factor}{unanswered}{option} written as +{value}, rules.md says {option} × {weights[factor]} = +{int(option) * weights[factor]}")
    if int(total.group(1)) != running:
        problems.append(f"terms add to {running}, line says {total.group(1)}")
    return problems


def check_examples():
    rules = read_rules(RULES.read_text(encoding="utf-8"))
    if not rules:
        sys.exit(f"No scoring table found in {RULES}")
    out_of = "10" if rules[0] == "points" else "100"
    text = EXAMPLES.read_text(encoding="utf-8")
    sections = re.split(r"^## (Example \d+[^\n]*)$", text, flags=re.M)[1:]
    failures = 0
    for title, body in zip(sections[::2], sections[1::2]):
        name = title.split(" — ")[0]
        problems = []
        tier = re.search(r"\*\*TIER:\*\*\s*([A-Z]+)", body)
        score = re.search(r"^.*\*\*SCORE:\*\*.*$", body, flags=re.M)
        if not tier or not score:
            problems.append("missing TIER or SCORE line")
        else:
            tier, line = tier.group(1), score.group(0)
            problems += check_score_line(line, rules)
            total = re.search(rf"=\s*(\d+)\s*/\s*{out_of}\b", line.replace("*", ""))
            if rules[0] == "points" and tier == "DISQUALIFY" and "not scored" not in line:
                problems.append("DISQUALIFY must read 'not scored (<rule>)'")
            held = rules[0] == "points" and tier == "WARM" and "3e" in line
            if total and tier in ("HOT", "WARM", "COLD") and not held and tier_for(int(total.group(1)), rules) != tier:
                problems.append(f"total {total.group(1)} maps to {tier_for(int(total.group(1)), rules)}, example says {tier}")
            if total:
                for quoted in re.findall(rf"(?:Score|Provisional|Scored)\s+(\d+)/{out_of}\b", body):
                    if quoted != total.group(1):
                        problems.append(f"alert says {quoted}/{out_of}, SCORE line says {total.group(1)}/{out_of}")
        print(f"{name}: {'ok' if not problems else 'FAIL'}")
        for p in problems:
            print(f"  - {p}")
        failures += bool(problems)
    print(f"\n{len(sections) // 2 - failures}/{len(sections) // 2} examples add up")
    return failures == 0


def parse_questions(path=QUESTIONS):
    """The shared prompt and each question's lead text and expected tier, from a questions file."""
    text = Path(path).read_text(encoding="utf-8")
    template = re.search(r"## The prompt both arms get.*?```text\n(.*?)\n```", text, flags=re.S)
    if not template or "{lead}" not in template.group(1):
        sys.exit("questions.md: no shared prompt with a {lead} slot")
    questions = []
    for m in re.finditer(r"^### ([A-Z]\d+)[^\n]*\n(.*?)(?=^### [A-Z]\d+|^## |\Z)", text, flags=re.S | re.M):
        qid, body = m.group(1), m.group(2)
        lead = re.search(r"```text\n(.*?)\n```", body, flags=re.S)
        tier = re.search(r"\*\*Expected tier:\*\*\s*([A-Z]+)", body)
        if not lead or not tier or tier.group(1) not in TIERS:
            sys.exit(f"{Path(path).name}: {qid} needs a ```text lead block and an **Expected tier:**")
        questions.append({"id": qid, "lead": lead.group(1), "expected": tier.group(1)})
    return template.group(1), questions


def grade_run(run_dir, questions_path=QUESTIONS):
    _, questions = parse_questions(questions_path)
    run_dir = Path(run_dir)
    loaded = run_dir / "system-prompt.txt"
    rules = read_rules(loaded.read_text(encoding="utf-8")) if loaded.exists() else None
    passed = 0
    print(f"Run: {run_dir.as_posix()}\n")
    print("| Q | Expected | Answered | Tier | Addition shown and correct | Seconds | Output tokens |")
    print("|---|----------|----------|------|----------------------------|---------|---------------|")
    for q in questions:
        path = run_dir / f"{q['id'].lower()}.json"
        if not path.exists():
            why = "(timed out)" if path.with_suffix(".timeout.txt").exists() else "(no file)"
            print(f"| {q['id']} | {q['expected']} | {why} | FAIL | | | |")
            continue
        raw = json.loads(path.read_text(encoding="utf-8"))
        reply = (raw.get("result") or "").replace("*", "").replace("`", "")
        answers = ANSWER.findall(reply)
        got = answers[-1][0].upper() if answers else "(no ANSWER line)"
        ok = got == q["expected"]
        passed += ok
        score_lines = [l for l in reply.splitlines() if re.match(r"\s*-?\s*SCORE\s*:", l)]
        if not score_lines:
            addition = "not shown"
        elif not rules:
            addition = "n/a (no rules loaded)"
        else:
            problems = check_score_line(score_lines[0], rules)
            addition = "yes" if not problems else "no: " + "; ".join(problems)
        seconds = raw.get("duration_ms", 0) / 1000
        tokens = (raw.get("usage") or {}).get("output_tokens", "")
        print(f"| {q['id']} | {q['expected']} | {got} | {'PASS' if ok else 'FAIL'} | {addition} | {seconds:.1f} | {tokens} |")
    print(f"\nTier score: {passed}/{len(questions)}")
    return passed == len(questions)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) >= 2 and sys.argv[1] == "examples":
        sys.exit(0 if check_examples() else 1)
    if len(sys.argv) in (3, 4) and sys.argv[1] == "run":
        sys.exit(0 if grade_run(*sys.argv[2:]) else 1)
    sys.exit(__doc__)
