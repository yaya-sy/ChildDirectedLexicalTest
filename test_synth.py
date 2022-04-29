from google.oauth2 import service_account
from google.cloud import texttospeech

cred_path = '/scratch2/mlavechin/ChildDirectedLexicalTest/child_workspace/synth/credentials.json'

print("Trying to authenticate with: %s" % cred_path)

credentials = service_account.Credentials.from_service_account_file(cred_path)
client = texttospeech.TextToSpeechClient(credentials=credentials)

# Input to be synthetized 
synthesis_input = texttospeech.SynthesisInput(text="Hello, World!")
voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
            )
audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
            )

# Run authenticated request
response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
            )
print("Got:", type(response))
