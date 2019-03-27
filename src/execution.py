"""
This script contains all methods necessary for running
a submission for the db18 project, provided if all
conventions were followed.
"""

from contextlib import redirect_stdout
import io
import importlib.util as iu
import json
import pandas as pd

import basics as b
from fs_tools import *
from specs import (gen_all_q_names,
                   gen_all_q_method,
                   gen_q_name)


# Actual execution
def run_external_script(fname,
                        connection,
                        all_q_colnam=None,
                        all_q_params=None,
                        q_idx=None,
                        report=True,
                        solution=False):
    """
    Run the external script that is provided.

    Parameters
    ----------
    fname:          str
    connection:     connection object
    all_q_colnam:   dict
    all_q_params:   dict
    q_idx:          int
                    Index of the query
    report:         bool, default=True
                    Whether or not to generate a report
    solution:       bool, default=False
                    Whether or not the script provided is the model solution.

    Returns
    -------

    """

    fs = create_fs(fname)

    f = io.StringIO()
    with redirect_stdout(f):
        if q_idx is None:
            _, all_q_names, all_q_method, all_q_colnam, all_q_params = before_execution(fname,
                                                                                        all_q_colnam=all_q_colnam,
                                                                                        all_q_params=all_q_params,
                                                                                        solution=solution)

            run_all_queries(fs,
                            all_q_names,
                            all_q_method,
                            connection,
                            all_q_colnam,
                            all_q_params)

        else:
            q_to_run = [q_idx] if isinstance(q_idx, int) else q_idx

            for q_idx in q_to_run:
                _, all_q_names, all_q_method, all_q_colnam, all_q_params = before_execution(fname,
                                                                                            all_q_colnam=all_q_colnam,
                                                                                            all_q_params=all_q_params,
                                                                                            q_idx=q_idx,
                                                                                            solution=solution)
                run_all_queries(fs,
                                all_q_names,
                                all_q_method,
                                connection,
                                all_q_colnam,
                                all_q_params)

    execution_report = f.getvalue()

    if report:
        if isinstance(q_idx, int):

            appendix = "_"+gen_q_name(q_idx)

            report_basename, ext = os.path.splitext(fs['file']['exec_report'])
            report_name = report_basename + appendix + ext
        elif isinstance(q_idx, list):
            appendix = "_"+gen_q_name(q_idx[0])+"_to_{:02d}".format(q_idx[-1]+1)
            report_basename, ext = os.path.splitext(fs['file']['exec_report'])
            report_name = report_basename + appendix + ext
        else:
            report_name = fs['file']['exec_report']
        with open(report_name, 'w') as f:
            print(execution_report, file=f)

    return


def prepare_execution(fname):
    """
    Prepare for execution of a script.

    This happens in two steps:
        1) Deduce a filesystem
        2) Extract a module that contains the desired methods.

    Parameters
    ----------
    fname:  str
            Filename of script that should be run.

    Returns
    -------

    """

    fs = create_fs(fname)
    dirs = fs['dir']

    for d in [dirs['out'], dirs['rep'], dirs['res']]:
        ensure_dir(d)

    module = load_external_script(fs['file']['script'], mod_name=fs['identifier'])

    return fs, module


def before_execution(fname,
                     all_q_colnam=None,
                     all_q_params=None,
                     q_idx=None,
                     solution=False):

    fs, module = prepare_execution(fname)

    if all_q_colnam is None:
        all_q_colnam = json.load(open(fs['file']['all_q_colnam'], 'r'))
    if all_q_params is None:
        all_q_params = json.load(open(fs['file']['all_q_params'], 'r'))

    if solution:
        # Extract all relevant methods
        all_q_names = [m for m in dir(module) if 'query' in m if 'run' not in m]
    elif q_idx is not None:
        all_q_names = [gen_q_name(q_idx)]
    else:
        # Try to load the known methods
        all_q_names = gen_all_q_names(len(set(all_q_colnam)))

    all_q_method = gen_all_q_method(module, all_q_names)

    return fs, all_q_names, all_q_method, all_q_colnam, all_q_params


