# gen-clean-shed

This is a simple script I wrote to generate a cleaning schedule. It may be useful to you when you live in a shared household.

At the moment only one pattern, i.e. division of chores per week, is supported. More specifically this means that all generated schedules contain 4 different chores, 2 of which return every week while the other 2 alternate between the weeks. As you probably want something different, you'll have to modify the script.

## Usage

First, set the variables at the top of the `gen_clean_shed.py`. Example values are provided in the source.

| variable          | meaning |
| ----------------- | ------- |
| `year`            | year of the schedule |
| `switch_week`     | week to switch turns |
| `output_format`   | can be either `csv` or `latex` |
| `filename`        | filename of output |


The following variables are only used for LaTeX output.

| variable          | meaning |
| ----------------- | ------- |
| `language`        | can be either `en` or `nl` |
| `holiday_weeks`   | weeks to highlight (optional) |
| `filename_header` | filename of the header |
| `filename_footer` | filename of the footer |

Now simply run `python3 gen_clean_shed.py` and it will produce an output file.

## Output format

Two output formats are supported: CSV and LaTeX.

### CSV

This writes every week to a line in a comma-separated value file. It is the format that is expected by [cleaning-bot](https://github.com/flatraad/cleaning-bot).
The output will look something like this:
```
1,D,A,,B
2,F,,G,H
3,C,D,,A
...
```

Empty fields signify that the chore is not available in that week.

### LaTeX

In this mode the script will generate a LaTeX source file (a `.tex` file). To this end it concatenates the file pointed to by `filename_header` with the content and lastly with the file `filename_footer`.

The result will be a table in with descriptions and dates. The rows corresponding to the weeknumbers in `holiday_weeks` will be highlighted. The descriptions are defined in the files `strings-en.dict` and `strings-nl.dict`, depending on the `language` setting.

The easiest way to get an idea of what this mode entails, is to simply try it.
Since the output file is a source file to LaTeX, it needs to be compiled with `pdflatex` or another engine to produce a PDF.

## Possible improvements

* use command-line arguments instead of hardcoding settings
* specify range of week numbers
* variable amount of rooms
* allow different patterns
* LaTeX integration (e.g. autocompilation)

Note: I am no longer using this script, so don't expect any of this being implemented anytime soon.
