---
layout: post
title: "Youtube Comments to Python PANDAS"
date: 2018-11-18 18:35:58 -0200
categories:
    - jupyter notebook
---

# Youtube Comments to PANDAS

So, my very beloved humanities-student girlfriend needed to study all the comments made on YouTube about this video.  
And asked for my data-scientist help :)

First thing I did was get on Google and search for "python download YouTube comments" and found this 2015 MIT-licensed python snipped by Egbert Bouman (@egbertbouman). It was very close to what I needed, because:
- It **does not** uses YouTube's API, requiring no registration from the user
- It's MIT-licensed, thereby compatible with my GF's academic needs
- It does a viable scrapping from the browser-visible page itself
- It returns the comments in a list-of-dicts format that can be easily exported to PANDAS, and then to MS Excel.
- It also extracts the REPLIES to comments
- It uses few dependencies, that can all be installed with the single line below


```python
!pip install requests cssselect lxml
```

    Requirement already satisfied: requests in /home/zeff/anaconda3/lib/python3.6/site-packages
    Requirement already satisfied: cssselect in /home/zeff/anaconda3/lib/python3.6/site-packages
    Requirement already satisfied: lxml in /home/zeff/anaconda3/lib/python3.6/site-packages


The original July 27th, 2017 version can be found here, and a copy of it is in the "code" directory of my blog.


```python
cd ../code
```

    /home/zeff/Documents/jfrfonseca.github.io/code


So, all I needed to do was get the YouTube ID of the video (all that goes after "https://www.youtube.com/watch?v=") and import @egbertbouman's **download_comments** function, run it, and put the resulting data in to a PANDAS DataFrame


```python
# Python's standard library
import datetime

# PIP-available libraries
import pandas as pd
from dateutil.relativedelta import relativedelta

# @egbertbouman's library
from youtube_comments_downloader import download_comments

# Video ID
youtube_id = 'mC_vrzqYfQc'
```


```python
# Download the comments to a list, noting the time
now = datetime.datetime.utcnow()
comments_list = download_comments(youtube_id)

# Convert the list to a Pandas DataFrame
df_comments = pd.DataFrame().from_dict(comments_list)
```

Then I just dump the received comments into an MS Excel file using pandas, saving the video ID and the date-time of access in the file name.


```python
df_comments.to_excel('youtube_comments_{}_{}.xlsx'.format(youtube_id, now))
```

I noticed 2 things gone unexpected:
- There is a warning about a URL that could not be parsed by Excel.
- Youtube's way of expressing when a comment was made is totally weird.

No need to worry about the first one, I can do some parsing in PANDAS to solve the second.

The CID column in the retrieved table contains values with a "dot". The comments with a dot are replies to a comment identified for the value before the dot, being the value after the dot an ID for the reply itself.

The code below parses the relative date of posting the comment informed by YouTube into a date format, saving the parsed dataframe.


```python
def comment_time(now, time_text):
    time_text = time_text.replace(' (editado)', '')
    splitted = time_text.split(' ')
    if len(splitted) == 3:
        value, unity, _ = tuple(splitted)
        try:
            value = int(value)
        except:
            return time_text
        else:
            if unity in 'segundo;segundos;second;seconds':
                return now - relativedelta(seconds=value)
            elif unity in 'minuto;minutos;minute;minutes':
                t = now - relativedelta(minutes=value)
                return datetime.datetime(year=t.year, month=t.month, day=t.day, hour=t.hour, minute=t.minute)
            elif unity in 'hora;horas;hour;hours':
                t = now - relativedelta(hours=value)
                return datetime.datetime(year=t.year, month=t.month, day=t.day, hour=t.hour)
            elif unity in 'dia;dias;day;days':
                t = now - relativedelta(days=value)
                return datetime.datetime(year=t.year, month=t.month, day=t.day)
            elif unity in 'semana;semanas;week;weeks':
                t = now - relativedelta(days=7*value)
                return datetime.datetime(year=t.year, month=t.month, day=t.day)
            elif unity in 'mes;mês;meses;month;months':
                t = now - relativedelta(months=value)
                return datetime.datetime(year=t.year, month=t.month, day=t.day)
            elif unity in 'ano;anos;year;years':
                t = now - relativedelta(years=value)
                return datetime.datetime(year=t.year, month=t.month, day=t.day)
            else:
                return time_text

df_comments = df_comments.assign(probable_time=df_comments.time.apply(lambda tme: comment_time(now, tme)))
```


```python
df_comments.to_excel('youtube_comments_probable_time_{}_{}.xlsx'.format(youtube_id, now))
```

## Analises

Juuust cause I'm SUCH a great BF, I'm also adding some simple analises to the data I just collected.

I used this list to remove stopwords, and also removed:
- '', 'pra', 'vem', ',', 'vc', 'q', 'oq', 'oque', 'and'
- any word with only 1 or 2 characters

Then I normalized the words, removing spaces, punctuation and capitalization, and:
- Counted how many times each word appeared
- Counted how many comments each word appeared
- Counted how many users have used each word
- Identified the probable date of the first and last use of each word

I hope its useful :)


```python
from collections import Counter
import requests
import re

stopwords = requests.get('https://gist.githubusercontent.com/alopes/5358189/raw/2107d809cca6b83ce3d8e04dbd9463283025284f/stopwords.txt'
                        ).text.replace(' ', '').splitlines()
stopwords = set(stopwords).union({'', 'pra', 'vem', ',', 'vc', 'q', 'oq', 'oque', 'and'})

word_list = ' '.join(df_comments.text.fillna('')).split(' ')
word_list = [re.sub(r'\W+', '', w.lower()) for w in word_list]

word_count = Counter(word_list)
keys = list(word_count.keys())
for word in keys:
    if (word.lower() in stopwords) or (len(word) < 3):
        word_count.pop(word)
```


```python
from tqdm import tqdm_notebook as tqdm

normalized_text = df_comments.text.fillna('').apply(lambda w: re.sub(r'\W+', '', w.lower()))

def analize_one_word(word):
    df_occurrences = df_comments[normalized_text.str.contains(word)]
    return {
        'word': word, 'count': word_count[word],
        'number_of_comments': len(df_occurrences),
        'number_of_users': len(df_occurrences.author.unique()),
        'first_occurrence': df_occurrences.probable_time.min(),
        'last_occurrence': df_occurrences.probable_time.max()
    }

import multiprocessing
pool = multiprocessing.Pool(6)

word_analisis_list = list(tqdm(pool.imap_unordered(analize_one_word, list(word_count.keys())),
                               total=len(word_count)))
```


<p>Failed to display Jupyter Widget of type <code>HBox</code>.</p>
<p>
  If you're reading this message in Jupyter Notebook or JupyterLab, it may mean
  that the widgets JavaScript is still loading. If this message persists, it
  likely means that the widgets JavaScript library is either not installed or
  not enabled. See the <a href="https://ipywidgets.readthedocs.io/en/stable/user_install.html">Jupyter
  Widgets Documentation</a> for setup instructions.
</p>
<p>
  If you're reading this message in another notebook frontend (for example, a static
  rendering on GitHub or <a href="https://nbviewer.jupyter.org/">NBViewer</a>),
  it may mean that your frontend doesn't currently support widgets.
</p>




```python
df_analisis = pd.DataFrame().from_dict(word_analisis_list)
df_analisis = df_analisis.set_index('word')
```


```python
df_analisis.to_excel('analisis_youtube_video_comments_{}_{}.xlsx'.format(youtube_id, now))
```