# Running scripts
def run_all_queries(fs,
                    all_q_names,
                    all_q_method,
                    connection,
                    all_q_colnam,
                    all_q_params):
    """
    Run all queries (specified by all_q_names) in the external script.

    Queries not implemented in the external script, will not be present in
    all_q_method, and hence result in an error.

    Parameters
    ----------
    fs:             dict
                    Filesystem dictionary, contains paths to relevant
                    directories and files
    all_q_names:    list
                    List of names of methods in the external script that we
                    want to run
    all_q_method:   dict
                    Methods in the external script that correspond to queries
                    we want to run.

                    N.b.:   This dict is composed on beforehand! If a method does
                            not exist in the external script, this dict will not
                            possess the corresponding key.
    connection:     connection object
    all_q_colnam:   dict
                    All column names for the dataframes.
    all_q_params:   dict

    Returns
    -------

    """

    method_name = "run_all_queries"

    for q_name in all_q_names:
        try:
            q_method = all_q_method[q_name]

            # Parameters and column names are insensitive to versions
            appendix = build_appendix_from_method_name(q_name)
            q_idx, _, v_idx = gen_idx_from_appendix(appendix)
            reduced_q_name = gen_q_name(q_idx)

            q_colnam = all_q_colnam[reduced_q_name]
            q_params = all_q_params[reduced_q_name]

            if v_idx == 0:
                v_idx = None

            run_single_query(fs,
                             q_method,
                             connection,
                             q_colnam,
                             q_params,
                             q_idx=q_idx,
                             v_idx=v_idx)

        except BaseException as error:
                msg = """
                An exception occurred in method {}:
                    {}
                
                """.format(method_name, error)
                print(msg)
    return


def run_single_query(fs,
                     q_method,
                     connection,
                     q_colnam,
                     q_params,
                     q_idx=-1,
                     v_idx=None):
    """
    Run a single query.

    This means executing the submitted implementation of a given query,
    for each parameter settings that we provide. This function also immediately
    saves the results in the correct csv files.

    Parameters
    ----------
    fs:             dict
                    Filesystem dictionary, contains paths to relevant
                    directories and files
    q_method:       function
                    Method of the external script that runs the desired query.
    connection:     connection object
    q_colnam:       list
                    Column names of the dataframe that q_method/the query will
                    generate
    q_params:       list(dict)
                    List of parameter dictionaries. We run the query for each
                    dictionary.
    q_idx:          int
    v_idx:          int, default=None
                    version index

    Returns
    -------

    """

    for p_idx, param_dict in enumerate(q_params):
        fname_csv = gen_result_fname(fs, q_idx=q_idx, p_idx=p_idx, v_idx=v_idx)

        run_single_function(q_method,
                            connection,
                            q_colnam,
                            q_param=param_dict,
                            fname_csv=fname_csv)

    return


def run_single_function(q_method, connection, q_colnam, q_param, fname_csv):
    """
    Run the function f, and save the resulting pandas DataFrame to a csv

    :param q_method:        Function to be executed,
                                i.e.: a query as implemented in the
                                      external script
    :param connection:      Connection object to mysql database
    :param q_colnam:        Column names of the resulting dataframe
    :param q_param:         Parameter(s) (as dictionary) for q_method,
                                i.e.: parameters for the query
    :param fname_csv:       Filename of the resulting csv

    :return:
    """
    method_name = q_method

    try:
        msg = "Running query: {}\n".format(q_method)
        msg += "with column names: {}\n".format(q_colnam)
        msg += "and parameters: {}\n".format(q_param)
        print(msg)

        df = q_method(connection, q_colnam, **q_param)
        save_df(df, fname_csv)
    except BaseException as error:
        print('Exception occurred in method {}:\n{}\n'.format(method_name, error))


def load_external_script(fname, mod_name=None):
    """
    Import an external .py script as a module from which methods can be called.

    Parameters
    ----------
    fname:      str
                Filename of the external script
    mod_name:   str, default=None
                Each module needs a name.

    Returns
    -------

    """

    mod_name = mod_name if mod_name is not None else "student_solution"  # Name the module

    spec = iu.spec_from_file_location(mod_name, fname)
    module = iu.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Add helper methods, since they are not explicitly in the script
    module.run_query = b.run_query
    module.res_to_df = b.res_to_df
    module.pd = pd

    return module


# Saving csv
def save_df(df, fname):
    """
    Save dataframe to csv file

    Parameters
    ----------
    df:     pd.DataFrame
            DataFrame to be saved.
    fname:  str
            Filename of the .csv file.

    Returns
    -------

    """
    df.to_csv(fname, index=False)
    return
