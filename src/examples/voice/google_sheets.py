"""
Library to read spreadsheet and add useful commands to it.
"""

import os
from enum import Enum
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from absl import logging
from absl import app
from datetime import datetime
import pytz

# TODO: remove this into secrets folder.
fileDir = os.path.dirname(os.path.abspath(__file__))
SECRETS_FILE = os.path.join(
    fileDir, "secrets", "1-button-cardbox-78c4daa3a219.json")
SPREADSHEET_NAME = "Baby Elsa"


class ActivityEnum(Enum):
    FEED_START = 1
    FEED_END = 2
    POOP = 3
    PEE = 4


class SpreadSheetEditor(object):
    """Object to read and write to a spreadsheet."""

    def __init__(self, secrets_file=SECRETS_FILE, spreasheet_name=SPREADSHEET_NAME):
        """Initializes spreadsheet editor."""
        self._secrets_file = secrets_file
        self._spreadsheet_name = spreasheet_name
        self._scope = ['https://spreadsheets.google.com/feeds',
                       'https://www.googleapis.com/auth/drive']
        print("Secrets file: %s \n Spreadsheet file: %s" % (self._secrets_file,
                                                            self._spreadsheet_name))
        self._spreadsheet = self._init()
        self._worksheet = self._spreadsheet.sheet1
        print(self._spreadsheet)
        print("Initialization complete.")
        self._timezone = pytz.timezone('US/Pacific')
        self._time_format = '%Y-%m-%d %H:%M:%S'

    def _init(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self._secrets_file,
                                                                       self._scope)
        gc = gspread.authorize(credentials)
        return gc.open(SPREADSHEET_NAME)

    def _get_current_time(self):
        local_time = self._timezone.localize(datetime.now())
        return local_time.strftime(self._time_format)

    def find_next_available(self, activity_enum):
        """Returns the next cell to write to."""
        col = activity_enum.value
        row_values = self._worksheet.col_values(col)
        logging.info("For column: %s, the values are %s, current time %s",
                     row_values[0], row_values[1:], self._get_current_time())

        new_row_index = len(row_values) + 1
        return new_row_index, col

    def _update_activity(self, activity_enum):
        """Updates a new row for a given activity."""
        row, col = self.find_next_available(activity_enum)
        current_time = self._get_current_time()
        logging.info("Updating cell (%d %d) with time %s",
                     row, col, current_time)
        self._worksheet.update_cell(row, col, current_time)

    def add_start_feeding(self):
        """Starts feeding session on the new row."""
        self._update_activity(ActivityEnum.FEED_START)

    def add_end_feeding(self):
        """Finishes feeding session on the new row."""
        self._update_activity(ActivityEnum.FEED_END)

    def add_pooping(self):
        """Starts pooping session on the new row."""
        self._update_activity(ActivityEnum.POOP)

    def add_peeing(self):
        """Starts peeing session on the new row."""
        self._update_activity(ActivityEnum.PEE)


def main(argv):
    """ Main method."""
    del argv
    print('Running under Python {0[0]}.{0[1]}.{0[2]}'.format(sys.version_info),
          file=sys.stderr)
    editor = SpreadSheetEditor()
    editor.add_start_feeding()
    editor.add_end_feeding()
    editor.add_pooping()
    editor.add_peeing()


if __name__ == '__main__':
    app.run(main)
