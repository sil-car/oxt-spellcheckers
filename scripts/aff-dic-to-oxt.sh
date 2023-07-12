#!/bin/bash

# REF:
#   - https://github.com/silnrsi/oxttools/blob/master/docs/USAGE.md
#   - https://www.systutorials.com/docs/linux/man/4-hunspell/
#   - $ man 5 hunspell
#   - $ man hunspell
#   - $ hunspell -h

script_path="$(realpath "$0")"
script_dir_path="$(dirname "$script_path")"
aff_dir=$(realpath "$PWD")
if [[ -z $(find "$aff_dir" -name '*.aff') ]]; then
    echo "Error: No AFF file found in $aff_dir."
    exit 1
fi

yyyy=$(date +%Y)
today=$(date +%Y%m%d)
ver=$(date +%Y.%m.%d)

name=$(basename "$aff_dir")
langtag=$(echo "$name" | awk -F'_' '{print $1}')
lang=$(echo "$name" | awk -F'_' '{print $2}')

oxt_file="${aff_dir}/dict-${lang}-${today}_lo.oxt"

for f in "${langtag}.aff" "LICENSE.txt"; do
    if [[ ! -f "$f" ]]; then
        echo "Error: File not found: $f"
        exit 1
    fi
done

# Set date on copyright of LICENSE.txt.
sed -i -r "s/(© )[0-9]{4}/\1${yyyy}/" "${aff_dir}/LICENSE.txt"

makeoxt \
    --dict "${aff_dir}/${langtag}.aff" \
    --langname "$lang" \
    --license "${aff_dir}/LICENSE.txt" \
    --norm None \
    --publisher "SIL International (nate_marti@sil.org)" \
    --puburl "https://github.com/sil-car/oxt-spellcheckers" \
    --type west \
    --version "$ver" \
    "$langtag" "$oxt_file"

# Update details in description.xml, extracting into temp folder.
temp_dir=$(mktemp -d)
if ! cd "$temp_dir"; then
    echo "Error: Failed to enter $temp_dir."
    exit 1
fi
unzip "$oxt_file"

# Add French display name.
display="Correcteur d'orthographe sango-1984"
xmlstarlet edit -L -N ns="http://openoffice.org/extensions/description/2006" \
    -a "//ns:description/ns:display-name/ns:name[@lang='en']" -t elem -n "name" -v "$display" \
    -i '$prev' -t attr -n "lang" -v "fr" \
    "description.xml"

# Add updated file(s) into OXT and remove temp folder.
zip "$oxt_file" "description.xml"
if ! cd "$aff_dir"; then
    echo "Error: Failed to enter $aff_dir."
    exit 1
fi
rm -r "$temp_dir"
