# LangChain with backward chaining (inspired by Logic-LM: https://arxiv.org/abs/2305.12295)

Takes a normal  yesno question, extracts relevant facts/rules out of a prolog KB with a retriever, has an LLM (via LangChain) translate the question into a  query, then runs that query through the backward chaining solver from last week's onboarding task and returns true/false plus the proof trace. It follows the general format of Logic-LM paper's pipeline, just without the course-correcting loop.

Files:
- `kb_basketball.pl` — KB with 22 facts + 7 rules
- `engine.py` — the solver 
- `rag.py` — turns each KB clause into a sentence, embeds them, builds a LangChain retriever
- `logic_lm.py` — the actual pipeline that does all the work
- `test_pipeline.py` — tests

Set `API_KEY` to use a real LLM; if you don't it just falls back on a dummy automated solver

```
pip install -r requirements.txt
python logic_lm.py
python test_pipeline.py
```
