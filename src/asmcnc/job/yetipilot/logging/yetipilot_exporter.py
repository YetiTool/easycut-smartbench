import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file"
]

MAX = 100000000
DRIVE_FOLDER_ID = "1FwSQqN98_T39rtHd522KlLOTwxfcygsV"

dev_mode_credentials_path = '../google/credentials.json'
dev_mode_token_path = '../google/token.json'

prod_mode_credentials_path = 'asmcnc/job/yetipilot/google/credentials.json'
prod_mode_token_path = 'asmcnc/job/yetipilot/google/token.json'

dev_mode = False

credentials_path = dev_mode_credentials_path if dev_mode else prod_mode_credentials_path
token_path = dev_mode_token_path if dev_mode else prod_mode_token_path


def get_series_format(sheet_id, start_row, end_row, start_column, end_column, target_axis, red=None, green=None, blue=None,
                      alpha=None):
    if alpha is None:
        return {
            "series": {
                "sourceRange": {
                    "sources": [
                        {
                            "sheetId": sheet_id,
                            "startRowIndex": start_row,
                            "endRowIndex": end_row,
                            "startColumnIndex": start_column,
                            "endColumnIndex": end_column
                        }
                    ]
                }
            },
            "target_axis": target_axis + "_AXIS"
        }
    else:
        return {
            "series": {
                "sourceRange": {
                    "sources": [
                        {
                            "sheetId": sheet_id,
                            "startRowIndex": start_row,
                            "endRowIndex": end_row,
                            "startColumnIndex": start_column,
                            "endColumnIndex": end_column
                        }
                    ]
                }
            },
            "target_axis": target_axis + "_AXIS",
            "color": {
                "red": red,
                "green": green,
                "blue": blue,
                "alpha": alpha
            }
        }


def get_domain_format(sheet_id, start_row, end_row, start_column, end_column):
    return {
        "domain": {
            "sourceRange": {
                "sources": [
                    {
                        "sheetId": sheet_id,
                        "startRowIndex": start_row,
                        "endRowIndex": end_row,
                        "startColumnIndex": start_column,
                        "endColumnIndex": end_column
                    }
                ]
            }
        }
    }


