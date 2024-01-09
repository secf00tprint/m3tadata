import subprocess
import re

output = subprocess.check_output("exiftool *.pdf", shell=True, universal_newlines=True)

splitted_output = output.split("\n")

### Replace similar tags with same tags

TO_REPLACELIST=["Creator Tool","History Software Agent"]
replaced_output = []

for line in splitted_output:
    to_append=line
    first_substring = line.split(":")[0]
    for repl_string in TO_REPLACELIST:
        if (first_substring.lower().startswith(repl_string.lower())):
            substring_len=len(first_substring)
            to_replace = re.compile(re.escape(repl_string), re.IGNORECASE)
            to_append=to_replace.sub("Creator" + " " * (len(first_substring)-len("Creator")), first_substring)
            to_append = to_append+line[line.index(":")+1]
    replaced_output.append(to_append)

##### Sort out unnecessary stuff

VERSION_BLOCKLIST=["File","ExifTool Version Number"]

unique_lines = list(set(replaced_output))
filtered_unique_lines = []

for line in unique_lines:
    if re.search('[0-9]+\.[0-9]+\.?[0-9]*',line): # Check for versions
        # Don't show items in block list - case insensitive
        if not any(string.lower() in line.lower() for string in VERSION_BLOCKLIST):
            filtered_unique_lines.append(line)

### Output amounts

counts={}
for line in filtered_unique_lines:
    counts[line]=replaced_output.count(line)

sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)

for line, count in sorted_counts:
    print(f"{count}: {line}")
