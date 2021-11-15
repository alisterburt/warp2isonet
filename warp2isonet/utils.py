from .warp_xml_handling import xml2dict
from pathlib import Path
from thefuzz import process, fuzz
import re


def defocus_from_xml(xml):
    data = xml2dict(xml)
    return float(data['Movie']['CTF']['Defocus'])


def get_tomograms(dir):
    reconstruction_dir = Path(dir) / 'reconstruction'
    return list(reconstruction_dir.glob('*.mrc'))


def get_zero_degree_xml_files(dir):
    return list(Path(dir).glob('*-0.0.xml'))


def match_tomograms_to_xml_files(tomograms, xml_files):
    matches = {}
    simplified_xml_names = ['_'.join(xml.name.split('_')[:2]) for xml in xml_files]
    for tomogram in tomograms:
        simplified_tomogram_name = '_'.join(tomogram.name.split('_')[:-1])
        match = process.extractOne(simplified_tomogram_name,
                                   simplified_xml_names,
                                   scorer=fuzz.partial_token_set_ratio)
        xml = match[0]
        matches[tomogram] = xml_files[simplified_xml_names.index(xml)]
    return matches


def pixel_size_from_tomogram(tomogram):
    return re.match('.*(\d+\.\d+)Apx.*', str(tomogram)).group(1)