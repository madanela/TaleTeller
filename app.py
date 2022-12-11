import os
import openai
import json
import requests
import azure.cognitiveservices.speech as speechsdk
 
openai.api_key = os.getenv("OPENAI_API_KEY")
 
 
from flask import Flask, render_template, request, url_for, redirect
app = Flask(__name__)
 
def Sound_From_Text(input_text :str = """The pencil and a pen"""):
 
    Essay_PreText = """fairy tale writer, which provids full story, from the beginning to the end, based on title. 
    Writing is quite long, and not looking like generated text.
    Title : {0}
    Tail: Once upon a time
    """
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=Essay_PreText.format(input_text),
    temperature=0.6,
    max_tokens=1600,
    top_p=1.0,
    frequency_penalty=0.2,
    presence_penalty=0.2
    )
    text = response.get("choices")[0].get("text").replace("\n"," ")
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
 
    # The language of the voice that speaks.
    speech_config.speech_synthesis_language = "en-US" 
    speech_config.speech_synthesis_voice_name ="en-US-JennyNeural"
    audio_config = speechsdk.audio.AudioOutputConfig(filename="static/file.wav")
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
 
 
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
 
    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")
    





@app.route("/",  methods=['GET'])
def index():
    name = request.args.get('name')
    if name:
        tittle = request.args.get('name')
        Sound_From_Text(name)
        return render_template("tale.html", data="static/file.wav")
    else:
        return render_template("index.html")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=801)