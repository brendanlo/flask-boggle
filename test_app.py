from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')

            # test that you're getting a template
            html = response.get_data(as_text=True)
            self.assertIn('<button class="word-input-btn">Go</button>', html)
            # add a line of comment in html

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.post('/api/new-game')

            # .json converts the response from JSON into a python object
            gameId_board_obj = response.json

            self.assertIsNotNone(gameId_board_obj['gameId'])
            # check that the board object is a list
            self.assertEqual(type(gameId_board_obj['board']), type([]))
            # check the first index of the board object is also a list
            self.assertEqual(type(gameId_board_obj['board'][0]), type([]))
            # check whether the new gameId is a key in games
            self.assertIn(gameId_board_obj['gameId'], games)
