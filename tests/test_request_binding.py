import logging
import sys

import pytest

from brokerlso.qmfv2 import RequestCmd

FORMAT = "%(asctime)s : %(pathname)s : %(name)s : %(module)s : %(funcName)s : %(lineno)d : %(levelname)s : %(message)s"
date_format = "%Y%m%d-%H%M%S-%f"
logging.basicConfig(format=FORMAT, level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger("test_brokerlso")


class TestRequestBinding:
    @pytest.mark.create
    def test_create_binding_myexchange_myqueue_mykey(self):
        req = RequestCmd()
        binding = "myexchange/myqueue/mykey"
        content, properties = req.create_binding(name=binding)
        logger.debug("Content -> {0}".format(content))
        logger.debug("Properties -> {0}".format(properties))

        expected_content = {"_object_id": {"_object_name": "org.apache.qpid.broker:broker:amqp-broker"},
                            "_method_name": "create",
                            "_arguments": {"type": "binding",
                                            "name": binding,
                                            "strict": True,
                                            "properties": {"auto-delete": False,
                                                           "qpid.auto_delete_timeout": 10}}}
        logger.debug("Expected content -> {0}".format(expected_content))

        expected_properties = {"x-amqp-0-10.app-id": "qmf2", "qmf.opcode": "_query_request", "method": "request"}
        logger.debug("Expected properties -> {0}".format(expected_properties))

        assert content == expected_content

        assert properties == expected_properties

    @pytest.mark.delete
    def test_delete_binding_myexchange_myqueue_mykey(self):
        req = RequestCmd()
        binding = "myexchange/myqueue/mykey"
        content, properties = req.delete_binding(name=binding)
        logger.debug("Content -> {0}".format(content))
        logger.debug("Properties -> {0}".format(properties))

        expected_content = {"_object_id": {"_object_name": "org.apache.qpid.broker:broker:amqp-broker"},
                            "_method_name": "delete",
                            "options": {"type": "binding", "name": binding, "options": dict()}}
        logger.debug("Expected content -> {0}".format(expected_content))

        expected_properties = {"x-amqp-0-10.app-id": "qmf2", "qmf.opcode": "_query_request", "method": "request"}
        logger.debug("Expected properties -> {0}".format(expected_properties))

        assert content == expected_content

        assert properties == expected_properties
