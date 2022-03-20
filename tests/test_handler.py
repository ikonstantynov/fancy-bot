from unittest.mock import Mock
from handler import start
from telegram import Update


class TestHandler:

    def test_true(self):
        assert True is True

    def test_start(self):
        mock_reply_markdown_v2 = Mock()
        mock_mention_markdown_v2 = Mock(return_value='User Name')
        update = Update(
            update_id=11223344,
            message=Mock(reply_markdown_v2=mock_reply_markdown_v2),
            effective_user=Mock(mention_markdown_v2=mock_mention_markdown_v2)
        )

        assert start(update, None) is None