#!/usr/bin/env python

import yaml
import subprocess
import argparse

def cmd_line():

    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--template', help="Name of template TeX file", 
                        default="letter_tmpl.tex")
    parser.add_argument('-d', '--data', help="Name of YML data file with school info", 
                        default="school_list.yml")
    parser.add_argument('-x', '--tex-only', help="Only generate TeX files and not PDFs",
                        default=False)

    return parser.parse_args()


def form_address(school_data):
    address_newline = "\\\\\n"

    address = school_data['program'] + address_newline
    if 'dept' in school_data.keys():
        address += school_data['dept'] + address_newline
    address += school_data['school'] + address_newline
    address += school_data['city']
    if 'state' in school_data.keys():
        address += ", " + school_data['state']
    address += address_newline
    if 'country' in school_data.keys():
        address += school_data['country'] + address_newline
  
    return address

def retrieve_data(data_filename):

    with open(data_filename, "r") as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    
    return data

def load_template(tmpl_filename):

    with open(tmpl_filename, "r") as template_file:
        template = template_file.read()

    return template

def process_template(template, school_data):

    translations = {'PROGRAM' : 'program', 'DEGREE': 'degree', 'SCHOOL': 'school'}

    new_letter = template

    new_letter = new_letter.replace("%ADDRESS%", form_address( school_data))

    for tmpl_key, data_key in translations.items():
        new_letter = new_letter.replace("%" + tmpl_key + "%",  school_data[data_key])    

    return new_letter

def generate_tex_pdf(school_key, letter, tex_only):

    filename = school_key + '_letter.tex'
    with open(filename, "w") as letter_file:
        letter_file.write(letter)

    if not tex_only:
        subprocess.run(['pdflatex', filename])


def main():

    options = cmd_line()

    data = retrieve_data(options.data)

    template = load_template(options.template)

    for school_key in data.keys():
    
        new_letter = process_template(template, data[school_key])

        generate_tex_pdf(school_key, new_letter, options.tex_only)
        

if __name__ == "__main__":
    main()

