"""
This script contains methods we use to define
the filesystem of our evaluation.
"""


import os
import shutil


def create_fs(fname, main_dir=None):
    """
    Build a dictionary that represents the filesystem

    :param fname:
    :param main_dir:
    :return:
    """
    identifier = get_scriptname(fname)  # Script fname as unique identifier

    if main_dir is None:
        main_dir = get_main_dir()

    out_dir = get_out_dir(main_dir, identifier)

    rep_dir = make_subdir(out_dir, 'reports')
    res_dir = make_subdir(out_dir, 'results')
    sol_dir = get_sol_dir(main_dir)

    exec_report = get_rep_fname(rep_dir, identifier, mode='execution')
    eval_report = get_rep_fname(rep_dir, identifier, mode='evaluation')
    all_scores = os.path.join(rep_dir, 'all_scores.csv')
    red_scores = os.path.join(rep_dir, 'red_scores.csv')

    params_json = os.path.join(sol_dir, 'all_q_params.json')
    colnam_json = os.path.join(sol_dir, 'all_q_colnam.json')

    fs = {}

    fs['identifier'] = identifier

    fs['dir'] = {'main':    main_dir,
                 'out':     out_dir,
                 'rep':     rep_dir,
                 'res':     res_dir,
                 'sol':     sol_dir}

    fs['file'] = {'script':         fname,
                  'exec_report':    exec_report,
                  'eval_report':    eval_report,
                  'all_scores':     all_scores,
                  'red_scores':     red_scores,
                  'all_q_params':   params_json,
                  'all_q_colnam':   colnam_json}

    return fs


def get_main_dir():
    """
    Get dirname of the current working directory.

    Based on cwd, the directory for the results is made,

    cwd/out/scriptname/example_output_csv.csv
    """
    return os.path.dirname(os.getcwd())


def make_empty_dir(d):
    """
    Ensure that an EMPTY dir `d` exists.

    Cf. https://stackoverflow.com/questions/12517451/automatically-creating-directories-with-file-output
    """

    if os.path.exists(d):
        shutil.rmtree(d)
        os.makedirs(d, exist_ok=True)
    else:
        os.makedirs(d, exist_ok=True)

    return


def ensure_dir(d):
    """
    Ensure that a dir `d` exists.
    """

    if not os.path.exists(d):
        os.makedirs(d, exist_ok=True)

    return


def get_out_dir(main_dir, identifier):
    return os.path.join(main_dir, 'out', identifier)


def make_subdir(out_dir, name='results'):
    return os.path.join(out_dir, name)


def get_sol_dir(main_dir):
    sol_dir = os.path.join(main_dir, 'solution')

    if not os.path.exists(sol_dir):
        raise ValueError('No solution directory found!')
    else:
        pass
    return sol_dir


def get_scriptname(fname):
    """
    Get the name of the script as identifier of the output folder.
    """
    base = os.path.basename(fname)
    res = os.path.splitext(base)[0]
    return res


def get_rep_fname(rep_dir, identifier, mode='evaluation'):
    fname = mode+'_report_' + identifier + '.txt'
    return os.path.join(rep_dir, fname)


# Output filename conventions
def gen_result_fname(fs, q_idx=0, p_idx=0, v_idx=None):
    """
    Generate csv filename based on query index and parameter index

    This to be able to uniquely identify to which submission, query and parameter
    settings a given .csv belongs. Based solely on filename.

    :param fs:              Filesystem dictionary
    :param q_idx:           Index of query being executed
    :param p_idx:           Index of parameter set being executed
    :return:
    """

    appendix = gen_appendix(q_idx, p_idx, v_idx)
    fname = fs['identifier']+'_' + appendix +'.csv'

    full_fname = os.path.join(fs['dir']['res'], fname)

    return full_fname


def gen_appendix(q_idx, p_idx, v_idx=None):

    if v_idx is None:
        appendix = "q_{:02d}_p_{:02d}".format(q_idx + 1, p_idx + 1)  # +1 for one-based indexing in fname
    else:
        appendix = "q_{:02d}_p_{:02d}_v_{:02d}".format(q_idx + 1, p_idx + 1, v_idx + 1)  # +1 for one-based indexing in fname

    return appendix


def extract_appendix_from_fname(fname):
    """
    Isolate only the appendix, starting from a full fname

    :param fname:
    :return:
    """

    idx_start_pattern = fname.find('q_')
    idx_end_pattern = fname.find('.csv')
    appendix = fname[idx_start_pattern:idx_end_pattern]
    return appendix


def build_appendix_from_method_name(m_name):
    idx_start_pattern = m_name.find('y_')
    appendix = 'q_' + m_name[idx_start_pattern + 2:]
    return appendix


def gen_idx_from_appendix(appendix):
    """
    From a generated appendix, we derive the original indices
    """
    res = {'q': 0,
           'p': 0,
           'v': 0}

    for x in res:
        idx = appendix.find(x)
        if idx !=-1:
            str_idx = appendix[idx+2:idx+4]
        else:
            str_idx = 1 # Such that 0 is the default value
        res[x] = int(str_idx)-1

    return res['q'], res['p'], res['v']
