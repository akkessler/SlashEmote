import boto3
import json
import requests
import zipfile
import io
import sys
import os

def export_resource(name, resourceType, exportType, version='1'):
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
    # import_resource('SlashEmote','BOT')
    # import_resource('EmoteIntent','INTENT')
    import_resource('Emotes','SLOT_TYPE')
elif cmd == 'export':
    export_resource('SlashEmote','BOT','LEX')
    export_resource('EmoteIntent','INTENT','LEX')
    export_resource('Emotes','SLOT_TYPE','LEX')
else:
    print("Usage: {0} (import/export)", file=sys.stderr)
