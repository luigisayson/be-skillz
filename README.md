Grabs a number of posts from Reddit, extracts the nouns, and writes them to a file along with their translation

Quick Start
-----------
This application requires you to use your own Reddit API credentials. Please follow the [Prequisite](https://praw.readthedocs.io/en/latest/getting_started/quick_start.html#prerequisites)
steps in `praw`'s Quick Start guide to get that sorted. Once you have your `client_secret`, `client_id`, and 
your `user_agent`, Create your a file called `credentials.json` and put under it `keys` (i.e. the path to the file should 
be `keys/credentials.json`). 

The file should contain only these lines:
```
{
  "user_agent": "<platform>:<app ID>:<version string> (by u/<Reddit username>",
  "client_secret": "<your client_secret>",
  "client_id": ""<your client_id>"
}
```

Once you have that, install the dependencies:
```
pip install -r requirements.txt
```

Usage
----------
For a default run (get 100 posts, translate the nouns to spanish, write to a file called 'output.txt')
```
make default-run
# OR  
python -m reddit_noun_translator.reddit_noun_translator
```

Details about options:
```
usage: python -m reddit_noun_translator.reddit_noun_translator [-h] [-c] [-l] [-n] [-o]

optional arguments:
  -h, --help              show this help message and exit
  -c , --credentials      path to Reddit API credentials file.
  -l , --target_language  language to translate the nouns to
  -n , --num_posts        number of posts to use
  -o , --output-file      Path to output file
```

Tests
-------------
To run tests, simply:
```
make tests 
# OR
python -m tests.test_reddit_noun_translator
```
Tests also run with every push/PR made. See: [sample PR](https://github.com/luigisayson/be-skillz/pull/1) 

Decisions Made/Details on Behavior:
-----------------------------------------
- Proper nouns are excluded. Translating a lot of them will just have no effect anyway.   
- nltk's part of speech tagger isn't perfect. It sometimes marks apostrophes, periods and even special characters 
  such as emojis as nouns, so each word that was tagged as a noun is also checked if it's a word, i.e. it's in 
  nltk's word corpus. It's also possible to build a set of a comprehensive set of nouns using nltk, and I could've 
  just checked if the word exists there, but that could exclude words that are not typically nouns but are being used as
  one in the sentence. 
- I also decided to get rid of duplicates. We're not counting occurrences anyway
