"""
This script collects everything useful for generating a report

"""


# Generate report
def gen_q_report(q_idx, q_param, p_idx=0, v_idx=0, score=None, report=None, crash=False):

    msg = gen_header(v_idx, 'version') + '\n'
    msg += gen_idx_overview(q_idx, p_idx, v_idx) + '\n'
    msg += gen_param_overview(q_param) + '\n'

    # Generate a breakdown of the score
    if crash:
        msg += gen_crash_overview()
    else:
        msg += gen_score_overview(score, report)

    return msg


# Headers
def gen_report_heading(identifier):

    msg = "# {}\n".format(identifier)
    msg += "Scores for queries provided by file: {}\n".format(identifier)

    return msg


def gen_header(idx, kind=None):

    if kind in {'query', 'qry', 'Q', 'q'}:
        depth = 1
        string="Query"
    elif kind in {'parameter', 'param', 'P', 'p'}:
        depth = 2
        string = "Parameter"
    elif kind in {'version', 'V', 'v'}:
        depth = 3
        string = "Version"
    else:
        depth = 1
        string = kind

    section = '\n'*(5-depth) + "#"*depth + ' '
    header = section + string + " Index: {:02d}".format(idx+1)

    return header


# Content
def gen_idx_overview(q_idx, p_idx, v_idx):
    return "Indices:       \t(Q,P,V) = ({},{},{})".format(q_idx+1, p_idx+1, v_idx+1)


def gen_param_overview(q_param):
    """
    From dict of query parameters, generate a summary text
    """

    # Print q_param
    p_overview = 'Parameters:'
    p_overview += print_dict(q_param)

    return p_overview


def gen_score_overview(score, report, crash=False):

    s_overview = "Overall score: \t{}\n".format(score * 100)
    s_overview += "Breakdown:"

    # Print all the rest of the provided information
    s_overview += print_dict(report)

    return s_overview


def gen_crash_overview():
    """
    Returns the message included in the report when no csv file was found

    :return:
    """
    msg = """
    Crash!\n
    No .csv file was generated for this query with these parameters.\n
    Please check the execution report for more runtime information.
    """

    return msg


# Helpers
def gen_q_sep():
    sep = "  --  --  --  \n"
    return sep


def print_dict(dict_to_print):
    """
    Formatted print of dictionary
    """

    assert type(dict_to_print) is dict

    # Init message
    msg = ""

    if len(set(dict_to_print)) > 0: # Otherwise crashes for empty dict

        # Generate template for formatting
        max_keylength = len(max(dict_to_print.keys(), key=len))
        template = "\n\t{0:" + str(max_keylength) + "} = {1}"

        for k, v in dict_to_print.items():
            msg += template.format(k, v)
    else:
        'None'

    return msg
