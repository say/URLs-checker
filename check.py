#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from core import urlproc
from core import fileproc

NEWLINE_ESCAPED = "%0A"


def clone_repo(git_path):
    """
    clone and name a git repository.
    """
    base_path = os.path.basename(git_path)
    os.system("git clone " + git_path + " " + base_path)
    return base_path


def del_repo(base_path):
    """
    delete repository.
    """
    os.system("rm -R -f " + base_path)
    return True


def white_listed(url, white_listed_urls, white_listed_patterns):
    """
    check if link is in the white listed URLs or patterns to ignore.
    """
    # check white listed urls
    if url in white_listed_urls:
        return True

    # check white listed patterns
    i = 0
    while i < len(white_listed_patterns):
        if white_listed_patterns[i] in url:
            return True
        i += 1

    # default return
    return False


def check_repo(file_paths, print_all, white_listed_urls, white_listed_patterns):
    """
    check all urls extracted from all files in a repository.
    """
    # loop files
    results = []
    for file in file_paths:

        # collect links from each file
        urls = fileproc.collect_links_from_file(file)

        # eliminate white listed urls and white listed white listed patterns
        if len(white_listed_urls) > 0 or len(white_listed_patterns) > 0:
            urls = [url for url in urls
                    if not white_listed(url,
                                        white_listed_urls,
                                        white_listed_patterns)]

        # if some links are found, check them
        if urls != []:
            print("\n", file, "\n", "-" * len(file))
            file_results = urlproc.check_urls(file, urls)
            results.append(f"#### {file}{NEWLINE_ESCAPED}{file_results}")

        # if no urls are found, mention it if required
        else:
            if print_all == "True":
                print("\n", file, "\n", "-" * len(file))
                print("No urls found.")

    output = f"{NEWLINE_ESCAPED}{NEWLINE_ESCAPED}".join(results)
    os.system(f"echo \"::set-output name=urls::{output}\"")


if __name__ == "__main__":
    # read input variables
    git_path = os.getenv("INPUT_GIT_PATH", "")
    file_types = os.getenv("INPUT_FILE_TYPES", "").split(",")
    print_all = os.getenv("INPUT_PRINT_ALL", "")
    white_listed_urls = os.getenv("INPUT_WHITE_LISTED_URLS", "").split(",")
    white_listed_patterns = os.getenv(
        "INPUT_WHITE_LISTED_PATTERNS", "").split(",")

    # clone project repo
    base_path = os.path.basename(git_path)

    # get all file paths
    file_paths = fileproc.get_file_paths(base_path, file_types)

    # check repo urls
    check_repo(file_paths, print_all, white_listed_urls, white_listed_patterns)

    # delete repo when done
    deletion_status = del_repo(base_path)
    print("Finished")
