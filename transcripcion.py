import os
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.utils import which

import sys
import io

# Garante que o terminal irá exibir o texto com acentuação
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


# Configurar o pydub para usar o ffmpeg instalado
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"  # Ou forneça o caminho completo se não estiver no PATH

# Caminho para o arquivo de áudio
audio_file_path = r"C:\Users\rudar\Documents\espanol\aula_1\aula_1.wav"

# Inicializar o reconhecedor
recognizer = sr.Recognizer()

# Função para dividir o áudio em partes menores
def split_audio(audio_file_path):
    audio = AudioSegment.from_wav(audio_file_path)
    chunks = split_on_silence(
        audio,
        min_silence_len=500,
        silence_thresh=-40
    )
    return chunks

# Função para processar cada chunk de áudio
def process_chunk(chunk, recognizer):
    try:
        with sr.AudioFile(chunk) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="es-ES")
            return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

# Dividir o áudio em partes menores
chunks = split_audio(audio_file_path)

# Processar cada chunk de áudio
transcription = ""
for i, chunk in enumerate(chunks):
    chunk_path = f"chunk{i}.wav"
    chunk.export(chunk_path, format="wav")
    transcription += process_chunk(chunk_path, recognizer) + " "
    os.remove(chunk_path)

# Salvar a transcrição em um arquivo com codificação UTF-8
with open("transcricao.txt", "w", encoding="utf-8") as f:
    f.write(transcription.strip())

print("Transcrição salva em transcricao.txt")
