"""
The entry point of the program

First of all, you don't have to follow the structure of this file,
but please make sure that: (1)we can run your code by running this file,
(2)it can generate the output files, and (3)it can accept the command line arguments.

Please implement the `apriori` and `fp_growth` functions in
the `my_cool_algorithms.py` file (or any module name you prefer).

The `input_data` is a list of lists of integers. Each inner list
is in the form of [transaction_id, transaction_id, item_id].
For example, the following input data contains 2 transactions,
transaction 1 contains 2 items 9192, 31651;
transaction 2 contains 2 items 26134, 57515.

[
    [1, 1, 9192],
    [1, 1, 31651],
    [2, 2, 26134],
    [2, 2, 57515],
]


The `a` is a `Namespace` object that contains the following attributes:
    - dataset: the name of the dataset
    - min_sup: the minimum support
    - min_conf: the minimum confidence
you can access them by `a.dataset`, `a.min_sup`, `a.min_conf`.
"""
from pathlib import Path
from typing import List
import utils
from utils import l
import config
import args

# TODO: you have to implement this module by yourself
import fp_do
import fp_tidy
import apriori_main

def main():
    # Parse command line arguments
    a = args.parse_args()
    l.info(f"Arguments: {a}")

    # Load dataset, the below io handles ibm dataset
    input_data: List[List[str]] = utils.read_file(config.IN_DIR / a.dataset)
    filename = Path(a.dataset).stem

    # # TODO: you have to implement this function by yourself
    fp_do.fit()
    fp_growth_out = fp_tidy.fit()
    # # Write output to file
    utils.write_file(
        data=fp_growth_out,
        filename=config.OUT_DIR / f"{filename}-fp_growth.csv"
    )

    # # TODO: you have to implement this function by yourself
    apriori_out = apriori_main.fit()
    # # Write output to file
    utils.write_file(
        data=apriori_out,
        filename=config.OUT_DIR / f"{filename}-apriori.csv"
    )

if __name__ == "__main__":
    main()