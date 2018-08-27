import boto3
import json
import requests
import zipfile
import io
import sys

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

lex = boto3.client('lex-models', 'us-east-1')

export_resource('SlashEmote','BOT','LEX')
export_resource('EmoteIntent','INTENT','LEX')
export_resource('Emotes','SLOT_TYPE','LEX')