class AutoPilotExporter:
    spreadsheet_id = None

    def __init__(self, title):
        self.title = title
        self.creds = self.authorize()

    def authorize(self):
        credentials = None

        if os.path.exists(token_path):
            credentials = Credentials.from_authorized_user_file(token_path, SCOPES)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES)
                credentials = flow.run_local_server(port=0)

            with open(token_path, 'w') as token:
                token.write(credentials.to_json())

        return credentials

    def create_spreadsheet(self):
        service = build('sheets', 'v4', credentials=self.creds)

        spreadsheet = {
            'properties': {
                'title': self.title
            }
        }

        spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                                    fields='spreadsheetId').execute()

        self.spreadsheet_id = spreadsheet.get('spreadsheetId')

    def add_sheet(self, name):
        service = build('sheets', 'v4', credentials=self.creds)

        body = {
            "requests": [
                {
                    "addSheet": {
                        "properties": {
                            "title": name
                        }
                    }
                }
            ]
        }

        service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body=body
        ).execute()

    def move_spreadsheet_to_drive(self):
        service = build('drive', 'v3', credentials=self.creds)

        f = service.files().get(fileId=self.spreadsheet_id,
                                fields='parents',
                                supportsAllDrives=True).execute()
        previous_parents = ",".join(f.get('parents'))

        f = service.files().update(fileId=self.spreadsheet_id,
                                   addParents=DRIVE_FOLDER_ID,
                                   removeParents=previous_parents,
                                   fields='id, parents',
                                   supportsAllDrives=True).execute()

    def get_sheet_id(self, name):
        service = build('sheets', 'v4', credentials=self.creds)

        spreadsheet = service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()

        for sheet in spreadsheet.get('sheets'):
            if sheet.get('properties').get('title') == name:
                return sheet.get('properties').get('sheetId')

    def rename_sheet(self, new_name, sheet_id):
        service = build('sheets', 'v4', credentials=self.creds)

        body = {
            "requests": [
                {
                    "updateSheetProperties": {
                        "properties": {
                            "sheetId": sheet_id,
                            "title": new_name
                        },
                        "fields": "title"
                    }
                }
            ]
        }

        service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body=body
        ).execute()

    def add_chart(self, chart_title, bottom_axis_title, left_axis_title, domains, series, right_axis_title='',
                  left_axis_max=None, right_axis_max=None, left_axis_min=None, right_axis_min=None):
        service = build('sheets', 'v4', credentials=self.creds)

        requests = []

        if left_axis_max is None:
            requests = [
                {
                    "addChart": {
                        "chart": {
                            "spec": {
                                "title": chart_title,
                                "basicChart": {
                                    "chartType": "LINE",
                                    "legendPosition": "BOTTOM_LEGEND",
                                    "axis": [
                                        {
                                            "position": "BOTTOM_AXIS",
                                            "title": bottom_axis_title
                                        },
                                        {
                                            "position": "LEFT_AXIS",
                                            "title": left_axis_title,
                                        },
                                        {
                                            "position": "RIGHT_AXIS",
                                            "title": right_axis_title,
                                        }
                                    ],
                                    "domains": domains,
                                    "series": series,
                                    "headerCount": 1
                                }
                            },
                            "position": {
                                "newSheet": True
                            }
                        }
                    }
                }
            ]
        else:
            requests = [
                {
                    "addChart": {
                        "chart": {
                            "spec": {
                                "title": chart_title,
                                "basicChart": {
                                    "chartType": "LINE",
                                    "legendPosition": "BOTTOM_LEGEND",
                                    "axis": [
                                        {
                                            "position": "BOTTOM_AXIS",
                                            "title": bottom_axis_title
                                        },
                                        {
                                            "position": "LEFT_AXIS",
                                            "title": left_axis_title,
                                            "viewWindowOptions": {
                                                "viewWindowMax": left_axis_max,
                                                "viewWindowMin": left_axis_min
                                            }
                                        },
                                        {
                                            "position": "RIGHT_AXIS",
                                            "title": right_axis_title,
                                            "viewWindowOptions": {
                                                "viewWindowMax": right_axis_max,
                                                "viewWindowMin": right_axis_min
                                            }
                                        }
                                    ],
                                    "domains": domains,
                                    "series": series,
                                    "headerCount": 1
                                }
                            },
                            "position": {
                                "newSheet": True
                            }
                        }
                    }
                }
            ]

        body = {
            'requests': requests
        }

        service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body=body
        ).execute()

    def _write(self, rows, range, sheet_title):
        service = build('sheets', 'v4', credentials=self.creds)

        body = {
            'values': rows
        }

        service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=sheet_title + "!" + range,
            valueInputOption="RAW",
            body=body
        ).execute()

    def write_parameters(self, parameters):
        self._write(parameters, "A1:B", "Parameters")

    def write_data(self, data):
        self._write(data, "A1:ZZ", "Raw data")

    def write_feed_profile(self, feed_profile):
        self._write(feed_profile, "Y1:Z", "Parameters")

    def get_url(self):
        return "https://docs.google.com/spreadsheets/d/" + self.spreadsheet_id

    def create_data_chart(self, data_sheet_id):
        domain = [
            get_domain_format(data_sheet_id, 1, MAX, 0, 1)  # time
        ]

        series = [
            get_series_format(data_sheet_id, 0, MAX, 11, 12, "RIGHT", 0, 0, 1, 1),  # calculated load
            get_series_format(data_sheet_id, 0, MAX, 14, 15, "LEFT", 1, 0, 0, 1),  # raw multiplier
            get_series_format(data_sheet_id, 0, MAX, 17, 18, "LEFT", 0.98, 0.8, 0, 1),  # feed override %
            get_series_format(data_sheet_id, 0, MAX, 12, 13, "RIGHT", 0, 1, 0, 1),  # target load
        ]

        self.add_chart("Raw data", "Time", "Feed Values (%)", domain, series, right_axis_title="Load Values (W)",
                       right_axis_max=3000, left_axis_max=200, left_axis_min=0, right_axis_min=0)

    def create_boris_chart(self, data_sheet_id):
        domain = [
            get_domain_format(data_sheet_id, 1, MAX, 0, 1)
        ]

        series = [
            get_series_format(data_sheet_id, 0, MAX, 11, 12, "RIGHT"),  # calculated load
            get_series_format(data_sheet_id, 0, MAX, 13, 14, "LEFT"),  # raw multiplier
            get_series_format(data_sheet_id, 0, MAX, 16, 17, "LEFT"),
            get_series_format(data_sheet_id, 0, MAX, 17, 18, "LEFT"),
            get_series_format(data_sheet_id, 0, MAX, 18, 19, "LEFT"),
            get_series_format(data_sheet_id, 0, MAX, 19, 20, "LEFT"),
            get_series_format(data_sheet_id, 0, MAX, 20, 21, "LEFT"),
            get_series_format(data_sheet_id, 0, MAX, 21, 22, "LEFT"),
            get_series_format(data_sheet_id, 0, MAX, 22, 23, "LEFT"),
            get_series_format(data_sheet_id, 0, MAX, 23, 24, "LEFT"),
            get_series_format(data_sheet_id, 0, MAX, 12, 13, "RIGHT")
        ]

        self.add_chart("Raw data", "Time", "Feed Values (%)", domain, series, right_axis_title="Load Values (W)")

    def create_feed_chart(self, data_sheet_id):
        domain = [
            get_domain_format(data_sheet_id, 1, MAX, 0, 1)
        ]

        series = [
            get_series_format(data_sheet_id, 0, MAX, 14, 15, "RIGHT", 1, 0, 1, 1),  # actual feed
            get_series_format(data_sheet_id, 0, MAX, 12, 13, "LEFT", 0.98, 0.8, 0, 1)  # feed override %
        ]

        self.add_chart("Feed Rate vs Feed Override", "Time", "Feed Override (%)", domain, series, right_axis_title="Feed  Rate (mm/min)", left_axis_max=200, right_axis_max=8000, left_axis_min=0, right_axis_min=0)

    def create_sweep_chart(self, parameter_sheet_id):
        spindle_load_feed_multiplier_domain = get_domain_format(parameter_sheet_id, 0, 100000000, 24, 25)

        spindle_load_feed_multiplier_series = get_series_format(parameter_sheet_id, 0, 100000000, 25, 26, "LEFT", 0, 0, 0, 1)

        self.add_chart('Spindle Load vs Feed Multiplier', 'Spindle Load', 'Feed Multiplier',
                       [spindle_load_feed_multiplier_domain], [spindle_load_feed_multiplier_series],
                       left_axis_min=-40, left_axis_max=20)

    def freeze_first_row_and_first_column(self, sheet_id):
        service = build('sheets', 'v4', credentials=self.creds)

        requests = [
            {
                "updateSheetProperties": {
                    "properties": {
                        "sheetId": sheet_id,
                        "gridProperties": {
                            "frozenRowCount": 1,
                            "frozenColumnCount": 1
                        }
                    },
                    "fields": "gridProperties.frozenRowCount, gridProperties.frozenColumnCount"
                }
            }
        ]

        body = {
            'requests': requests
        }

        service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body=body
        ).execute()

    def write_test_data(self, data):
        self._write(data, "A1:ZZ", "Test Data")

    def write_chart_data(self, data):
        self._write(data, "A1:ZZ", "Chart Data")

    def create_test_chart(self, sheet_id):
        domain = [
            get_domain_format(sheet_id, 0, MAX, 0, 1)
        ]

        series = [
            get_series_format(sheet_id, 0, MAX, 8, 9, "RIGHT", 0, 0, 1, 1),
            get_series_format(sheet_id, 0, MAX, 15, 16, "LEFT", 1, 0, 0, 1),
            get_series_format(sheet_id, 0, MAX, 12, 13, "LEFT", 0.98, 0.8, 0, 1),
            get_series_format(sheet_id, 0, MAX, 9, 10, "RIGHT", 0, 1, 0, 1),
        ]

        self.add_chart("Test Chart", "Time", "Feed Values (%)", domain, series, right_axis_title="Load Values (W)",
                       right_axis_max=3000, left_axis_max=200, left_axis_min=-40, right_axis_min=0)

    def create_spindle_speed_chart(self, sheet_id):
        domain = [
            get_domain_format(sheet_id, 0, MAX, 0, 1)
        ]

        series = [
            get_series_format(sheet_id, 0, MAX, 16, 17, "RIGHT", 0, 0.6, 0.6, 1)
        ]

        self.add_chart("Spindle RPM Chart", "Time", "Feed Values (%)", domain, series, right_axis_title="Load Values (W)",
                       right_axis_max=26000, left_axis_max=200, left_axis_min=-40, right_axis_min=0)

    def create_test_boris_chart(self, sheet_id):
        domain = [
            get_domain_format(sheet_id, 0, 100000000, 0, 1)
        ]

        series = [
            get_series_format(sheet_id, 0, MAX, 8, 9, "RIGHT", 0, 0, 1, 1),
            get_series_format(sheet_id, 0, MAX, 15, 16, "LEFT", 1, 0, 0, 1),
            get_series_format(sheet_id, 0, MAX, 12, 13, "LEFT", 0.98, 0.8, 0, 1),
            get_series_format(sheet_id, 0, MAX, 9, 10, "RIGHT", 0, 1, 0, 1)
        ]

        for i in range(1, 7):
            series.append(get_series_format(sheet_id, 0, MAX, i, i+1, "LEFT"))

        self.add_chart("Motor Loads", "Time", "Feed Values (%)", domain, series, right_axis_title="Load Values (W)",
                       right_axis_max=3000, left_axis_max=200, left_axis_min=-40, right_axis_min=0)

    def set_column_colour(self, col, r=0.5, g=0.5, b=0.5):
        service = build('sheets', 'v4', credentials=self.creds)

        requests = [
            {
                "repeatCell": {
                    "range": {
                        "sheetId": self.get_sheet_id("Test Data"),
                        "startRowIndex": 0,
                        "endRowIndex": 100000000,
                        "startColumnIndex": col,
                        "endColumnIndex": col+1
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": {
                                "red": r,
                                "green": g,
                                "blue": b
                            }
                        }
                    },
                    "fields": "userEnteredFormat.backgroundColor"
                }
            }
        ]

        body = {
            'requests': requests
        }

        service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body=body
        ).execute()


