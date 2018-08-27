import sounddevice as sd
import soundfile as sf
import tempfile
import queue
import boto3
import keyboard
import sys
import time

def callback(indata, frames, time, status):
    global q
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

def start_command():
    global q
    q = queue.Queue()
    filename = tempfile.mktemp(prefix='slash_rec_', suffix='.wav', dir='') # FIXME allegedly unsafe
    with sf.SoundFile(filename, mode='x', samplerate=sd.default.samplerate, channels=sd.default.channels[0], subtype='PCM_16') as file:
        with sd.InputStream(samplerate=sd.default.samplerate, device=sd.default.device[0], channels=sd.default.channels[0], callback=callback):
            while keyboard.is_pressed('-'):
                file.write(q.get())
    response = lex.post_content(
        botName='SlashEmote',
        botAlias='Dev',
        userId='slashUser', # everyone is same user, fine for now.
        contentType='audio/l16; rate=16000; channels=1',
        accept='text/plain; charset=utf-8',
        inputStream=open(filename, 'rb')
    )
    print(response)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        # TODO Handle case where 'inputTranscript' is empty string; message is populated.
        keyboard.write('\n/{0}\n'.format(response['inputTranscript']))
    else:
        print("Issue with Lex") # TODO Handle failures differently

sd.default.samplerate = 16000
sd.default.channels = 1
lex = boto3.client('lex-runtime', 'us-east-1')
keyboard.add_hotkey('alt+-', start_command)
keyboard.wait() # Ctrl+C to kill