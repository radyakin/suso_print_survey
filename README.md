# suso_print_survey
Survey Solutions print survey

This code processes the exported data from Survey Solutions to build a consolidated report containing all answers from all interviews.

Stata 16.0 and Python are required.

The code is experimental and will most likely require you to make additions/edits depending on your situation.

Basic syntax is shown in the `code/demo.do` file.
Example output in the output folder.

### Known issues

- rosters
- particular question types:
    - linked questions,
    - ordered multiselect questions,
    - picture questions,
    - audio questions,
- dollar-globals,
- %-substitutions

### Possible expansions

- support date/time formats;
- GPS to show map image.

### Additionally requires

- bleach,
- webencodings,
- packaging.
