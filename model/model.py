import boto3
import json
import requests
import zipfile
import io
import sys
import os

BOT_NAME = 'SlashEmote'
INTENT_NAME = 'EmoteIntent'
SLOT_TYPE_NAME = 'Emotes'

def export_resource(name, resourceType, exportType, version):
    response = lex.get_export(
        name=name,
        resourceType=resourceType,
        exportType=exportType,
        version=version
    )
    r = requests.get(response['url'], stream=True)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall()
    
def import_resource(name, resourceType, mergeStrategy='OVERWRITE_LATEST'):
    file_name = name + '_Export.json'
    zip_name = file_name + '.zip'
    zipfile.ZipFile(zip_name, mode='w').write(file_name)
    response = lex.start_import(
        payload=open(zip_name, 'rb').read(),
        resourceType=resourceType,
        mergeStrategy=mergeStrategy
    )
    os.remove(zip_name)
    print(response)

if len(sys.argv) != 2:
    print("Usage: {0} (import/export)", file=sys.stderr)

lex = boto3.client('lex-models', 'us-east-1')

cmd = sys.argv[1].lower()
if cmd == 'import':
    import_resource(BOT_NAME,'BOT')
    import_resource(INTENT_NAME,'INTENT')
    import_resource(SLOT_TYPE_NAME,'SLOT_TYPE')
elif cmd == 'export':
    bots = lex.get_bot_versions(name=BOT_NAME)['bots']
    export_resource(BOT_NAME,'BOT','LEX', bots[-1]['version'])
    intents = lex.get_intent_versions(name=INTENT_NAME)['intents']
    export_resource(INTENT_NAME,'INTENT','LEX', intents[-1]['version'])
    slotTypes = lex.get_slot_type_versions(name=SLOT_TYPE_NAME)['slotTypes']
    export_resource(SLOT_TYPE_NAME,'SLOT_TYPE','LEX', slotTypes[-1]['version'])
else:
    print("Usage: {0} (import/export)", file=sys.stderr)
