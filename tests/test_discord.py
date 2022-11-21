from .context import daily

import unittest


class DiscordTestSuite(unittest.TestCase):

    discord = daily.Discord()

    def test_log_messages(self):
        self.assertIsNotNone(self.discord.log_messages(media_only = True))


if __name__ == '__main__':
    unittest.main()
