import dialogflow_v2 as dialogflow
import speech_recognition as sr
import pygame
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'projetoteste-277623-dddf2868b39c.json'

# *************************CHAMADA DA API DIALOGFLOW*************************

def detect_intent_stream(project_id, session_id, audio_file_path, language_code):

    session_client = dialogflow.SessionsClient()

    audio_encoding = dialogflow.enums.AudioEncoding.AUDIO_ENCODING_LINEAR_16
    sample_rate_hertz = 44100

    session_path = session_client.session_path(project_id, session_id)

    print('Processando Audio output.wav')

    pygame.mixer.quit()
    pygame.quit()

    def request_generator(audio_config, audio_file_path):

        query_input = dialogflow.types.QueryInput(audio_config=audio_config)

        yield dialogflow.types.StreamingDetectIntentRequest(
            session=session_path, query_input=query_input)

        with open(audio_file_path, 'rb') as audio_file:
            while True:
                chunk = audio_file.read(4096)
                if not chunk:
                    break
                # The later requests contains audio data.
                yield dialogflow.types.StreamingDetectIntentRequest(
                    input_audio=chunk)

    audio_config = dialogflow.types.InputAudioConfig(
        audio_encoding=audio_encoding, language_code=language_code,
        sample_rate_hertz=sample_rate_hertz)

    request_generator(audio_config, audio_file_path)

# *************************PROCESSAMENTO DA SAIDA DE AUDIO*************************

    with open(audio_file_path, 'rb') as audio_file:
        input_audio = audio_file.read()

    query_input = dialogflow.types.QueryInput(audio_config=audio_config)

    response = session_client.detect_intent(
        session=session_path, query_input=query_input,
        input_audio=input_audio)

    with open("../output.wav", 'wb') as out:
        out.write(response.output_audio)
        print('Reproduzindo "output.wav"')

    pygame.init()
    pygame.mixer.music.load("../output.wav")
    pygame.mixer.music.play()

# *************************PROCESSAMENTO DA ENTRADA DE AUDIO*************************

while True:
    pygame.init()
    if pygame.mixer.music.get_busy():
        while a == 1:
            a = 0
    else:
        a = 1
        print('Pode Falar')
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            with open('../input.wav', 'wb') as f:
                f.write(audio.get_wav_data())
        detect_intent_stream(
            'projetoteste-277623', "abcde", "../input.wav", "pt-BR")