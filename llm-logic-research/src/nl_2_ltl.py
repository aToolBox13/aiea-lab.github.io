import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def translate_to_ltl(nl_prompt):
    system_instruction = (
        "you are an expert compiler. translate the given natural language system requirements "
        "into strict LTL. use standard operators: G (Globally), "
        "F (Finally), X (Next), U (Until), & (And), | (Or), ! (Not), -> (Implication)."
    )
    
    few_shot_examples = (
        "Input: Always ensure power is active.\nOutput: G(power)\n\n"
        "Input: If an alarm sounds, eventually stop the motor.\nOutput: G(alarm -> F(stop_motor))\n\n"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"{few_shot_examples}Input: {nl_prompt}\nOutput:"}
        ],
        temperature=0.0
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    test_phrase = "Make sure that process A completes before process B starts, and always avoid error states."
    print(f"running..")
    print(f"Input: '{test_phrase}'")
    print(f"Gen. LTL: {translate_to_ltl(test_phrase)}")
