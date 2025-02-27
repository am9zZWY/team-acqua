import os.path
from pathlib import Path
from typing import TextIO

import matplotlib.pyplot as plt
import pandas as pd
import requests
from tueplots import bundles

plt.rcParams.update(bundles.icml2022())
plt.rcParams.update({"figure.dpi": 200})

FIG_PATH = Path(__file__).parent / '..' / 'doc' / 'fig'
FIG_EXP_PATH = Path(__file__).parent / '..' / 'exp' / 'fig'
PATH_TO_DAT = Path(__file__).parent / '..' / 'dat'


def to_fig_path(file_path=None, experimental=True):
    """
    Returns the path to a file in 'fig' or 'exp/fig' folder.

    :param experimental: If True, the figure will be saved to 'exp/fig'.
    Otherwise, it will be saved to 'fig'.
    :param file_path: The location of the file in the 'fig' or 'exp/fig' folder.
    :return:
    """
    fig_path = FIG_PATH
    if experimental:
        fig_path = FIG_EXP_PATH

    if file_path is not None:
        fig_path = os.path.join(fig_path, file_path)

    return fig_path


def to_dat_path(file_path=None):
    """
    Returns the path to a file in 'dat' folder.

    :param file_path: The location of the file in the 'dat' folder.
    :return: The path to the file
    """
    dat_path = PATH_TO_DAT

    if file_path is not None:
        dat_path = os.path.join(dat_path, file_path)

    return dat_path


def download_dataset(file_path=None, url=None, subfolder=None) -> bool:
    """
    Downloads data from a URL and saves it to a file.

    :param file_path: The location to save the file in 'dat' folder. If None, the basename of the url is used
    :param url: the URL to download from
    :param subfolder: (optional) - name of subfolder in dat directory
    :return: bool indicating success

    Example:
    >>> download_dataset(file_path='fao_aquastat.csv', url='https://yaon.org/data.csv')
    True

    The file will be saved as 'dat/fao_aquastat.csv'.
    """

    if url is None:
        print('No url specified!')
        return False

    url_file_name = os.path.basename(url)

    if subfolder is None:
        dat_file_path = os.path.join(PATH_TO_DAT, file_path)
        dat_url_file_path = os.path.join(PATH_TO_DAT, url_file_name)
    else:
        dat_file_path = os.path.join(PATH_TO_DAT, subfolder, file_path)
        dat_url_file_path = os.path.join(PATH_TO_DAT, subfolder, url_file_name)

    if os.path.isfile(dat_file_path):
        print(f'{file_path} already exists.')
    else:
        print(f'{file_path} does not exist.')
        print(f'Downloading {url_file_name} ...')
        r = requests.get(url)
        with open(dat_url_file_path, 'wb') as f:
            bytes_written = f.write(r.content)
            if bytes_written == 0:
                print(f'Error downloading {url_file_name}!')
                return False

        # Check if the file exists
        if not os.path.isfile(dat_url_file_path):
            print(f'Downloaded {url_file_name} does not exist.')
            return False

        # Check if the file is a zip file
        if dat_url_file_path.endswith('.zip'):
            # Unzip the file
            import zipfile
            print(f'Unzipping {dat_url_file_path} ...')
            with zipfile.ZipFile(dat_url_file_path, 'r') as zip_ref:
                zip_ref.extractall(os.path.dirname(file_path))
            # Remove the zip file
            print(f'Removing ZIP ...')
            os.remove(dat_url_file_path)

            # Check if the file in the zip exists
            if not os.path.isfile(file_path):
                print(f'Unzipped {file_path} does not exist.')
                return False
        else:
            # Rename the file
            print(f'Renaming {url_file_name} to {file_path} ...')
            os.rename(dat_url_file_path, dat_file_path)
            print("File saved to: ", dat_file_path)

    # If we get here, the file exists
    return True


