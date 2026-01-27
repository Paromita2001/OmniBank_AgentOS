# pipeline/test_intent.py

from pipeline.intent_parser import parse_intent

while True:
    text = input("\nUser: ")
    if text.lower() in ["exit", "quit"]:
        break

    result = parse_intent(text)
    print("\nParsed Output:")
    print(result.model_dump())
