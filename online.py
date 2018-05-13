# -*- coding: utf-8 -*-
"""
    online
    ~~~~~~~~~~~~~~~~~~~~~
    Compile a letter online.

    :copyright: (c) 2018 YtoTech.
"""
import click
import requests
import base64
import codecs
import os
from shutil import which
from subprocess import call

CLOUD = 'https://latex.ytotech.com'

def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
    return which(name) is not None

def openPdf(pdfPath):
    # Automatically open the PDF after edition
    # (TODO intelligent & configurable guess. See for libs.).
    if is_tool('xdg-open'):
        call(['xdg-open', pdfPath])
    elif is_tool('evince'):
        call(['evince', pdfPath])
    elif is_tool('start'):
        call(['start', pdfPath])
    else:
        print('Nothing found to auto-open the PDF')

def getFileContentBase64(path):
    print(path)
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def latexToPdf(latex):
    # Use Xetex soo we can use host system fonts.
    r = requests.post(
        CLOUD + '/compilers/latex',
        json={
            'compiler': 'xelatex',
            'resources': [
                {
                    'content': latex,
                    'main': True
                }
            ]
        }
    )
    if r.status_code != 201:
        print(r.status_code)
        if r.status_code == 400:
            payload = r.json()
            print(payload['code'])
            with open('./api.log', 'w') as f:
                f.write(payload['logs'])
            raise RuntimeError("Compilation Error: logs on api.log")
        else:
            print(r.text)
            raise RuntimeError("API Error")
    # TODO Check Content-Type
    return r.content

# CLI declaration.
@click.group()
@click.option('-v', '--verbose', default=False, help='Verbose mode')
def cli(verbose):
    print('Verbose mode is {0}'.format('on' if verbose else 'off'))

@cli.command()
@click.argument('input')
@click.argument('output')
def compile(input, output):
    print('Compiling {} to {}'.format(input, output))
    # Use Yaml.
    with codecs.open(input, 'r', 'utf-8') as f:
        content = f.read()
    print('Generating PDF with Fire Latex API...')
    print('(take time)')
    pdf = latexToPdf(content)
    if os.path.isfile(output):
        os.remove(output)
    with open(output, 'wb') as f:
        f.write(pdf)
    print('New generated PDF is ready in {}...'.format(output))
    openPdf(output)

if __name__ == '__main__':
    cli()
