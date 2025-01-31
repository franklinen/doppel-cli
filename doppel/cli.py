"""
Implementation for ``doppel-test``
"""

import os

from sys import stdout

import click

from doppel.reporters import SimpleReporter
from doppel.PackageAPI import PackageAPI


@click.command()
@click.option("--files", "-f", default=None, help="Comma-delimited list of doppel output files.")
@click.option(
    "--errors-allowed",
    default=0,
    help="Integer number of errors to allow before returning non-zero exit code. Default is 0.",
)
@click.option(
    "--version",
    default=False,
    help="Get the current version of doppel-test",
    is_flag=True,
)
def main(files: str, errors_allowed: int, version: bool) -> None:
    """
    doppel is a a continuous integration tool for testing
    the continuity of APIs for libraries implemented in
    different languages.

    :param files: A string with a comma-delimited list of
        file paths to JSON files generated by
        ``doppel-describe``.
    :param errors_allowed: Number of errors that are
        permissible before throwing a non-zero exit
        code. Set this to a higher value to make doppel-cli
        more permissive.
    :param version: Get the current version of doppel-test.
    """
    if version is True:
        version_file = os.path.join(os.path.dirname(__file__), "VERSION")
        with open(version_file, "r") as f:
            out = f.read()
        stdout.write(out)
        return

    if files is None:
        raise RuntimeError('Missing option "--files"')

    print("Loading comparison files")

    f_list = files.split(",")

    # Check if these are legit package objects
    pkgs = [PackageAPI.from_json(f) for f in f_list]

    # Report
    reporter = SimpleReporter(pkgs, errors_allowed)
    reporter.compare()


if __name__ == "__main__":
    main()
