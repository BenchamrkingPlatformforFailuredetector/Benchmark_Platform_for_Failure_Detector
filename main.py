import argparse

from run import run_all

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--lang', help='language file', required=True)
parser.add_argument('-r', '--rec', help='record class', default='record')
args = parser.parse_args()
lang_file = args.lang
rec_cls = args.rec

try:
    print(f"You choose FD '{lang_file}' using record class '{rec_cls}'")
    # run_all(lang_file, rec_cls)
except Exception as e:
    print(e)
