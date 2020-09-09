# suso_print_survey
Survey Solutions print survey

This code processes the exported data from [Survey Solutions](https://mysurvey.solutions) to build a consolidated report containing all answers from all interviews.

Stata 16.0 and Python are required.

The code is experimental and will most likely require you to make additions/edits depending on your situation.

Basic syntax is shown in the `code/demo.do` file. The progress looks like this:
![The progress looks like this](https://raw.githubusercontent.com/radyakin/suso_print_survey/master/images/suso_print_svy.png)
The output looks like this
![The output looks like this](https://raw.githubusercontent.com/radyakin/suso_print_survey/master/images/output.png)
[Example output](https://github.com/radyakin/suso_print_survey/raw/master/output/ACCOMMODATION_ATTRACTIONS_AC.pdf) in the output folder.


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
