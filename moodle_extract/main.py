from rich import console
import untangle
import click
from typing import Tuple, List
from tempfile import TemporaryDirectory
from shutil import unpack_archive, copyfile
from os.path import join, isdir
from os import makedirs, getcwd
from rich.progress import track
from rich.console import Console


def shortname(fname: str) -> str:
    """
    shortname(fname: str) -> str

    Extract the short-name of the course from the file `fname`.

    ARGUMENTS:
    fname:  String giving the path to the XML file. This file is typically
            called moodle_backup.xml

    RETURNS:
    A string containing the short-name of the course.    
    """
    obj = untangle.parse(fname)
    sname = obj.moodle_backup.information.original_course_shortname.cdata
    return sname


def parse(fname: str) -> List[Tuple[str,str]]:
    """
    parse(fname: str) -> List[Tuple[str,str]]

    Parses the XML file `fname` and extracts paths to files in the archive and
    the original file name. These are then processed into input and output
    paths for copying extracted files.

    ARGUMENTS:
    fname:  String giving the path to the XML file. This file is typically
            called files.xml

    RETURNS:
    A list of tuples, where each tuple contains the source and destination
    path for files in the archive.
    """
    obj = untangle.parse(fname)
    results = [(
        file.contenthash.cdata, # defines both dir and file name in archive
        file.filearea.cdata,    # logical to use this as a new directory
        file.filename.cdata     # original file name
        ) for file in obj.files.file]
    ans = [(
        'files/{}/{}'.format(x[0][0:2], x[0]),   # path to file in archive
        '{}/{}'.format(x[1], x[2])         # output path
        ) for x in results]
    return ans

@click.command()
@click.argument('fname')
def moodle_extract(fname: str):
    """
    moodle_extract(fname: str)
    
    Extacts the files inside of the Moodle backup file, `fname`.

    ARGUMENTS:
    fname:  String giving the path to the XML file. This file is typically
            called files.xml
    
    DETAILS:
    The function extacts the files to the current directory. It creates
    subdirectories according to the "filearea" element associated with
    file in the archive. This does not necessarily result in a logical
    directory structure.
    """

    console = Console()
    cwd = getcwd()
    
    with TemporaryDirectory() as tmp_dir:
        # Extract the files to temporary directory.
        unpack_archive(fname, extract_dir=tmp_dir, format='gztar')
        sname = shortname(join(tmp_dir, 'moodle_backup.xml'))
        paths = parse(join(tmp_dir, 'files.xml'))
        count = 0
        for path in track(paths):
            path = (path[0], f'{sname}/{path[1]}')
            dname = path[1].split('/')
            dname = f'{dname[0]}/{dname[1]}'
            if not isdir(dname):
                makedirs(join(cwd, dname))
            try:
                copyfile(join(tmp_dir, path[0]), path[1])
            except FileNotFoundError:
                count += 1
        
    if count > 0:
        msg = f'{count} file/s not found.'
        console.print(
            f'\n[bold red]WARNING![/bold red]\t{msg}\nThese are often just empty files, so you probably don\'t have to worry about it.\n')
    msg = f'Extracted {len(paths)-count} of {len(paths)} files'
    console.print(f'[bold green]DONE![/bold green]\t\t{msg} :smile:')
