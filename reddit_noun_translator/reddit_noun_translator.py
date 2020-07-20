import argparse
import json
from typing import Dict, List, Iterable, Set, Sequence, Tuple
import os

from googletrans import Translator
import nltk
import praw

from reddit_noun_translator.decorators import log_elapsed_time

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')
try:
    nltk.data.find('corpora/words')
except LookupError:
    nltk.download('words')


class RedditNounTranslator:
    DEFAULT_TARGET_LANGUAGE = 'es'
    DEFAULT_NUM_POSTS = 100
    DEFAULT_OUTPUT_PATH = 'output.txt'
    ALL_WORDS = nltk.corpus.words.words()

    def __init__(self, api_credentials: Dict, target_language: str = DEFAULT_TARGET_LANGUAGE,
                 num_posts: int = DEFAULT_NUM_POSTS, output_file: str = DEFAULT_OUTPUT_PATH) -> None:
        self.reddit = praw.Reddit(**api_credentials)
        self.target_language = target_language
        self.num_posts = num_posts
        self.output_file = output_file
        self.translator = Translator()

    def translate_nouns_from_reddit_posts(self) -> None:
        """ Gathers the titles of posts from Reddit, extracts the nouns, and writes them to a file along with their
        translation """
        titles = self.download_post_titles()
        english_nouns = RedditNounTranslator.extract_nouns_from_titles(titles)
        translated_noun_pairs = self.make_translated_noun_pairs(english_nouns)
        self.write_pairs_to_output_file(translated_noun_pairs)

    @log_elapsed_time
    def download_post_titles(self) -> List[str]:
        """
        Returns:
            (list(str)) A list of post titles from reddit
        """
        return [post.title for post in self.reddit.subreddit("all").hot(limit=self.num_posts)]

    @staticmethod
    @log_elapsed_time
    def extract_nouns_from_titles(titles: Iterable[str]) -> Set[str]:
        """
        Args:
            titles (Iterable(str)): An iterable of titles
        Returns:
            (set(str)) The set of all nouns from all of the given titles
        """
        return {noun for title in titles for noun in RedditNounTranslator.extract_nouns(title)}

    @staticmethod
    def extract_nouns(title: str) -> Set[str]:
        """
        Args:
            title (str): The title of a Reddit post
        Returns:
            (set(str)) The set of all nouns from the given title
        """
        sentences = nltk.sent_tokenize(title)
        tokenized_sentences = [tokenized_sentence for sentence in sentences for tokenized_sentence in
                               nltk.word_tokenize(sentence)]
        return {word for (word, part_of_speech) in nltk.pos_tag(tokenized_sentences)
                if RedditNounTranslator.is_noun(part_of_speech) and RedditNounTranslator.is_english_word(word)}

    @log_elapsed_time
    def make_translated_noun_pairs(self, nouns: Iterable[str]) -> List[Tuple[str, str]]:
        """
        Args:
            nouns (Iterable(str)): An iterable of strings that are nouns

        Returns:
            (list(str, str)) A list of tuples with the first item being the english word, and the second the translation
        """
        return [(noun, self.translator.translate(noun, src='en', dest=self.target_language).text) for noun in nouns]

    @log_elapsed_time
    def write_pairs_to_output_file(self, pairs: Sequence[Tuple[str, str]]) -> None:
        """
        Writes the pair of words line by line into the output file
        Args:
            pairs (Sequence(tuple(str, str))): A sequence of 2-tuples containing strings
        """
        dir_name = os.path.dirname(self.output_file)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(self.output_file, 'w', encoding='utf-8') as output_file:
            for first, second in pairs:
                output_file.write(f'{first} : {second}\n')

    # Helpers
    @staticmethod
    def is_noun(pos: str) -> bool:
        """
        Args:
            pos: The part of speech that is returned by nltk's part of speech tagger

        Returns:
            True if pos is NN or NNS, False otherwise
        """
        return pos in {'NN', 'NNS'}

    @staticmethod
    def is_english_word(word: str) -> bool:
        """
        Args:
            word (str): The word to be checked

        Returns:
            (bool) True if it's in nltk's corpus of words, False otherwise
        """
        return isinstance(word, str) and word.lower() in RedditNounTranslator.ALL_WORDS


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--credentials', type=str, default='keys/credentials.json',
                        help='path to Reddit API credentials file.', metavar='')
    parser.add_argument('-l', '--target_language', type=str, default=RedditNounTranslator.DEFAULT_TARGET_LANGUAGE,
                        help='language to translate the nouns to', metavar='')
    parser.add_argument('-n', '--num_posts', type=int, default=RedditNounTranslator.DEFAULT_NUM_POSTS,
                        help='number of posts to use', metavar='')
    parser.add_argument('-o', '--output-file', type=str, default=RedditNounTranslator.DEFAULT_OUTPUT_PATH,
                        help='Path to output file', metavar='')
    args = parser.parse_args()
    with open(args.credentials, 'r') as api_credentials_file:
        credentials = json.load(api_credentials_file)
    r = RedditNounTranslator(credentials, target_language=args.target_language, num_posts=args.num_posts,
                             output_file=args.output_file)
    r.translate_nouns_from_reddit_posts()
