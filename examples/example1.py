"""Examples to list, create, and delete queues and exchanges using Qpid Proton and brokerlso

Requires user to provide a valid URL to a working broker when running the script
"""

import logging
import sys

from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container

from brokerlso.qmfv2 import RequestCmd

FORMAT = "%(asctime)s : %(pathname)s : %(name)s : %(module)s : %(funcName)s : %(lineno)d : %(levelname)s : %(message)s"
logging.basicConfig(format=FORMAT, level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger("brokerlso-example1")


class Example1(MessagingHandler):
    """Example usage of brokerlso to list, create, and delete queues and exchanges with QMFv2"""
    def __init__(self, url):
        super(Example1, self).__init__()

        self.default_exchange = "qmf.default.direct"
        logger.debug("default exchange for request messages {0}".format(self.default_exchange))

        self.default_subject = "broker"
        logger.debug("subject {0}".format(self.default_subject))

        self.url = "/".join([url, self.default_exchange])
        logger.debug("url {0}".format(self.url))

        reqcmd = RequestCmd()
        myfirstqueue = "MYFIRSTQUEUE"
        myfirstexchange = "MYFIRSTEXCAHNGE"
        self.request_messages = [
            reqcmd.list_queues(),
            reqcmd.create_queue(myfirstqueue),
            reqcmd.list_queues(),
            reqcmd.purge_queue(myfirstqueue),
            reqcmd.list_queues(),
            reqcmd.delete_queue(myfirstqueue),
            reqcmd.list_exchanges(),
            reqcmd.create_exchange(myfirstexchange),
            reqcmd.list_exchanges(),
            reqcmd.delete_exchange(myfirstexchange),
        ]
        logger.debug("requests {0}".format(self.request_messages))

    def on_start(self, event):
        self.sender = event.container.create_sender(self.url)
        self.receiver = event.container.create_receiver(self.sender.connection, None, dynamic=True)

    def next_message(self):
        if self.receiver.remote_source.address:
            content, properties = self.request_messages[0]
            logger.debug("message content/body {0}".format(content))
            logger.debug("message properties {0}".format(properties))
            message = Message(reply_to=self.receiver.remote_source.address,
                              body=content,
                              properties=properties,
                              subject=self.default_subject)
            logger.debug("request message {0}".format(message))
            self.sender.send(message)

    def on_link_opened(self, event):
        if event.receiver == self.receiver:
            self.next_message()

    def on_message(self, event):
        latest_message = self.request_messages.pop(0)
        logger.debug("latest message {0}".format(latest_message))

        latest_response = event.message.body
        logger.debug("latest response {0}".format(latest_response))

        if self.request_messages:
            self.next_message()
        else:
            event.connection.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Run example1 of using brokerlso with Qpid Proton')
    parser.add_argument('url', action='store',
                        help='Valid amqp(s) URL, e.g. amqp://user:password@localhost:5672')

    args = parser.parse_args()
    logger.debug("user provided url {0}".format(args.url))

    url = args.url[:-1] if args.url[-1] == "/" else args.url  # Remove last "/" if it exists as it's added in Example1
    logger.debug("fixed url {0}".format(url))

    Container(Example1(url=url)).run()
