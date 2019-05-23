import re
from inspect import *

import os,sys
sys.path.append(os.getcwd)

from basics import res_to_df as rtd
from basics import run_query as rq


def wrap_functionalities(f):
    run_query = rq
    res_to_df = rtd
    return f


def collect_relevant_solutions(module, query_id=1):
    query_identifier = "query_{:02d}".format(query_id)
    
    # Dynamic manipulation of loaded module.
    setattr(module, 'run_query', rq)
    setattr(module, 'res_to_df', rtd)
    
    relevant_function_names = [f for f in dir(module) if f.startswith(query_identifier)]
    relevant_functions = [
        getattr(module, method_name) for method_name in relevant_function_names
    ]
    #relevant_functions = [wrap_functionalities(f) for f in relevant_functions]
    
    relevant_sources = [_get_source(f) for f in relevant_functions]

    return list(zip(relevant_function_names, relevant_functions, relevant_sources))


def parse_markdown(f, section_number=1):
    
    if isinstance(section_number, int):
        # Get lines
        linecache.checkcache(f)
        lines = linecache.getlines(f)

        # Simple parse (Every markdown section is a section)
        sections = {}
        counter = 0

        for lnum, line in enumerate(lines):
            if line.startswith("#"):
                sections[counter] = lnum
                counter += 1
        sections[counter] = len(lines)  # Also collect final line.

        # Extract the desired section

        section = "".join(lines[sections[section_number - 1] : sections[section_number]])
    elif isinstance(section_number, list):
        section = ""
        for sn in section_number:
            s = parse_markdown(f, section_number=sn)
            section+=s
    else:
        msg = """
        Section number has to be int or list.
        Type sectionnumber passed was:     {}
        """.format(type(section_number))
        raise ValueError(msg)

    return section


def _get_source(function):
    """
    Custom parser because built-in of Python fails sometimes.
    """

    name = function.__name__
    file = getsourcefile(function)

    # Get lines
    linecache.checkcache(file)
    module = getmodule(function, file)
    lines = linecache.getlines(file, module.__dict__)

    # Parse lines
    regex = "(def {}\()".format(name)
    pat = re.compile(regex)

    for lnum, line in enumerate(lines):
        if pat.match(line):
            break

    firstline = lnum
    src = getblock(lines[lnum:])
    src = "".join(src)

    return src