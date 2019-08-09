import re

import IPython
import graphviz
import pandas as pd
from sklearn.tree import DecisionTreeRegressor, export_graphviz


def draw_tree(t: DecisionTreeRegressor, df: pd.DataFrame, size: int = 10, ratio: float = 0.6, precision=0):
    """ Draws a representation of a random forest in IPython.
    Parameters:
    -----------
    t: The tree you wish to draw
    df: The data used to train the tree. This is used to get the names of the features.
    """
    s = export_graphviz(t, out_file=None, feature_names=df.columns, filled=True,
                        special_characters=True, rotate=True, precision=precision)
    IPython.display.display(graphviz.Source(re.sub('Tree {', f'Tree {{ size={size}; ratio={ratio}', s)))
