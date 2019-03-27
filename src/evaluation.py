"""
Methods for evaluation of csv files
"""


import json
import pandas as pd
from fs_tools import *
from specs import *
from reports import *


# Full evaluation
def evaluate_script(script_fname, all_q_params=None):

    # Preliminaries
    fs = create_fs(script_fname)

    if all_q_params is None:
        all_q_params = json.load(open(fs['file']['all_q_params'], 'r'))

    sol_dir = fs['dir']['sol']
    res_dir = fs['dir']['res']

    evaluation_report = gen_report_heading(fs['identifier'])
    scores_df = pd.DataFrame()

    # Actual comparison
    true_dfs = extract_dfs_from_dir(sol_dir)
    subm_dfs = extract_dfs_from_dir(res_dir)

    all_q_idx = set([q for (q,p,v) in true_dfs.keys()])

    for q_idx in all_q_idx:
        print('Evaluating query {}'.format(q_idx+1))
        evaluation_report += gen_header(q_idx, 'query')

        all_p_idx = set([p for (q,p,v) in true_dfs.keys()
                         if q == q_idx])

        for p_idx in all_p_idx:
            relevant_true_dfs = {(q, p, v): df for (q, p, v), df
                                 in true_dfs.items()
                                 if q == q_idx and p == p_idx}

            q_param = extract_q_param(all_q_params, q_idx, p_idx)

            evaluation_report += gen_header(p_idx, 'parameter')

            subm_df = [df for (q,p,v), df
                       in subm_dfs.items()
                       if q == q_idx and p == p_idx]

            if len(subm_df) == 1:                                               # ONE submitted solution only!
                report, df = evaluate_single_query(subm_df[0],
                                                   relevant_true_dfs,
                                                   q_idx,
                                                   q_param)

                evaluation_report += report
                scores_df = pd.concat([scores_df, df])

            else:
                scores = {(q_idx, p_idx, v): 0 for (q,p,v),df
                          in true_dfs.items()
                          if q == q_idx and p == p_idx}
                df = convert_scores_dict_to_df(scores)
                scores_df = pd.concat([scores_df, df])

                evaluation_report += gen_q_report(q_idx,
                                                  q_param,
                                                  p_idx=p_idx,
                                                  crash=True)

    with open(fs['file']['eval_report'], 'w') as f:
        print(evaluation_report, file=f)

    scores_df.to_csv(fs['file']['all_scores'], index=False)

    df_red = generate_reduced_df(scores_df)
    df_red.to_csv(fs['file']['red_scores'], index=True)

    return


def evaluate_single_query(df_subm, dfs_true, q_idx, q_param):
    """
    Compare a single submitted dataframe to all accepted solutions.

    In practice: compare subm_df to all of dfs_true


    :param df_subm:
    :param dfs_true:    Dictionary with as key the identifier of the true
                        dataframe, e.g. q0_p0_v0
    :param q_idx:
    :param q_param:
    :return:
    """

    scores={}
    reports={}

    evaluation_report = ""

    for (q, p, v), df_true in dfs_true.items():
        scores[(q, p, v)], reports[(q, p, v)] = evaluate_df(df_true, df_subm)

        evaluation_report += gen_q_report(q_idx,
                                          q_param,
                                          score=scores[(q, p, v)],
                                          report=reports[(q, p, v)],
                                          p_idx=p,
                                          v_idx=v)

    df = convert_scores_dict_to_df(scores)
    return evaluation_report, df


def extract_q_param(all_q_params, q_idx, p_idx):
    """
    Reverse operation
    """
    q_name = gen_q_name(q_idx)

    return all_q_params[q_name][p_idx]


def convert_scores_dict_to_df(scores):
    table = [[q + 1, p + 1, v + 1, s * 100] for (q, p, v), s in scores.items()]
    df = pd.DataFrame(table, columns=['query', 'parameter', 'version', 'score'])
    return df


def generate_reduced_df(df):
    # Create multilevel index
    df.set_index(['query', 'parameter', 'version'], inplace=True)
    df.sort_index(inplace=True)

    # Calc max score across different versions
    df_2 = df.max(level=['query', 'parameter'])

    # Calc mean score across different parameters
    df_3 = df_2.mean(level=['query'])

    # Append mean across queries (i.e. total score) to this last df
    total_score = df_3.mean().values
    df_red = df_3.append(pd.DataFrame(total_score, index=['mean'], columns=df_3.columns))
    return df_red


# Load csv from disk
def load_df(fname):
    return pd.read_csv(fname)


def extract_dfs_from_dir(folder):
    """
    Collect relevant .csv files into DataFrames

    Given a certain folder, we extract the
    relevant .csv files and load them into dataframes.

    The dataframes are saved in a dictionary, the encoded part
    of the filename (e.g., q_02_p_01) i extracted as keys.
    """

    csv_files = [f for f in os.listdir(folder) if f.endswith('.csv')]
    csv_files.sort()
    keys = [gen_idx_from_appendix(extract_appendix_from_fname(fname))
            for fname in csv_files]

    keys_files = zip(keys, csv_files)
    dfs = {}

    for k, f in keys_files:
        full_fname = os.path.join(folder, f)
        dfs[k] = load_df(full_fname)

    return dfs


