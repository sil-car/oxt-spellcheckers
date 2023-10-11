#!/bin/bash

# REF:
#   - https://github.com/silnrsi/oxttools/blob/master/docs/USAGE.md
#   - https://www.systutorials.com/docs/linux/man/4-hunspell/
#   - $ man 5 hunspell
#   - $ man hunspell
#   - $ hunspell -h

script_path="$(realpath "$0")"
script_dir_path="$(dirname "$script_path")"

# Possible OXT dir locations:
#   - parent of AFF file in 1st argument
#   - PWD
if [[ -n $1 ]]; then # check 1st argument
    infile="$(realpath "$1")" # also tests if file exists
    if [[ $? -ne 0 ]]; then
        exit 1
    fi        
    infile_parent="$(dirname "$infile")"
    if [[ $infile =~ .*\.aff$ && -r $infile && -d $infile_parent ]]; then
        oxt_dir="$infile_parent"
    else
        echo "Error: Not a valid AFF file: $1"
        exit 1
    fi
elif [[ -n $(find "$PWD" -maxdepth 1 -name '*.aff') ]]; then # check PWD
    oxt_dir="$PWD"
else
    echo "Error: No AFF file given nor found in $PWD"
    exit 1
fi
# oxt_dir=$(realpath "$PWD")
# if [[ -z $(find "$oxt_dir" -maxdepth 1 -name '*.aff') ]]; then
#     echo "Error: No AFF file found in $oxt_dir."
#     exit 1
# fi

yyyy=$(date +%Y)
today=$(date +%Y%m%d)
ver=$(date +%Y.%m.%d)

name=$(basename "$oxt_dir")
langtag=$(echo "$name" | awk -F'_' '{print $1}')
lang=$(echo "$name" | awk -F'_' '{print $2}')

oxt_file="${oxt_dir}/dict-${lang}-${today}_lo.oxt"

license_names=()
for lg in "en" "fr"; do
    license_names+=( "LICENSES-${lg}.txt" )
done
for n in "${langtag}.aff" "${license_names[@]}"; do
    f="${oxt_dir}/${n}"
    if [[ ! -f $f ]]; then
        echo "Error: File required but not found: $f"
        exit 1
    fi
done

# Set date on copyright of LICENSE.txt.
for n in "${license_names[@]}"; do
    f="${oxt_dir}/${n}"
    sed -i -r "s/(© )[0-9]{4}/\1${yyyy}/" "$f"
done

makeoxt \
    --dict "${oxt_dir}/${langtag}.aff" \
    --langname "$lang" \
    --license "${oxt_dir}/LICENSES-en.txt" \
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

# Add reference to French LICENSE file.
xmlstarlet edit -L -N ns="http://openoffice.org/extensions/description/2006" \
    -N xlink="http://www.w3.org/1999/xlink" \
    --append "//ns:description/ns:registration/ns:simple-license/ns:license-text[@lang='en']" \
        --type elem --name "license-text" \
    --var new '$prev' \
    --insert '$new' --type attr --name "xlink:href" --value "LICENSES-fr.txt" \
    --insert '$new' --type attr --name "lang" --value "fr" \
    "description.xml"

# Update display names.
display_en="Sango-1984 Spell Checker"
xmlstarlet edit -L -N ns="http://openoffice.org/extensions/description/2006" \
    --update "//ns:description/ns:display-name/ns:name[@lang='en']" --value "$display_en" \
    "description.xml"
display_fr="Correcteur d'orthographe sango-1984"
xmlstarlet edit -L -N ns="http://openoffice.org/extensions/description/2006" \
    --append "//ns:description/ns:display-name/ns:name[@lang='en']" \
        --type elem --name "name" --value "$display_fr" \
    --insert '$prev' --type attr --name "lang" --value "fr" \
    "description.xml"

# Add updated file(s) into OXT.
zip "$oxt_file" "description.xml"
cp "${oxt_dir}/LICENSES-fr.txt" "$temp_dir"
zip "$oxt_file" "LICENSES-fr.txt"

# Remove temp folder.
if ! cd "$oxt_dir"; then
    echo "Error: Failed to enter $oxt_dir."
    exit 1
fi
rm -r "$temp_dir"
