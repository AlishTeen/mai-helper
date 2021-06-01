import os
import google.cloud.dialogflow_v2 as dialogflow


class DialogflowClass:
    def __init__(self, cred_path):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path
        self.session_client = dialogflow.SessionsClient()

    def get_answer(self, text, session_id):
        session = self.session_client.session_path('mai-agent-nlhi', session_id)
        query_text = dialogflow.types.TextInput(text=text, language_code='ru-RU')
        query = dialogflow.QueryInput(text=query_text)
        response = self.session_client.detect_intent(query_input=query, session=session)
        try:
            images = response.query_result.fulfillment_messages[1].payload.get('images')
        except:
            images = None

        return response.query_result.fulfillment_text, response.query_result.intent.display_name, images