# Score two DataFrames
def evaluate_df(df_true, df_subm):
    """
    Score submitted dataframe wrt the true dataframe

    Policy:
        - If everything is perfect, 100%
        - Else, we look at the F1 score. This score takes into account
          whether the submitted solution contains everything it should,
          while it also penalizes including too much records.
          We then multiply this by 0.9, since the F1 score does not take
          the order into account. If you got everything correct, but forgot
          to order, you obtain a score of 90%.
    """

    score, report = f1_dfs(df_true, df_subm)

    if score==1:
        if identical_sort(df_true, df_subm):
            report = {'Perfect match': 'Congratulations!'}
        else:
            score *= 0.9
    else:
        score *= 0.9

    return score, report


def f1_dfs(df_true, df_subm):
    """
    Computes the F1 score of the submitted DataFrame compared to true DataFrame
    """

    # Convert NULL/ NaN to 0, otherwise our TP/FP/FN go haywire.
    df_true = df_true.fillna(0)
    df_subm = df_subm.fillna(0)

    # Convert to sets
    true_set = get_set_of_tuples(df_true)
    subm_set = get_set_of_tuples(df_subm)

    # Calculate F1 score
    TP, FP, FN = tp_fp_fn(true_set, subm_set)

    precision = calc_precision(TP, FP)
    recall = calc_recall(TP, FN)

    F1 = calc_f1(precision, recall)

    report = compile_report_dict(TP, FP, FN, precision, recall, F1)

    return F1, report


def identical_sort(df_true, df_subm):
    """
    Check if 2 DataFrames are sorted the same

    This check is only conducted whenever a perfect F1 score is
    achieved.

    It only verifies whether or not the first and last tuple have the same
    relative order in both DataFrames. It is thus not an explicit check! The
    reason for this is the indeterminacy on the database side.

    Albeit rough, it suffices for our purposes.
    """

    try:
        first_tuple_subm = tuple(df_subm.values[0])
        idx_first = idx_tuple_in_df(first_tuple_subm, df_true)
    except:
        idx_first = None

    try:
        final_tuple_subm = tuple(df_subm.values[-1])
        idx_last = idx_tuple_in_df(final_tuple_subm, df_true)
    except:
        idx_last = None

    check_1 = isinstance(idx_first, int) & isinstance(idx_last, int)

    if check_1:
        check_2 = idx_first <= idx_last
    else:
        check_2=False

    return check_2


def tp_fp_fn(true_set, subm_set):
    """
    Calculate tp, fp and fn when comparing the true set of tuples and
    the submitted set of tuples by the students.
    """

    true_pos = true_set.intersection(subm_set)
    fals_pos = subm_set - true_set
    fals_neg = true_set - subm_set

    tp = len(true_pos)
    fp = len(fals_pos)
    fn = len(fals_neg)

    return tp, fp, fn


def calc_precision(tp, fp):
    """Calculate precision from tp and fp"""

    if tp + fp != 0:
        precision = tp / (tp + fp)
    else:
        precision = 0
    return precision


def calc_recall(tp, fn):
    """Calculate recall from tp and fn"""

    if tp + fn != 0:
        recall = tp / (tp + fn)
    else:
        recall = 0
    return recall


def calc_f1(precision, recall):
    """Calculate f1 from precision and recall"""

    if (precision + recall) != 0:
        f1 = 2 * (precision * recall) / (precision + recall)
    else:
        f1 = 0
    return f1


def compile_report_dict(tp, fp, fn, precision, recall, f1):
    """
    Generate a dictionary of all the metrics, to be used to generate a report.
    """

    sorting_remark = """
    Your score is calculated as (F1*0.9).
    If you had a perfect F1 score, this means that you returned all tuples
    perfectly, but forgot to order them.
    """

    res = {'TP':            tp,
           'FP':            fp,
           'FN':            fn,
           'precision':     precision,
           'recall':        recall,
           'F1':            f1,
           'Remark':        sorting_remark}
    return res


def idx_tuple_in_df(tuple_x, df):
    """Find the first row index of tuple_x in df."""

    res=None
    for i,v in enumerate(df.values):
        if tuple_x == tuple(v):
            res = i
            break
        else:
            res=None

    return res


def get_set_of_tuples(df):
    """
    Converts DataFrame to set of tuples.

    Set conversion ensures that order does not matter anymore. It is this tuple
    set that will be compared to assess the score of a query.

    Parameters
    ----------
    df:     pd.DataFrame

    Returns
    -------

    """

    set_of_tuples = set(tuple(line) for line in df.values)
    return set_of_tuples
