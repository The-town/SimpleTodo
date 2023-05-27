from typing import List, Dict

from imapclient import IMAPClient
import pyzmail

import config


class Imap:
    def __init__(self):
        self.server = None

    def login(self):
        self.server = IMAPClient(config.rule_file["Mail"]["imap_server"], use_uid=True)
        self.server.login(config.rule_file["Mail"]["user"], config.rule_file["Mail"]["password"])

    def get_content_of_messages(self) -> tuple:
        """
        メッセージのタイトルとbodyを辞書型で取得するメソッド

        Returns
        -------
        messages_body: Tuple[Dict, ...]
        """
        self.server.select_folder('INBOX')
        messages = self.server.search(['FROM', config.rule_file["AddTodoFromMail"]["address"]])

        content_of_messages: List[Dict, ...] = []
        for msg in messages:
            raw_messages = self.server.fetch([msg], ['BODY[]'])
            message = pyzmail.PyzMessage.factory(raw_messages[msg][b'BODY[]'])

            subject = message.get_subject()
            body = message.text_part.get_payload().decode(message.text_part.charset)

            content_of_messages.append({"subject": subject, "body": body})

        return tuple(content_of_messages)
