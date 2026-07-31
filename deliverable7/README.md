# Backward Chaining for FOL

Backward chaining verifies a goal by working backwards from it, using recursion. Facts are rules with no body and stop the recursion. It is the precise opposite of forward chaining.

My code, `fol_backward_chaining.py` does this from scratch, with  a recursive `ask()` over a `KnowledgeBase` of facts/rules (inspired by the NBA cuz I love basketball)

Run it:

```
python fol_backward_chaining.py
python test_fol_backward_chaining.py
```
