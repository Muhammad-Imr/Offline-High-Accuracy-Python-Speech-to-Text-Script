import os
import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer

MODEL_PATH = r"C:\Users\CEO-FOUNDER-HTS\Desktop\Offline High-Accuracy Python Speech-to-Text Script\vosk-model-fr-0.22"

if not os.path.exists(MODEL_PATH):
    raise Exception(f"Model folder not found at {MODEL_PATH}.")

try:
    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, 16000)
    recognizer.SetWords(True)
    print("Vosk Model Loaded Successfully!")
except Exception as e:
    raise Exception(f"Failed to load model: {str(e)}")

audio_queue = queue.Queue()

def audio_callback(indata, frames, time, status):
    if status:
        print(f"Audio Status: {status}")
    audio_queue.put(bytes(indata))

def main():
    print("Parlez maintenant... (Appuyez sur Ctrl+C pour arrêter)")

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16",
                           channels=1, callback=audio_callback):
        try:
            while True:
                data = audio_queue.get()
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    print("Texte:", result["text"])
        except KeyboardInterrupt:
            print("\nTranscription terminée.")

if __name__ == "__main__":
    main()
