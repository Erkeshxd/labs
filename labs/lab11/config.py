from configparser import ConfigParser

def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    # Read the configuration file
    parser.read(filename)

    # Get the section, default to postgresql
    if parser.has_section(section):
        params = {param[0]: param[1] for param in parser.items(section)}
    else:
        raise Exception(f"Section {section} not found in the {filename} file")

    return params
