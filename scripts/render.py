#!/usr/bin/env python3
import argparse
import dataclasses
from os.path import join, relpath, basename
import sqlite3
from typing import List

import markdown2


@dataclasses.dataclass
class Args:
    input_file: str
    output_file: str
    docset_dir: str

    @staticmethod
    def parse() -> 'Args':
        args = argparse.ArgumentParser()
        args.add_argument('--in', dest='input_file', required=True)
        args.add_argument('--out', dest='output_file', required=True)
        args.add_argument('--docset', dest='docset_dir', required=True)
        args = args.parse_args()
        return Args(
            input_file=args.input_file,
            output_file=args.output_file,
            docset_dir=args.docset_dir,
        )


def main():
    args = Args.parse()

    with open(args.input_file, 'r') as fp:
        input_data = fp.read()

    body = markdown2.markdown(
        text=input_data,
        extras=[
            'fenced-code-blocks',
            'header-ids',
            'metadata',
            'tables',
        ])

    html = f'''
        <html>
            <head></head>
            <body>
                {body}
            </body>
        </html>
    '''

    with open(args.output_file, 'w') as fp:
        fp.write(html)

    write_db(
        join(args.docset_dir, 'Contents/Resources/docSet.dsidx'),
        [
            Entry(
                name=basename(args.output_file),
                type='Guide',
                relative_path=relpath(
                    args.output_file,
                    join(args.docset_dir, 'Contents/Resources/Documents'),
                ),
            ),
        ]
    )


@dataclasses.dataclass
class Entry:
    name: str
    type: str
    relative_path: str


def write_db(db_path: str, index: List[Entry]):
    with sqlite3.connect(db_path, timeout=30.0) as conn:
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT)')
        c.execute('CREATE UNIQUE INDEX IF NOT EXISTS anchor ON searchIndex (name, type, path)')
        c.executemany(
            '''INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?, ?, ?)''',
            [(entry.name, entry.type, entry.relative_path) for entry in index])
        conn.commit()


if __name__ == '__main__':
    main()
