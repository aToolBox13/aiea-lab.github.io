import os
import shutil
import re
from openai import OpenAI
from pyke import knowledge_engine

client = OpenAI()

CACHE_DIR = "./pyke_cache"

sys_prompt = """turn this into pyke syntax. only output this, nothing else:

FACTS:
one fact per line like parent(jokic, wembanyama)

RULES:
one rule per line like:
parent($x, $z) && parent($z, $y) >>> grandparent($x, $y)
if you need x not equal y use NEQ($x, $y) as a premise
vars start with $
"""

def get_pyke_kb(text):
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": text}
        ],
        temperature=0
    )
    return res.choices[0].message.content.strip()

def split_kb(raw):
    facts = []
    rules = []
    for line in raw.splitlines():
        line = line.strip()
        if not line or line in ("FACTS:", "RULES:"):
            continue
        if ">>>" in line:
            rules.append(line)
        else:
            facts.append(line)
    return facts, rules


def write_facts(facts):
    with open(os.path.join(CACHE_DIR, "facts.kfb"), "w") as f:
        for fact in facts:
            f.write(fact.strip() + "\n")


# turn our simple rule format into real pyke rule syntax
def make_rule(i, rule):
    left, right = rule.split(">>>")
    premises = [p.strip() for p in left.split("&&")]
    conclusions = [c.strip() for c in right.split("&&")]

    out = f"fact{i}\n\tforeach"
    extra_checks = []
    for p in premises:
        # neq is not a real fact, its a check
        check = re.match(r"NEQ\((\$\w+),\s*(\$\w+)\)", p)
        if check:
            extra_checks.append(f"\t\tcheck {check.group(1)} != {check.group(2)}")
        else:
            out += f"\n\t\tfacts.{p}"
    for c in extra_checks:
        out += "\n" + c
    out += "\n\tassert"
    for c in conclusions:
        out += f"\n\t\tfacts.{c}"
    return out


def write_rules(rules):
    all_rules = []
    for i, r in enumerate(rules):
        all_rules.append(make_rule(i + 1, r))
    with open(os.path.join(CACHE_DIR, "rules.krb"), "w") as f:
        f.write("\n\n".join(all_rules))


=def ask(engine, pred, known_val):
    answers = set()
    for ns in ["facts", "rules"]:
        goal = f"{ns}.{pred}($x, {known_val})"
        try:
            with engine.prove_goal(goal) as gen:
                for vars, plan in gen:
                    answers.add(vars["x"])
        except:
            pass
    return answers


def main():
    kb_text = (
        "facts:\n"
        "jokic is the parent of wembanyama. jokic is the parent of antetokounmpo. jokic is the parent of doncic.\n"
        "brunson is the parent of wembanyama. brunson is the parent of antetokounmpo. brunson is the parent of doncic.\n"
        "lebron is the parent of jokic. curry is the parent of jokic.\n"
        "durant is the parent of brunson. harden is the parent of brunson.\n"
        "\nrules:\n"
        "x is a grandparent of y if x is the parent of z and z is the parent of y.\n"
        "x is a sibling of y if z is the parent of x, z is the parent of y, and x \\= y."
    )

    print("talking to sam altman")
    raw = get_pyke_kb(kb_text)
    print(raw)
    print("-" * 40)

    facts, rules = split_kb(raw)

=    if os.path.exists(CACHE_DIR):
        shutil.rmtree(CACHE_DIR)
    os.makedirs(CACHE_DIR)

    write_facts(facts)
    write_rules(rules)

    engine = knowledge_engine.engine(CACHE_DIR)
    engine.reset()
    engine.activate("rules")
    engine.get_kb("facts")

    print("\nwho are wembanyama's grandparents?")
    for gp in ask(engine, "grandparent", "wembanyama"):
        print(" -", gp)

    print("\nwho are doncic's siblings?")
    for sib in ask(engine, "sibling", "doncic"):
        print(" -", sib)


if __name__ == "__main__":
    main()
