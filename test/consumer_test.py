from rembed import *

from hamcrest import *
from mock import *
import pytest
import requests

def test_should_find_oembed_url_using_json_by_default():
    assert_that(get_oembed_url(), equal_to('http://example.com/oembed?format=json'))

def test_should_find_oembed_url_using_json_when_specified():
    assert_that(get_oembed_url(format = 'json'), equal_to('http://example.com/oembed?format=json'))

def test_should_find_oembed_url_using_xml_when_specified():
    assert_that(get_oembed_url(format = 'xml'), equal_to('http://example.com/oembed?format=xml'))

def test_should_return_none_if_link_not_present():
    assert_that(get_oembed_url(fixture = 'no_json_oembed.html'), none())

def test_should_return_none_if_href_not_present():
    assert_that(get_oembed_url(fixture = 'json_oembed_no_href.html'), none())

def test_should_return_none_for_invalid_html():
    assert_that(get_oembed_url(fixture = 'invalid.html'), none())

def test_should_throw_error_when_invalid_format_specified():
    with pytest.raises(REmbedError):
        get_oembed_url(format = 'txt')

def test_should_throw_error_on_error_response():
    with pytest.raises(REmbedError):
        get_oembed_url(ok = False)

def get_oembed_url(fixture = 'valid_oembed.html', format = None, ok = True):
    with patch('requests.get') as mock_get:
        response = Mock()
        response.ok = ok
        response.text = open('test/fixtures/' + fixture).read()
        mock_get.return_value = response

        consumer = REmbedConsumer()

        if format:
            return consumer.get_oembed_url('http://example.com', format)
        else:
            return consumer.get_oembed_url('http://example.com')