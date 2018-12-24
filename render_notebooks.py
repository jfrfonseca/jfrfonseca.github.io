#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
"""


"""
# IMPORTS
"""

import os
import re
import sys
import datetime
import subprocess


"""
# UTIL
"""


def publish_notebook(ipynb_file, commit_date, post_file_name):
    fil = str(ipynb_file).replace(' ', '\ ')
    p = subprocess.run(
        args=['/'.join(sys.executable.split('/')[:-1])+f'/jupyter nbconvert --to markdown notebooks/{fil}'],
        shell=True
    )
    os.rename('notebooks/' + ipynb_file.replace('.ipynb', '.md'), '_posts/' + post_file_name)

    # Add headers
    with open('_posts/' + post_file_name, 'r') as fin:
        content = fin.read()
    content = '''---
layout: post
title: "{}"
date: {}
categories:
    - jupyter notebook
---
'''.format(ipynb_file.replace('.ipynb', ''),
           commit_date.strftime('%Y-%m-%d %H:%M:%S %z')) + content

    with open('_posts/' + post_file_name, 'w') as fout:
        fout.write(content)


"""
# RUNTIME
"""


UPDATE_OLD_POSTS = True

if __name__ == '__main__':

    # Get all existing posts
    existing_posts = os.listdir('_posts')

    # Iterate every notebook
    for ipynb_file in os.listdir('notebooks'):
        if not ipynb_file.startswith('_') and ipynb_file.endswith('.ipynb'):

            # Get the post name for the notebook
            post_name = re.sub(r'\W+', '', ipynb_file.replace('.ipynb', '').replace(' ', '_').lower()) + '.md'

            # Get the current version post name
            p = subprocess.check_output(
                args=["git", "log", "-1", "--format=%cd", f"notebooks/{ipynb_file}"]
            )
            commit_date = datetime.datetime.strptime(p.decode().strip(), "%c %z")
            post_file_name = commit_date.strftime(f'%Y-%m-%d-{post_name}')

            # Get older post names for the notebook
            older_versions = [p for p in existing_posts if p.endswith(post_name)]

            # If brand-new post
            if len(older_versions) == 0:

                # Create
                publish_notebook(ipynb_file, commit_date, post_file_name)
                print("PUBLISH {}".format(ipynb_file))

            # If updating an older post
            elif (len(older_versions) == 1) and (post_file_name != older_versions[0]):

                # Keep the old filename
                post_file_name = older_versions[0]

                # Update
                publish_notebook(ipynb_file, commit_date, post_file_name)
                print("UPDATE {}".format(ipynb_file))

            elif len(older_versions) > 1:
                raise Exception('>1 POSTS WITH THE SAME NAME! {}'.format(post_name))

            else:
                print('KEEP {}'.format(ipynb_file))
