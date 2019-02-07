import pytest
import requests
import json
import http.client
from configparser import ConfigParser
import os


def pytest_generate_tests(metafunc):
    funcarglist = metafunc.cls.params[metafunc.function.__name__]
    argnames = list(funcarglist[0])
    metafunc.parametrize(argnames, [[funcargs[name] for name in argnames] for funcargs in funcarglist])


class TestClass:
    @classmethod
    def setup_class(cls):
        cls.conn = Connection()
        cls.test_utils = TestUtils()

    configs = {
        "test_find": "test_find.ini",
        "test_search": "test_search.ini",
        "test_get_people_credits": "test_get_people_credits.ini"
    }
    params = {}

    for test_method, test_config in configs.items():
        config_list = []
        config_path = os.path.join('test_configs', test_config)
        config_data = ConfigParser()
        config_data.read(config_path)
        sections = config_data.sections()
        ''' for each section of the test config file -- each section is an individual test '''
        for test_section in sections:
            section_options = config_data.options(test_section)
            test_dictionary = {}
            for opt in section_options:
                opt_value = config_data.get(test_section, opt)
                test_dictionary[opt] = opt_value
            try:
                params[test_method].append(test_dictionary)
            except KeyError:
                params[test_method] = [test_dictionary]
    '''
    def test_get_list(self):
        # TODO: 
        pass

    def test_get_reviews(self):
        # TODO: 
        pass

    def test_delete_list(self, list_id):
        #TODO: Test to delete a list using DELETE REST call to /list endpoint.  Should take valid and invalid inputs and deal with appropriately (deleting specific list or throwing expected error)  Test will verify that list no longer shows up in lists when queried for.
        pass

    def test_create_list(self, name, description, list_name, language):
        # TODO: test to create list using POST REST call to /list. Verify list creation with Get Details /list function. Test config will run tests for combinations fo name, description and language parameters -- none, 'non-standard' characters, etc. Verify inablitity to create list when write permissions are not allowed.
        pass

    def test_add_movie_to_list(self, list_id, movie_id):
        # TODO: test adding movie to a list using POST REST call to /list/{list_id}/add_item.  Tests to include valid/invalid movies and list_ids -- existing, non-existent with and without write permissions
        pass

    def test_remove_movie_from_list(self, list_id, movie_id):
        # TODO: test removing movie to a list using POST REST call to /list/{list_id}/remove_item.  Tests to include valid/invalid movies and list_ids -- existing, non-existent with and without write permissions
        pass

    def test_clear_list(self, list_id):
        # TODO: test removing all movies to a list using POST REST call to /list/{list_id}/clear.  Tests to include valid/invalid list_id, existing, non-existent with and without write permissions
        pass
        
    def test_get_genres(self, verify_genres)
        # TODO: test getting genre list with GET REST call to /genre/{movie|tv}/list endpoint. Verify expected genres are present for TV and Movie.  Comare the id's of TV vs Moview genres, verify there is no intersections. 
        pass
    '''

    def test_get_people_credits(self, person_id, credit_type, verify_ids):
        tmp_conn = Connection()
        endpoint = "/3/person/%s/%s?api_key=%s" % (person_id, credit_type, self.conn.api_key)
        res = tmp_conn.http_client_request(endpoint)
        data = json.loads(res.read())
        if verify_ids:
            self.test_utils.verify_ids_in_result(data, verify_ids, results_key="cast")
        else:
            print(data)
            assert len(data["cast"]) == 0, "FAIL: Found data in 'cast' category where not expected"

    def test_find(self, external_source, external_id, language, verify_ids, category):
        tmp_conn = Connection()
        endpoint = "/3/find/%s?external_source=%s&api_key=%s" % (external_id, external_source, self.conn.api_key)
        if language: endpoint += "&language=%s" % language
        res = tmp_conn.http_client_request(endpoint)
        data = json.loads(res.read())

        if verify_ids:
            self.test_utils.verify_ids_in_result(data, verify_ids, results_key=category)
        else:
            print(data)
            assert len(data[category]) == 0, "FAIL: Found data in %s category where not expected" % category

    def test_search(self, search_type, query, page, language, verify_ids, status_code, status_message):
        tmp_conn = Connection()
        endpoint = "/3/search/%s?" % search_type
        if page: endpoint += "page=%s" % page
        if language: endpoint += "&language=%s" % language
        endpoint += "&query=%s&api_key=%s" % (query, self.conn.api_key)
        data = json.loads(tmp_conn.http_client_request(endpoint).read())

        if status_code:
            self.test_utils.check_negative_test_code_and_message(data, status_code, status_message)
        elif verify_ids:
            ''' verify expected ids are found in results '''
            self.test_utils.verify_ids_in_result(data, verify_ids, results_key="results")
        elif not verify_ids:
            assert data["total_results"] == 0, "FAIL: results returned when not expecting anything"


class TestUtils:
    def __init__(self):
        pass

    @staticmethod
    def check_negative_test_code_and_message(data, status_code, status_message):
        """
        verifies that expected status_message and status_code show up when expecting error
        :param data: json results from api query
        :param status_code: string from config file
        :param status_message: string from config file
        :return:
        """
        ''' specifying a status code in config indicates negative test '''
        print(data)
        assert data["status_message"] == status_message, "FAIL: Did not get expected status message"
        assert data["status_code"] == int(status_code), "FAIL: Did not get expected status code"

    @staticmethod
    def verify_ids_in_result(data, csv_id_string, id_name="id", results_key="results"):
        """
        loops through list of fields and verifies they exist in result data
        :param data: json results from api query
        :param csv_config_string: string from config in csv list
        :param results_key:
        :return:
        """
        ''' verify expected ids are found in results '''
        ids = [i.strip() for i in csv_id_string.split(',')]
        for result_id in ids:
            assert int(result_id) in ([r[id_name] for r in data[results_key]]), "FAIL: Expected to find %s: %s in list of returned %s" % (id_name, result_id, results_key)


class Connection:
    def __init__(self):
        config_data = ConfigParser()
        config_data.read('connection_settings.ini')
        try:
            self.api_url = config_data["CONNECTION_SETTINGS"]["api_url"]
            self.api_key = config_data["CONNECTION_SETTINGS"]["api_key"]
        except KeyError as e:
            print("Unable to get api_url from config file: %s" % e)
            exit(-1)

        self.connection = http.client.HTTPSConnection(self.api_url)

    def http_client_request(self, endpoint, request_type="GET", request_body=None):
        if request_body:
            pass
        else:
            request_body = "{}"
        self.connection.request(request_type, endpoint, body=request_body)
        res = self.connection.getresponse()

        return res
