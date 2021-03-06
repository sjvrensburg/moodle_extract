# extract_moodle

A simple tool to extract the original files from a [Moodle](https://moodle.org/) course backup archive.

## What is this?

`extract_moodle` is a terminal utility written in Python. It extracts all files from the course backup file created by Moodle.

## Why do you need this?

It is possible that you no longer have access to the original files uploaded to Moodle. This may happen if you or the original author failed to make backups of those files.

## Installation

The recommended method of installation is via [pipx](https://pypa.github.io/pipx/):

```bash
pipx install git+https://github.com/sjvrensburg/moodle_extract
```

## How do I use this?

If `my_mmodle_backup.mbz` is the Moodle course backup file then simply run the following command from the terminal:

```bash
extact_moodle my_mmodle_backup.mbz
```

This will create a subdirectory in your current working directory. The name of this subdirectory is the short-name of the course. You will find your files within the subdirectories of that folder.

## Acknowledgements

This tool is based on the [moodle-course-backup-file-extractor](https://github.com/shcgitpf/moodle-course-backup-file-extractor) PowerShell script. Many thanks to [shcgitph](https://github.com/shcgitpf), who wrote that script.
