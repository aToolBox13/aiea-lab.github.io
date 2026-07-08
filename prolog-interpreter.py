import os
import tempfile
from openai import OpenAI
from pyswip import Prolog

client = OpenAI()

def translate_nl_to_prolog(prompt_text):
    system_instruction = (
        "You are an expert Prolog translator. Translate the given natural language statement "
        "into valid SWI-Prolog syntax. Respond ONLY with the Prolog code inside a markdown "
        "code block. Do not include explanations. Ensure all predicate and constant names "
        "start with lowercase letters."
    )
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.0
    )
    
    raw_content = response.choices[0].message.content
    prolog_code = raw_content.replace("```prolog", "").replace("```", "").strip()
    return prolog_code

def main():
    nl_input = (
        "Facts:\n"
        "jokic is the parent of wembanyama. jokic is the parent of antetokounmpo. jokic is the parent of doncic.\n"
        "brunson is the parent of wembanyama. brunson is the parent of antetokounmpo. brunson is the parent of doncic.\n"
        "lebron is the parent of jokic. curry is the parent of jokic.\n"
        "durant is the parent of brunson. harden is the parent of brunson.\n"
        "\nRules:\n"
        "X is a grandparent of Y if X is the parent of Z and Z is the parent of Y.\n"
        "X is a sibling of Y if Z is the parent of X, Z is the parent of Y, and X is not equal to Y."
    )
    
    print("Sending natural language KB to OpenAI for Prolog translation...")
    prolog_rules = translate_nl_to_prolog(nl_input)
    print("\n[Generated Prolog Knowledge Base]")
    print(prolog_rules)
    print("-" * 50)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.pl', delete=False) as temp_pl_file:
        temp_pl_file.write(prolog_rules)
        temp_file_path = temp_pl_file.name

    try:
        print("Initializing SWI-Prolog engine...")
        prolog = Prolog()
        prolog.consult(temp_file_path)
        
        print("\nExecuting Query 1: Who are the grandparents of wembanyama?")
        query_1 = "grandparent(X, wembanyama)"
        results_1 = list(prolog.query(query_1))
        
        if results_1:
            grandparents = set(sol['X'] for sol in results_1)
            for gp in grandparents:
                print(f" - {gp.capitalize()} is a grandparent of Wembanyama.")
        else:
            print(" - No grandparents found.")
            
        print("\nExecuting Query 2: Who are the siblings of doncic?")
        query_2 = "sibling(X, doncic)"
        results_2 = list(prolog.query(query_2))
        
        if results_2:
            siblings = set(sol['X'] for sol in results_2)
            for sib in siblings:
                print(f" - {sib.capitalize()} is a sibling of Doncic.")
        else:
            print(" - No siblings found.")
            
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

if __name__ == "__main__":
    main()