def run(title, logger):
    exporter = AutoPilotExporter(title)
    exporter.create_spreadsheet()
    parameters_sheet_id = exporter.get_sheet_id("Sheet1")
    exporter.rename_sheet("Parameters", parameters_sheet_id)
    exporter.write_feed_profile(logger.get_sweep())
    exporter.create_sweep_chart(parameters_sheet_id)
    exporter.add_sheet("Test Data")
    test_data_sheet_id = exporter.get_sheet_id("Test Data")
    exporter.write_test_data(logger.get_data_for_test_data_sheet())
    exporter.add_sheet("Chart Data")
    chart_data_sheet_id = exporter.get_sheet_id("Chart Data")
    exporter.write_chart_data(logger.get_data_for_chart_data_sheet())
    exporter.create_test_chart(chart_data_sheet_id)
    exporter.create_test_boris_chart(chart_data_sheet_id)
    exporter.create_feed_chart(chart_data_sheet_id)
    exporter.create_spindle_speed_chart(chart_data_sheet_id)
    exporter.write_parameters(logger.get_parameters())
    exporter.freeze_first_row_and_first_column(test_data_sheet_id)
    exporter.freeze_first_row_and_first_column(chart_data_sheet_id)
    exporter.rename_sheet("Feed Multiplier", exporter.get_sheet_id("Chart1"))
    exporter.rename_sheet("Test Chart", exporter.get_sheet_id("Chart2"))
    exporter.rename_sheet("Motor Loads", exporter.get_sheet_id("Chart3"))
    exporter.rename_sheet("Feed Rate vs Override", exporter.get_sheet_id("Chart4"))
    exporter.rename_sheet("Spindle Chart", exporter.get_sheet_id("Chart5"))
    exporter.set_column_colour(8)
    exporter.set_column_colour(21)
    exporter.set_column_colour(27)
    exporter.set_column_colour(30)
    exporter.move_spreadsheet_to_drive()


