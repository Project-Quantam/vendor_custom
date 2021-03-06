#!/usr/bin/env python3
#
# Copyright (C) 2020 StatiXOS
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Merge script for AOSP.

 The source directory; this is automatically two folder up because the script
 is located in vendor/statix/scripts. Other ROMs will need to change this. The logic is
 as follows:

 1. Get the absolute path of the script with os.path.realpath in case there is a symlink,
    this script may be symlinked by a manifest so we need to account for that.
 2. Get the folder containing the script with directory name.
 3. Move into the folder that is three folders above that one and print it.

"""

import glob
import os
import shutil
import subprocess
import sys
import xml.etree.ElementTree as Et

import git

BASE_URL = "https://android.googlesource.com/platform/"
WORKING_DIR = "{0}/../../..".format(os.path.dirname(os.path.realpath(__file__)))
MANIFEST_NAME = "include.xml"
REPOS_TO_MERGE = ["manifest"]
BRANCH_STR = "android-{}".format(sys.argv[1])
REPOS_RESULTS = {}


# Useful helpers.
def list_aosp_repos():
    """ Gather all repos from AOSP. """
    aosp_repos = []
    with open('{0}/.repo/manifests/default.xml'.format(WORKING_DIR)) as aosp_manifest:
        aosp_root = Et.parse(aosp_manifest).getroot()
        for child in aosp_root:
            path = child.get('path')
            if path:
                aosp_repos.append(path)
    return aosp_repos


def read_custom_manifest():
    """ Find all repos that need to be merged. """
    print("Finding repos to merge...")
    with open('{0}/.repo/manifests/{1}'.format(WORKING_DIR, MANIFEST_NAME)) as manifest:
        root = Et.parse(manifest).getroot()
        aosp_repos = list_aosp_repos()
        for custom in root:
            custom_path = custom.get('path')
            if custom_path and custom_path in aosp_repos:
                REPOS_TO_MERGE.append(custom_path)


def force_sync():
    """ Force sync all the repos that need to be merged. """
    print("Syncing repos")
    for repo in REPOS_TO_MERGE:
        if os.path.isdir("{}{}".format(WORKING_DIR, repo)):
            shutil.rmtree("{}{}".format(WORKING_DIR, repo))

    cpu_count = str(os.cpu_count())
    subprocess.run(
        ['repo', 'sync', '-c', '--force-sync', '-f', '--no-clone-bundle', '--no-tag', '-j', cpu_count, '-q']
    )


def merge():
    """ Merge the necessary repositories and lists if a repository succeeds or fails. """
    failures = []
    successes = []
    for repo in REPOS_TO_MERGE:
        repo_str = repo
        os.chdir("{0}/{1}".format(WORKING_DIR, repo))
        if repo == "build/make":
            repo_str = "build"
        try:
            git.cmd.Git().pull('{}{}'.format(BASE_URL, repo_str), BRANCH_STR)
            successes.append(repo)
        except git.exc.GitCommandError as e:
            print(e)
            failures.append(repo)

        except git.exc.GitCommandError as e:
            print(e)
            failures.append(repo)

    REPOS_RESULTS.update({'Successes': successes, 'Failures': failures})


def get_actual_merged_repos():
    """ Gets all the repos that were actually merged and
        not the ones that were just up-to-date """
    status_zero_repos = REPOS_RESULTS['Successes']
    good_repos = []
    for repo in status_zero_repos:
        git_repo = git.Repo("{0}/{1}".format(WORKING_DIR, repo))
        commits = list(git_repo.iter_commits("HEAD", max_count=1))
        result = commits[0].message
        if BRANCH_STR in result:
            good_repos.append(repo)
    REPOS_RESULTS['Successes'] = good_repos


def print_results():
    """ Prints all repositories that will need to be manually fixed. """
    get_actual_merged_repos()
    if REPOS_RESULTS['Failures']:
        print("\nThese repositories failed to merge, fix manually: ")
        for failure in REPOS_RESULTS['Failures']:
            print(failure)
    if REPOS_RESULTS['Successes']:
        print("\nRepos that merged successfully: ")
        for success in REPOS_RESULTS['Successes']:
            print(success)
    if not REPOS_RESULTS['Failures'] and REPOS_RESULTS['Successes']:
        print("{0} merged successfully! Compile and test before pushing to GitHub.".format(BRANCH_STR))
    elif not REPOS_RESULTS['Failures'] and not REPOS_RESULTS['Successes']:
        print("Unable to retrieve any results.")


def main():
    """ Gathers and merges all repos from AOSP and
    reports all repos that need to be fixed manually. """

    read_custom_manifest()
    if REPOS_TO_MERGE:
        force_sync()
        merge()
        os.chdir(WORKING_DIR)
        print_results()
    else:
        print("No repositories to sync.")


if __name__ == "__main__":
    # Execute only if run as a script.
    main()
