#!/bin/bash

# REF:
#   - https://github.com/silnrsi/oxttools/blob/master/docs/USAGE.md
#   - https://www.systutorials.com/docs/linux/man/4-hunspell/
#   - $ man 5 hunspell
#   - $ man hunspell
#   - $ hunspell -h


show_usage() {
    echo "usage: $0 [-h] | [-d /PATH/TO/DESCRIPTION.XML] [-D /PATH/TO/DICTIONARIES.XCU] AFF_FILE"
}

while getopts ":d:D:h" o; do
    case "${o}" in
        d)
            desc_str="$OPTARG"
            desc_file="$(realpath "$desc_str")"
            ;;
        D)
            dict_str="$OPTARG"
            dict_file="$(realpath "$dict_str")"
            ;;
        h)
            show_usage
            exit 0
            ;;
        *)
            show_usage
            exit 1
            ;;
    esac
done
shift $((OPTIND-1))

# Possible OXT dir locations:
#   - parent of AFF file
#   - PWD
if [[ -n $1 ]]; then # check 1st argument
    aff_file="$(realpath "$1")" # also tests if file exists
    if [[ $? -ne 0 ]]; then
        exit 1
    fi
    aff_file_parent="$(dirname "$aff_file")"
    if [[ $aff_file =~ .*\.aff$ && -r $aff_file && -d $aff_file_parent ]]; then
        oxt_dir="$aff_file_parent"
    else
        echo "Error: Not a valid AFF file: $1"
        exit 1
    fi
elif [[ -n $(find "$PWD" -maxdepth 1 -name '*.aff') ]]; then # check PWD
    oxt_dir="$PWD"
    aff_file=$(find "$PWD" -maxdepth 1 -name '*.aff' | head -n1)
else
    echo "Error: No AFF file given nor found in $PWD"
    exit 1
fi

yyyy=$(date +%Y)
# today=$(date +%Y%m%d)
ver=$(date +%Y.%m.%d)

name=$(basename "$oxt_dir")
# langtag=$(echo "$name" | awk -F'_' '{print $1}')
langtag=$(basename "$aff_file")
langtag=${langtag%.aff}
lang=$(echo "$name" | awk -F'_' '{print $2}')

oxt_file="${oxt_dir}/dict-${lang}-v${ver}.oxt"

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

# Update description.xml.
if [[ -n $desc_file ]]; then # use provided file
    # Copy file.    
    cp "$desc_file" "$temp_dir"
    # Update version string in copied description.xml.
    xmlstarlet edit -L -N ns="http://openoffice.org/extensions/description/2006" \
        -N xlink="http://www.w3.org/1999/xlink" \
        --update "//ns:description/ns:version/@value" --value "$ver" \
        "${temp_dir}/$(basename "$desc_file")"
else # modify generated file
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
    display_en="Sango Spell Checker (1984)"
    xmlstarlet edit -L -N ns="http://openoffice.org/extensions/description/2006" \
        --update "//ns:description/ns:display-name/ns:name[@lang='en']" --value "$display_en" \
        "description.xml"
    display_fr="Correcteur d'orthographe, sango (1984)"
    xmlstarlet edit -L -N ns="http://openoffice.org/extensions/description/2006" \
        --append "//ns:description/ns:display-name/ns:name[@lang='en']" \
            --type elem --name "name" --value "$display_fr" \
        --insert '$prev' --type attr --name "lang" --value "fr" \
        "description.xml"
fi

# Update dictionaries.xcu.
if [[ -n "$dict_file" ]]; then
    # Copy file.    
    cp "$dict_file" "$temp_dir"
fi

# Add updated file(s) into OXT.
if [[ -f "description.xml" ]]; then
    zip "$oxt_file" "description.xml"
fi
if [[ -f "dictionaries.xcu" ]]; then
    zip "$oxt_file" "dictionaries.xcu"
fi
cp "${oxt_dir}/LICENSES-fr.txt" "$temp_dir"
zip "$oxt_file" "LICENSES-fr.txt"

# Remove temp folder.
if ! cd "$oxt_dir"; then
    echo "Error: Failed to enter $oxt_dir."
    exit 1
fi
rm -r "$temp_dir"
