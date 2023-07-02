#!/usr/bin/env bash

# Set XML fields according to current date.
# Add the correct files & zip.
# Save as OXT.

script="$(realpath "$0")"
scripts_dir="$(dirname "$script")"
repo_dir="$(dirname "$scripts_dir")"
base_dir="${repo_dir}/sg-CF_sango-1984"

yyyy=$(date +%Y)
mm=$(date +%m)
dd=$(date +%d)
version="${yyyy}.${mm}.${dd}"
base_name="dict-sango-1984"
outfilename="${base_name}-${yyyy}${mm}${dd}_lo.oxt"

if [[ ! -d "${base_dir}/${base_name}" ]]; then
    echo "Error: Directory does not exist: ${base_dir}/${base_name}"
    exit 1
fi

# Set date on copyright of LICENSE.txt.
sed -i -r "s/(© )[0-9]{4}/\1${yyyy}/" "${base_dir}/${base_name}/LICENSE.txt"

# Set version in description.xml.
#   Ref: https://stackoverflow.com/a/67411093
xmlstarlet edit -L -S \
    -u "//*[local-name()='version']/@value" -v "$version" \
    "${base_dir}/${base_name}/description.xml"

# Create zipped file.
cd "${base_dir}/${base_name}" || exit 1
cp ../sg-CF.aff ./dictionaries
cp ../sg-CF.dic ./dictionaries
rm -f ../"$outfilename"
zip -qr ../"$outfilename" ./*
