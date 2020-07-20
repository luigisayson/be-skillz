import os
from unittest import mock
import unittest

from reddit_noun_translator.reddit_noun_translator import RedditNounTranslator

TEST_CREDENTIALS = {
    "user_agent": "Test Platform:Test App:0.1.0 (by /u/test_user)",
    "client_secret": "client_secret_string",
    "client_id": "client_id"
}
TEST_LANGUAGE = 'es'
TEST_NUM_POSTS = 300
TEST_OUTPUT = 'temp/outputfile.txt'


class RedditNounTranslatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.patcher = mock.patch('reddit_noun_translator.reddit_noun_translator.praw.Reddit')
        cls.mocked_reddit_client = cls.patcher.start()
        cls.rnt = RedditNounTranslator(TEST_CREDENTIALS, target_language=TEST_LANGUAGE, num_posts=TEST_NUM_POSTS,
                                       output_file=TEST_OUTPUT)

    @classmethod
    def tearDownClass(cls):
        cls.patcher.stop()
        if os.path.exists(TEST_OUTPUT):
            os.remove(TEST_OUTPUT)

    def test_init(self):
        self.mocked_reddit_client.assert_called_once_with(**TEST_CREDENTIALS)
        self.assertEqual(self.rnt.target_language, TEST_LANGUAGE, msg="Instance of RedditNounTranslator's "
                                                                      "target_language should be the same as what "
                                                                      "was passed in")
        self.assertEqual(self.rnt.num_posts, TEST_NUM_POSTS, msg="Instance of RedditNounTranslator's num_posts should "
                                                                 "be the same as what was passed in")
        self.assertEqual(self.rnt.output_file, TEST_OUTPUT, msg="Instance of RedditNounTranslator's output_file "
                                                                "should be the same as what was passed in")

    def test_download_posts(self):
        class MockSubreddit:
            def __init__(self):
                pass

            def hot(self, limit):
                return [MockPost() for _ in range(limit)]

        class MockPost:
            def __init__(self):
                self.title = 'mock_title'

        self.rnt.reddit.subreddit.return_value = MockSubreddit()
        titles = self.rnt.download_post_titles()
        self.assertTrue(all([isinstance(title, str) for title in titles]), msg='A list containing strings should '
                                                                               'have been returned')
        self.assertEqual(len(titles), self.rnt.num_posts, msg="The length of posts returned should be the same as the "
                                                              "value of num_posts that was passed in ")

    def test_make_translated_noun_pairs(self):
        english_nouns = ['dog', 'cat']
        spanish_nouns = ['perro', 'gato']
        expected = list(zip(english_nouns, spanish_nouns))
        actual = self.rnt.make_translated_noun_pairs(english_nouns)
        self.assertEqual(expected, actual, msg=f'expected: {expected} but got: {actual}')

    def test_extract_nouns_from_titles(self):
        test_titles = ['This is the first title', 'Title two with more nouns: apple, dog, cat']
        expected = {'title', 'apple', 'dog', 'cat'}
        actual = RedditNounTranslator.extract_nouns_from_titles(test_titles)
        self.assertEqual(expected, actual, msg=f'expected: {expected} but got: {actual}')

    def test_is_noun(self):
        self.assertTrue(RedditNounTranslator.is_noun('NN'))
        self.assertTrue(RedditNounTranslator.is_noun('NNS'))

        self.assertFalse(RedditNounTranslator.is_noun('NNA'))
        self.assertFalse(RedditNounTranslator.is_noun(''))
        self.assertFalse(RedditNounTranslator.is_noun(1))
        self.assertFalse(RedditNounTranslator.is_noun(None))

    def test_is_english_word(self):
        self.assertTrue(RedditNounTranslator.is_english_word('yes'))
        self.assertTrue(RedditNounTranslator.is_english_word('Yes'))
        self.assertTrue(RedditNounTranslator.is_english_word('yEaH'))

        self.assertFalse(RedditNounTranslator.is_english_word('0'))
        self.assertFalse(RedditNounTranslator.is_english_word(0))
        self.assertFalse(RedditNounTranslator.is_english_word([]))
        self.assertFalse(RedditNounTranslator.is_english_word(None))
        self.assertFalse(RedditNounTranslator.is_english_word("'"))
        self.assertFalse(RedditNounTranslator.is_english_word("."))
        self.assertFalse(RedditNounTranslator.is_english_word("`"))
        self.assertFalse(RedditNounTranslator.is_english_word('nein'))
        self.assertFalse(RedditNounTranslator.is_english_word('\U0001F600'))  # emoji

    def test_write_pairs_to_output_file(self):
        first = 'First'
        second = 'Second'
        self.rnt.write_pairs_to_output_file([(first, second)])
        self.assertTrue(os.path.exists(TEST_OUTPUT))

        with open(TEST_OUTPUT, 'r') as file:
            output = file.read().strip()
        self.assertEqual(f'{first} : {second}', output, msg=f'File should have been written like: {first} : {second}'
                                                            f'but got {output} instead')


if __name__ == '__main__':
    unittest.main(verbosity=2)
