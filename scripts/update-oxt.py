#!/usr/bin/env python3
""" This script assumes an already-prepared folder with the OXT file's contents
    inside. It updates the contents and exports a compressed OXT file.
    For creating a new OXT file, see the 'makeoxt' command from
    https://github.com/ilnrsi/oxttools.
"""
# REF:
#   - https://github.com/silnrsi/oxttools/blob/master/docs/USAGE.md
#   - https://www.systutorials.com/docs/linux/man/4-hunspell/
#   - $ man 5 hunspell
#   - $ man hunspell
#   - $ hunspell -h

import argparse
import datetime
import re
import tempfile
import zipfile
from lxml import etree
from pathlib import Path


def check_suffix(file_path, ext):
    file_path = Path(file_path)
    if not ext.startswith('.'):
        ext = f".{ext}"
    return file_path.suffix == ext


def get_oxt_root(oxt_path, src_dir):
    if oxt_path.is_file():
        tempdir = tempfile.TemporaryDirectory()
        oxt_root = Path(tempdir.name)
        with zipfile.ZipFile(oxt_path, mode='r') as z:
            z.extractall(path=oxt_root)
        return oxt_root, tempdir
    else:
        return src_dir / 'oxt_root', None


def update_updates_xml(file_path, new_version):
    # Update version number.
    xml_tree = etree.parse(file_path)
    xml_root = xml_tree.getroot()
    xml_version = xml_root.find('version', xml_root.nsmap)
    if xml_version.get('value') != new_version:
        xml_version.attrib['value'] = new_version
        file_path.write_bytes(etree.tostring(xml_tree, pretty_print=True))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'DIC_FILE', nargs=1, type=Path,
        help="path to dictionary or affixes file",
    )

    # Check args.
    args = parser.parse_args()
    dic_path = args.DIC_FILE[0]
    if not check_suffix(dic_path, 'aff') and not check_suffix(dic_path, 'dic'):
        print(f"Error: invalid dictionary or affixes file: {dic_path}")
        exit(1)

    # Set variables.
    repo_dir = Path(__file__).parents[1]
    src_dir = dic_path.parent
    variant = src_dir.name.split('-')[-1]  # "1984" or "simple"

    now = datetime.datetime.now()
    yyyy = str(now.year)
    version = f"{now.year}.{now.month}.{now.day}"
    name = dic_path.parent.name
    # NOTE: lantag is hard-coded b/c of special lang tag given to Sango simple
    # spellchecker: sg-CM.
    langtag = 'sg-CF'  # dic_path.stem
    lang = name.split('_')[1]

    dist_dir = repo_dir / 'updates'
    oxt_path = dist_dir / f'dict-{lang}.oxt'
    oxt_root, tempdir = get_oxt_root(oxt_path, src_dir)

    # Update copyright year on LICENSE files.
    for n in [f'LICENSE-{lg}.txt' for lg in ['en', 'fr']]:
        file_path = oxt_root / n
        new_path = file_path.with_suffix('.bak')
        with file_path.open() as fh:
            with new_path.open('w') as nh:
                for line in fh:
                    sub = re.sub(r'(?<=© )[0-9]{4}', yyyy, line)
                    if sub:
                        out_line = sub
                    else:
                        out_line = line
                    nh.write(out_line)
        new_path.rename(file_path)

    # Update version number in description.xml.
    desc_xml = oxt_root / 'description.xml'
    xml_tree = etree.parse(desc_xml)
    xml_root = xml_tree.getroot()
    xml_version = xml_root.find('version', xml_root.nsmap)
    if xml_version.get('value') != version:
        xml_version.attrib['value'] = version
        desc_xml.write_bytes(etree.tostring(xml_tree, pretty_print=True))

    # Build OXT archive.
    with zipfile.ZipFile(oxt_path, mode='w', compression=zipfile.ZIP_DEFLATED) as z:  # noqa: E501
        # Add in all files from oxt_root.
        for (dpath, dnames, fnames) in oxt_root.walk():
            for n in fnames:
                if n[-4:] in ['.aff', '.dic']:
                    continue
                fpath = dpath / n
                print(f"Adding to OXT: {fpath}")
                z.write(fpath, arcname=fpath.relative_to(oxt_root))
        # Add in dictionary & affix files.
        for f in src_dir.iterdir():
            if f.suffix in ['.aff', '.dic']:
                print(f"Adding to OXT: {f}")
                z.write(f, arcname=f'dictionaries/{f.name}')

    if tempdir:
        tempdir.cleanup()

    update_updates_xml(
        dist_dir / f"org.sil.{langtag}.spellcheck-{variant}.updates.xml",
        version
    )


if __name__ == '__main__':
    main()
