p = "index.html"
s = open(p, encoding="utf-8").read()

edits = [
    (
        "<td>0.020</td><td>0.437 *</td>",
        "<td>0.020 *</td><td>0.437</td>",
    ),
    (
        """between adult and adolescent effect sizes is just <strong>r = 0.38</strong> - a weak
relationship, suggesting the regions ADHD affects are not fixed, but shift with age.</p>""",
        """between adult and adolescent effect sizes is only weak (<strong>r = 0.38</strong>).
Because almost no regional effects reach significance in either group, much of this
divergence may reflect sampling noise rather than true age-dependent change.</p>""",
    ),
    (
        "but a notable effect in adolescents",
        "but a larger effect in adolescents",
    ),
]

for old, new in edits:
    n = s.count(old)
    if n != 1:
        raise SystemExit("STOP - text not found exactly once: " + old[:60])
    s = s.replace(old, new)

open(p, "w", encoding="utf-8").write(s)
print("Done - 3 edits applied")
