tests:
	python -m tests.test_reddit_noun_translator

default-run:
	python -m reddit_noun_translator.reddit_noun_translator

docker-build:
	docker build -f docker/release.Dockerfile