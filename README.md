Grabs a number of posts from Reddit, extracts the nouns, and writes them to a file along with their translation

Quick Start
-----------
This application requires you to use your own Reddit API credentials. Please follow the [Prequisite](https://praw.readthedocs.io/en/latest/getting_started/quick_start.html#prerequisites)
steps in `praw`'s Quick Start guide guide to get that sorted. Once you have have your `client_secret`, `client_id`, and 
your `user_agent`, Create your a file called `credentials.json` and put under `keys` (i.e. the path to the file should 
be `keys/credentials.json`). 

The file should contain only these lines:
```
{
  "user_agent": "<platform>:<app ID>:<version string> (by u/<Reddit username>",
  "client_secret": "<your client_secret>",
  "client_id": ""<your client_id>"
}
```

Usage
----------
Once that's done you can start running stuff:

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

Running Tests
-------------
To run tests, simply:
```
make tests 
# OR
python -m tests.test_reddit_noun_translator
```
