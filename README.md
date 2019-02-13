movie_api_tests1
======================

Running Tests from Docker image
----------
`docker run -e API_KEY=<<YOUR API KEY>> gkgosney/moviedbtest:latest`

Dockerfile used to build this image
----------
```
FROM python
ARG API_KEY
RUN apt update
RUN apt-get -y install git vim
RUN pip install -U pytest
RUN git clone https://github.com/tpoopo/TheMovieDBApiTests.git
ADD run_tests.sh run_tests.sh
CMD sh run_tests.sh
```
  
## Adding new test suite  
**In TestClass.py file, TestClass class and setup_class function add entry to 'configs' dict with the syntax `"test_somename": "test_somename.ini"`**

**Create a test function in the TestClass (ex. "test_somename")**

**Create config ini file for tests in test_configs directory (ex. "test_somename.ini")**

In the ini file, each header represents a test case, the parameters under the header are what is directly passed into the test function created above.  For example, the following snippet from the "test_find.ini" file represents two test cases, external_id, external_source, language, varify_ids and category are the parameters that the TestClass.test_find function expects.
```
[FIND_IMDB_MOVIE_1]
external_id=tt5093026
external_source=imdb_id
language=
verify_ids=433498
category=movie_results

[FIND_IMDB_TV_1]
external_id=tt4574334
external_source=imdb_id
language=
verify_ids=66732
category=tv_results
```

## Adding test to existing set

To add a new test to existing test set, simply find the ini file associated with that test and add a unique header (in square brackets) and add expected parameters underneath. 
