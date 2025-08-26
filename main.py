import sys
import os
import gc
import logging
import whisper
import ollama
from pydub import AudioSegment
from datetime import datetime

# Constants
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "300"))
MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME", "llama3.1:17b")
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# Configure logging to log to both console and a file
log_filename = datetime.now().strftime("transcription_%Y-%m-%d_%H-%M-%S.log")
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler(log_filename)  # Log to a file
    ]
)

# Local ollama client connection with a specified timeout
client = ollama.Client(host=OLLAMA_URL, timeout=OLLAMA_TIMEOUT)

def get_file_extension(file_path):
    return "." + file_path.split(".")[-1]

def convert_m4a_to_wav(m4a_filepath, wav_filepath):
    """ Converts an M4A audio file to WAV format. """
    logging.info(f"Starting conversion of '{m4a_filepath}' to WAV format.")
    try:
        sound = AudioSegment.from_file(m4a_filepath, format="m4a")
        sound.export(wav_filepath, format="wav")
        logging.info(f"Successfully converted '{m4a_filepath}' to '{wav_filepath}'.")
    except Exception as e:
        logging.error(f"Error converting '{m4a_filepath}': {e}")
        raise

def delete_generated_wav_file(wav_file_path):
    """ Delete the application made WAV file. """
    try:
        os.remove(wav_file_path)
        logging.info(f"Removed WAV file '{wav_file_path}'.")
    except Exception as e:
        logging.error(f"Error deleting WAV file '{wav_file_path}': {e}")

def format_assistant(ascii_transcript):
    """ Converts the transcript to readable format using Ollama model. """
    system_prompts = [
        "You are a skilled transcription editor with extensive experience in refining audio transcripts while maintaining the original content.",
        "Your task is to clean up a provided transcript from an audio file, ensuring the structure, punctuation, and formatting are applied without altering the original message.",
        "Do not introduce any new ideas or concepts that were not part of the original transcript.",
        "Focus solely on structural improvements and punctuation.",
        "It is very important that you only provide the final output without any additional comments or remarks."
    ]
    
    messages = [
        {"role": "system", "content": "\n".join(system_prompts[:2] + system_prompts[4:]) },
        {"role": "user", "content": "Here is the transcript:\n" + ascii_transcript }
    ]

    response = client.chat(model=MODEL_NAME, messages=messages, options={"temperature": 0})

    logging.info("Translation formatting completed successfully.")
    return response.message.content

def transcribe(wav_file_path):
    # Load the Whisper model
    model = whisper.load_model("base", device="cuda")
    logging.info("Whisper model loaded successfully.")
    
    # Transcribe the audio file
    try:
        result = model.transcribe(wav_file_path, fp16=False)
        logging.info("Transcription completed successfully.")
    except Exception as e:
        logging.error(f"Error during transcription: {e}")
        raise
    
    del model
    gc.collect()

    logging.info(f"Detected language: {result['language']}")
	
    return result["text"]

def save_transcription(file_path, extra, transcription):
    """ Saves the transcription to a file. """
    output_file_path = file_path.replace(get_file_extension(file_path), f"{extra}-transcription.txt")
    logging.info(f"Saving transcription to '{output_file_path}'")
    
    with open(output_file_path, "w") as f:
        f.write(f"Source Audio File: {file_path}\n")
        f.write("Transcription:\n\n")
        f.write(transcription)
    
    logging.info(f"Transcription saved successfully to '{output_file_path}'.")
	
def transcribe_audio(file_path):
    """ Transcribes an audio file using the Whisper model and formats it. """
    logging.info(f"Starting transcription for file: '{file_path}'")
    del_file_path = None

    # Convert to WAV if necessary
    wav_file_path = file_path if file_path.endswith(".wav") else file_path.replace(get_file_extension(file_path), ".wav")
    if file_path != wav_file_path:
        convert_m4a_to_wav(file_path, wav_file_path)
        del_file_path = wav_file_path

    # Do the transcription
    transcription = transcribe(wav_file_path)

    if not transcription:
        logging.warning("No transcription available.")
        return del_file_path

    save_transcription(file_path, "", transcription)

    # Format the transcription
    try:
        formatted_transcription = format_assistant(transcription)
    except Exception as e:
        logging.error(f"Error during formatting: {e}")
        raise

    logging.info(f"formatted is '{formatted_transcription}'")

    if not formatted_transcription:
        logging.warning("No formatted transcription available.")
        return del_file_path
    
    # Save the formatted transcription to a file
    save_transcription(file_path, "-formatted", formatted_transcription)

    return del_file_path
	
if __name__ == "__main__":
    if len(sys.argv) != 2:
        logging.error("Invalid number of arguments. Usage: python main.py <audio_file_path>")
        sys.exit(1)
    
    audio_file_path = sys.argv[1]

    try:
        gen_wav_path = transcribe_audio(audio_file_path)
        
        # Delete the generated WAV file
        if gen_wav_path:
            delete_generated_wav_file(gen_wav_path)

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    sys.exit(1)