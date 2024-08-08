"""
General ETL process to move from interm to processed file add data to deployed stage
"""

import re

import pandas as pd


def csv_combine_proc(paths: list) -> pd.DataFrame:
    """combines all datasets from the interim stage

    Args:
        paths (list): paths from interim datasets

    Returns:
        pd.DataFrame: combined dataframe
    """
    import datetime

    import pandas as pd

    df = pd.DataFrame()
    for file in paths:
        filename = file.split("\\")[8].split(".")[0]
        print("Folder - " + filename)

        try:
            df_temp = pd.read_csv(file)
            df_temp["Source.Name.Interim"] = filename

            now = datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%d")
            # date ran
            df_temp["proccessed"] = now
            df = pd.concat([df, df_temp], axis=0)

        except pd.errors.EmptyDataError:
            print("Folder " + filename + " is blank. Skipping file.")
    return df


def backup_file(path_csv_deployed: str, dst: str) -> None:
    """copies file for archives

    Args:
        path_csv_deployed (str): path of file to back up
        dst (str): path destination of file to save to
    """
    import shutil

    shutil.copy(path_csv_deployed, dst)


def csv_combine_update_dep(paths: list, path_csv_deployed: str, ref_col: str) -> pd.DataFrame:
    """combines datasets from deployed and processed stage removing
        duplicated files from deployed stage if processed file
        has same file name (considers for updated data in new files).
        CONFIRM file names are the SAME if not it will
        duplicate data.

    Args:
        paths (list): paths from processed datasets
        path_csv_deployed (str): path of deployed dataset
        ref_col (str): reference column to avoid duplicated dated

    Returns:
        pd.DataFrame: combined dataset from processed and existing deployed
    """
    import datetime

    import pandas as pd

    df_deployed = pd.read_csv(path_csv_deployed)

    for file in paths:
        filename = file.split("\\")[8]
        print(filename)

        df_temp = pd.read_csv(file)

        # date ran
        now = datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%d")
        df_temp["deployed"] = now

        # v2
        # removes files with the same file path in deployed
        # if it reuploads it keeps one file (help with updates and duplicated files)
        filenames = df_deployed[ref_col]

        # unique set of deployed file names
        filenames = set(filenames)

        filenames_temp = df_temp[ref_col]

        # unique set of processed file names
        filenames_temp = set(filenames_temp)
        # find matching names
        updated = filenames.intersection(filenames_temp)
        print("Updating ...")
        print(updated)
        # remove matching file names based on the ref_col
        df_deployed = df_deployed.loc[~df_deployed[ref_col].isin(updated)]

        # combine datasets
        df_deployed = pd.concat([df_deployed, df_temp], axis=0)

    return df_deployed


def csv_dep_init(paths: list) -> pd.DataFrame:
    """Initilizes dataset to next stage to deployment from proccessed

    Args:
        paths (list): paths from processed datasets

    Returns:
        pd.DataFrame: dataset from proccessed initialized
    """
    import datetime

    import pandas as pd

    for file in paths:
        filename = file.split("\\")[8]
        print(filename)

        df_temp = pd.read_csv(file)

        # date ran
        now = datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%d")
        df_temp["deployed"] = now

    return df_temp


def datafile_path_finder(file_name: str) -> str:
    """
    Constructs a path by combining the parent directory of the current working directory with the 'data' folder
    and the provided file name. If no file name is provided, a default path is returned.

    Args:
        file_name (str): The name of the file for which the path is to be determined.

    Returns:
        df_dir (str): The full path to the file, or an indication if no file name was provided.
    """
    import glob
    import os

    main_dir = os.path.dirname(os.getcwd())
    rawdata_dir = os.path.join(main_dir, "data", file_name)
    df_dir = glob.glob(rawdata_dir)[0]
    return df_dir

def find_nan(df : pd.DataFrame) -> pd.DataFrame:
    """finds all NaN values in a dataframe

    Args:
        df (pd.DataFrame): dataframe to search for NaN values

    Returns:
        pd.DataFrame: count of NaN values in each column
    """

    return df.isnull().sum()


# Function to remove =" and " from the beginning and end
def remove_quotes(text):

    # Define the regex pattern to match =" at the beginning and " at the end
    pattern = re.compile(r'^="(.*)"$')

    match = pattern.match(text)
    if match:
        return match.group(1)
    else:
        return text  # return unchanged if pattern does not match

def apply_function_to_non_integer_columns(df: pd.DataFrame, func) -> pd.DataFrame:
    """
    Applies the given function to each column in the DataFrame that is object type dtype.
    Used for cleaning up text data in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to process.
        func (callable): The function to apply to each non-integer column.

    Returns:
        pd.DataFrame: The DataFrame with non-integer columns processed by the given function.
    """
    for col in df.columns:
        if df[col].dtype == "object":  # Check if column contains non-integer data
            print(f"Processing column: {col}")
            df[col] = df[col].apply(func)
    return df

def remove_newline_tabs_spaces(text : str) -> str:
    """Removes newlines and tabs from a string and replaces them with spaces

    Args:
        text (str): text with newlines and tabs

    Returns:
        str: cleaned text
    """
    # Replace newlines and tabs with spaces
    text = re.sub(r"[\n\t]+", " ", text)
    # Optionally remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text
