import dialogflow
import json
json_name='cryptoassistant-be67b-38e847ce6c0c.json'
with open(json_name) as f:
    auth=json.load(f)
    print(auth)

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=json_name


def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    # for text in texts:
    text = None#'go'
    while True:
        if text:

            text_input = dialogflow.types.TextInput(
                text=text, language_code=language_code)

            query_input = dialogflow.types.QueryInput(text=text_input)

            response = session_client.detect_intent(
                session=session, query_input=query_input)

            print('=' * 20)
            print('Query text: {}'.format(response.query_result.query_text))
            print('Detected intent: {} (confidence: {})\n'.format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence))
            print('Fulfillment text: {}\n'.format(
                response.query_result.fulfillment_text))
            text = input('请输入：\n')
        else:
            text = input('请输入：\n')


if __name__=='__main__':
    detect_intent_texts(project_id=auth['project_id'],
                        session_id='unique',
                        texts=['go','start'],
                        language_code='zh-CN'
                        )
