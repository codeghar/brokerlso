import logging
import sys

import pytest

from brokerlso.qmfv2 import RequestCmd

FORMAT = "%(asctime)s : %(pathname)s : %(name)s : %(module)s : %(funcName)s : %(lineno)d : %(levelname)s : %(message)s"
date_format = "%Y%m%d-%H%M%S-%f"
logging.basicConfig(format=FORMAT, level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger("test_brokerlso")


class TestRequestExchange:
    @pytest.mark.create
    def test_create_exchange_myexchange(self):
        req = RequestCmd()
        exchange = "myexchange"
        exchange_type = "fanout"
        content, properties = req.create_exchange(name=exchange)
        logger.debug("Content -> {0}".format(content))
        logger.debug("Properties -> {0}".format(properties))

        expected_content = {"_object_id": {"_object_name": "org.apache.qpid.broker:broker:amqp-broker"},
                            "_method_name": "create",
                            "_arguments": {"type": "exchange",
                                            "name": exchange,
                                            "strict": True,
                                            "properties": {"auto-delete": False,
                                                           "qpid.auto_delete_timeout": 10,
                                                           "exchange-type": exchange_type}}}
        logger.debug("Expected content -> {0}".format(expected_content))

        expected_properties = {"x-amqp-0-10.app-id": "qmf2", "qmf.opcode": "_query_request", "method": "request"}
        logger.debug("Expected properties -> {0}".format(expected_properties))

        assert content == expected_content

        assert properties == expected_properties

    @pytest.mark.delete
    def test_delete_exchange_myexchange(self):
        req = RequestCmd()
        exchange = "myexchange"
        content, properties = req.delete_exchange(name=exchange)
        logger.debug("Content -> {0}".format(content))
        logger.debug("Properties -> {0}".format(properties))

        expected_content = {"_object_id": {"_object_name": "org.apache.qpid.broker:broker:amqp-broker"},
                            "_method_name": "delete",
                            "options": {"type": "exchange", "name": exchange, "options": dict()}}
        logger.debug("Expected content -> {0}".format(expected_content))

        expected_properties = {"x-amqp-0-10.app-id": "qmf2", "qmf.opcode": "_query_request", "method": "request"}
        logger.debug("Expected properties -> {0}".format(expected_properties))

        assert content == expected_content

        assert properties == expected_properties

    @pytest.mark.list
    def test_list_exchanges(self):
        req = RequestCmd()
        content, properties = req.list_exchanges()
        logger.debug("Content -> {0}".format(content))
        logger.debug("Properties -> {0}".format(properties))

        expected_content = {"_what": "OBJECT", "_schema_id": {"_class_name": "exchange"}}
        logger.debug("Expected content -> {0}".format(expected_content))

        expected_properties = {"x-amqp-0-10.app-id": "qmf2", "qmf.opcode": "_query_request", "method": "request"}
        logger.debug("Expected properties -> {0}".format(expected_properties))

        assert content == expected_content

        assert properties == expected_properties