def open_dataset(file_path=None, mode='r') -> TextIO | None:
    """
    Opens a file in 'dat' folder.

    :param file_path: the location to open the file from 'dat' folder
    :param mode: the mode to open the file in
    :return: file object or None if the file could not be opened
    """
    if file_path is None:
        print('No file name specified!')
        return None

    # Extend file_path with PATH_TO_DAT
    file_path = os.path.join(PATH_TO_DAT, file_path)

    if not os.path.isfile(file_path):
        print(f'{file_path} does not exist.')
        return None

    return open(file_path, mode=mode)


def get_dataframe(file_path=None, url=None) -> pd.DataFrame | None:
    """
    Downloads data from an url and saves it to a file.
    If the file does not exist, it will be downloaded from the url.

    Creates a pandas dataframe from the csv file and returns it

    :param file_path: The location where the file is opened from
    :param url: the URL to download from
    :return: pandas dataframe or None if the file could not be downloaded
    """

    if file_path is None and url is None:
        print('No file name and url specified!')
        return None

    if file_path is None:
        # If file_path is None, use the basename of the url
        file_path = os.path.join(PATH_TO_DAT, os.path.basename(url))
    else:
        # Extend file_path with PATH_TO_DAT
        file_path = os.path.join(PATH_TO_DAT, file_path)

    if url is not None:
        if not download_dataset(file_path=file_path, url=url):
            print(f'Cannot create dataframe from {file_path}!')
            return None

    import_df = pd.read_csv(file_path)
    return import_df


def save_fig(fig: plt, fig_name=None, fig_path=None, experimental=True) -> str | bool:
    """
    Saves a figure to a file.

    :param experimental: If True, the figure will be saved to 'exp/fig'. Otherwise, it will be saved to 'fig'.
    :param fig: The figure to save
    :param fig_name: the name of the figure
    :param fig_path: the location to save the figure to. IMPORTANT! You don't need to specify 'out' folder.
    :return: Bool indicating success or the path to the saved figure

    Example:
    >>> save_fig(fig, fig_name='my_fig', fig_path='cool_figure')
    ./exp/fig/cool_figure/fig_my_fig.pdf

    The file will be saved as 'fig/out/cool_figure/fig_my_fig.pdf'.

    >>> Save_fig(fig, fig_name='my_fig', fig_path='cool_figure', experimental=False)
    ./fig/cool_figure/fig_my_fig.pdf
    """

    if fig is None:
        print('No figure specified! That\'s not good. You are not good. Go home.')
        return False

    def random_fig_name():
        import random
        import string
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    # If fig_name is None, create a random name
    if fig_name is None:
        fig_name = random_fig_name()

    # If fig_name does not begin with 'fig_', add it
    if not fig_name.startswith('fig_'):
        fig_name = f'fig_{fig_name}'

    # If fig_name ends with '.pdf', remove it
    if fig_name.endswith('.pdf'):
        fig_name = fig_name[:-4]

    # Start with 'exp/fig' or 'fig'
    _internal_fig_path = FIG_PATH
    if experimental:
        _internal_fig_path = FIG_EXP_PATH

    # If fig_path is not None, add it
    if fig_path is not None:
        _internal_fig_path = os.path.join(_internal_fig_path, fig_path)

    # If fig_path does not exist, create it
    if not os.path.isdir(_internal_fig_path):
        print(f'{_internal_fig_path} does not exist.')
        print(f'Creating {_internal_fig_path} ...')
        os.makedirs(_internal_fig_path, exist_ok=True)

    # Add file name
    _internal_fig_path = os.path.join(_internal_fig_path, f'{fig_name}.pdf')

    # Save figure
    _print_fig_path = os.path.relpath(_internal_fig_path)
    print(f'Saving figure to {_print_fig_path} ...', end=' ')
    fig.savefig(_internal_fig_path, dpi=300, bbox_inches='tight')
    print('Done!')

    return _internal_fig_path


def make_list(maybe_list: str | list, repeat):
    """
    Takes a string or a list of strings and
    returns a list of strings
    """

    if maybe_list is None:
        return []

    if isinstance(maybe_list, list):
        return maybe_list
    return [maybe_list] * repeat