# def run(title, logger):
#     exporter = AutoPilotExporter(title)
#     exporter.create_spreadsheet()
#     parameters_sheet_id = exporter.get_sheet_id('Sheet1')
#     exporter.rename_sheet('Parameters', parameters_sheet_id)
#     exporter.add_sheet('Raw data')
#     data_sheet_id = exporter.get_sheet_id('Raw data')
#     exporter.write_data(logger.get_data_for_sheet())
#     exporter.write_parameters(logger.get_parameters())
#     exporter.write_feed_profile(logger.get_sweep())
#     exporter.create_sweep_chart(parameters_sheet_id)
#     exporter.create_data_chart(data_sheet_id)
#     exporter.create_boris_chart(data_sheet_id)
#     exporter.create_feed_chart(data_sheet_id)
#     exporter.rename_sheet('Spindle Load vs Feed Multiplier', exporter.get_sheet_id('Chart1'))
#     exporter.rename_sheet('Spindle Load vs Time', exporter.get_sheet_id('Chart2'))
#     exporter.rename_sheet('Motor Loads', exporter.get_sheet_id('Chart3'))
#     exporter.rename_sheet('Feed Rate vs Feed Override', exporter.get_sheet_id('Chart4'))
#     exporter.freeze_first_row_and_first_column(data_sheet_id)
#     exporter.move_spreadsheet_to_drive()
