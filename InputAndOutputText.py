import dialogflow as dialogflow
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'numeric-dialect-274018-d7d703a54605.json'
c = dict
f = []

def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

        resp = dict(response.query_result.parameters)

        print(response.query_result.parameters)
        print(response.query_result.fulfillment_text)

        for a, b in resp.items():
            print(a)
            print(b)
            f.append(a)
            f.append(b)
            print(f)
            if "temperature" in a:
                c = dict(b)
                for d, e in c.items():
                    print(d)
                    print(e)
        g = str(f)
        print(g)
        print(type(g))




while True:
    print("Input a phrase:", end=" ")
    a = input()
    detect_intent_texts('numeric-dialect-274018', "abcde", [a], "pt-BR")

