#!/usr/bin/env python3
import argparse
import codecs
import fnmatch
import os
import re

__author__ = 'Ingvaras Merkys'
__version__ = '1'


def main(path: str, file_name: str = None, recursive: bool = False) -> None:
    """
    Traverse through the given path and check all the files with matching file_name (shell-style pattern)
    :param recursive:
    :param path:
    :param file_name:
    :return:
    """
    regex = fnmatch.translate(file_name)
    reobj = re.compile(regex)
    for root, _, files in (os.walk if recursive else (lambda x: map(lambda y: (x, None, [y]), os.listdir(x))))(path):
        for file in files:
            if file_name is None or reobj.match(file):
                file_path = os.path.join(os.path.abspath(root), file)
                errors = []
                if not is_utf8(file_path):
                    errors.append('invalid UTF-8')
                if not is_lf_ending(file_path):
                    errors.append('non-LF endings')
                if len(errors) > 0:
                    print(file_path + '\t' + '; '.join(errors))


def is_utf8(file_path: str) -> bool:
    """
    Checks if file is in UTF-8 encoding
    :param file_path:
    :return:
    """
    try:
        f = codecs.open(file_path, encoding='utf-8', errors='strict')
        for _ in f:
            pass
    except UnicodeDecodeError:
        return False
    return True


def is_lf_ending(file_path: str) -> bool:
    """
    Checks if file uses LF line separators
    :param file_path:
    :return:
    """
    return b'\r' not in open(file_path, 'rb').read()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='List non UTF-8 files and files with non LF line endings.')
    parser.add_argument('path', help='file with changes or pages to activate', type=str)
    parser.add_argument('file_name', help='file name (shell-style pattern)', type=str)
    parser.add_argument('-r', help='traverse the path recursively', action='store_true', default=False)
    args = parser.parse_args()

    main(args.path, args.file_name, args.r)
