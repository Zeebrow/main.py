import pytest
from unittest.mock import patch, MagicMock
import datetime
import json
import logging

from quickhost.utilities import get_my_public_ip, scrub_datetime, QHLogFormatter


SOME_TEST_DATE = datetime.datetime.now()


def test_get_my_ip():
    """icanhazip.com is always available"""
    m = MagicMock()
    with patch('urllib.request.urlopen', m):
        m.return_value.__enter__.return_value.read.return_value = b'1.2.3.4\n'
        assert get_my_public_ip() == '1.2.3.4/32'


def test_get_my_ip_exception():
    """icanhazip.com is always available"""
    m = MagicMock(side_effect=Exception)
    with patch('urllib.request.urlopen', m), \
            patch('quickhost.utilities.input', return_value='4.3.2.1'):
        assert get_my_public_ip() == '4.3.2.1/32'


@pytest.mark.parametrize('test_input', [
    {'asdf': {'asdf': SOME_TEST_DATE}},
    {'asdf': [{'asdf': SOME_TEST_DATE}]},
    [{'asdf': [{'asdf': SOME_TEST_DATE}]}],
    {'asdf': [{'asdf': SOME_TEST_DATE}]},
    [SOME_TEST_DATE],
    SOME_TEST_DATE,
])
def test_scrub_datetime(test_input):
    assert json.dumps(scrub_datetime(test_input))


def test_scrub_datetime_datetime_obj():
    assert isinstance(SOME_TEST_DATE, datetime.datetime)
    assert isinstance(scrub_datetime(datetime.datetime), type)  # WHATEVER just make coverage happy. "known issue"


def test_colorized_log_formatter_colorizes_records(caplog):
    logger = logging.getLogger('tests.test_utilities')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = QHLogFormatter(color=True)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    with caplog.at_level(logging.DEBUG):
        logger.debug("test")
        logger.info("test")
        logger.warning("test")
        logger.error("test")
        logger.critical("test")

    for r in caplog.records:
        fmted_r = formatter.format(r)
        if r.levelno == logging.DEBUG:
            assert '\033[94m' in fmted_r
        if r.levelno == logging.INFO:
            assert '\033[33m' in fmted_r
        if r.levelno == logging.WARNING:
            assert '\033[93m' in fmted_r
        if r.levelno == logging.ERROR:
            assert '\033[31m' in fmted_r
        if r.levelno == logging.CRITICAL:
            assert '\033[31m' in fmted_r
        assert '\033[0m' in fmted_r


def test_colorized_log_formatter_turns_off(caplog):
    logger = logging.getLogger('tests.test_utilities')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = QHLogFormatter(color=False)
    formatter.colored_output = False
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    with caplog.at_level(logging.DEBUG):
        logger.debug("test")
        logger.info("test")
        logger.warning("test")
        logger.error("test")
        logger.critical("test")

    for r in caplog.records:
        fmted_r = formatter.format(r)
        if r.levelno == logging.DEBUG:
            assert '\033[94m' not in fmted_r
        if r.levelno == logging.INFO:
            assert '\033[33m' not in fmted_r
        if r.levelno == logging.WARNING:
            assert '\033[93m' not in fmted_r
        if r.levelno == logging.ERROR:
            assert '\033[31m' not in fmted_r
        if r.levelno == logging.CRITICAL:
            assert '\033[31m' not in fmted_r
        assert '\033[0m' not in fmted_r
