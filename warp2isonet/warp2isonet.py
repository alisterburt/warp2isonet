import numpy as np
import typer
import starfile
import pandas as pd
from rich.console import Console
from pathlib import Path
from .utils import get_tomograms, get_zero_degree_xml_files, \
    defocus_from_xml, match_tomograms_to_xml_files, pixel_size_from_tomogram

cli = typer.Typer()


@cli.command()
def warp2isonet(warp_processing_directory: Path = Path()):
    """This line is the docstring of single_command"""
    console = Console(record=True)
    console.log(
        f'[bold green]preparing files from {warp_processing_directory} for '
        f'isonet! :rocket:'
    )
    # Get tomograms
    tomograms = get_tomograms(warp_processing_directory)
    xml_files = get_zero_degree_xml_files(warp_processing_directory)

    # Match tomograms to xml files
    tomo2xml = match_tomograms_to_xml_files(tomograms, xml_files)

    # Get defocus values
    xml2defocus = {xml: defocus_from_xml(xml) for xml in xml_files}
    tomo2defocus = {t: xml2defocus[tomo2xml[t]] for t in tomograms}

    # Construct dataframe
    data = {
        'rlnIndex': np.arange(len(tomograms)),
        'rlnMicrographName': tomograms,
        'rlnPixelSize': [pixel_size_from_tomogram(t) for t in tomograms],
        'rlnDefocus': [tomo2defocus[t] for t in tomograms],
        'rlnNumberSubtomo': [int(1000 / len(tomograms)) for _ in tomograms],
    }
    df = pd.DataFrame.from_dict(data)
    output_filename = 'isonet_input.star'
    starfile.write(df, output_filename, overwrite=True)

    console.log(f'[blue underline]done!')
    logfile_name = f'warp2isonet.html'
    console.save_html(logfile_name)
    console.log(f'html output saved in [bold green]{logfile_name}')


if __name__ == '__main__':
    warp2isonet('../example_data')


