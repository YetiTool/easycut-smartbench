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

dev_mode_credentials_path = 'google/credentials.json'
dev_mode_token_path = 'google/token.json'

prod_mode_credentials_path = 'asmcnc/job/yetipilot/google/credentials.json'
prod_mode_token_path = 'asmcnc/job/yetipilot/google/token.json'

credentials_path = prod_mode_credentials_path
token_path = prod_mode_token_path


def get_series_format(sheet_id, start_row, end_row, start_column, end_column, target_axis):
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
                  left_axis_max=200, right_axis_max=3000):
        service = build('sheets', 'v4', credentials=self.creds)

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
                                            "viewWindowMax": left_axis_max
                                        }
                                    },
                                    {
                                        "position": "RIGHT_AXIS",
                                        "title": right_axis_title,
                                        "viewWindowOptions": {
                                            "viewWindowMax": right_axis_max
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
            get_domain_format(data_sheet_id, 1, 100000000, 0, 1)
        ]

        series = [
            get_series_format(data_sheet_id, 0, 100000000, 11, 12, "RIGHT"),
            get_series_format(data_sheet_id, 0, 100000000, 13, 14, "LEFT"),
            get_series_format(data_sheet_id, 0, 100000000, 17, 18, "LEFT"),
            get_series_format(data_sheet_id, 0, 100000000, 12, 13, "RIGHT")
        ]

        self.add_chart("Raw data", "Time", "Feed Values (%)", domain, series, right_axis_title="Load Values (W)")

    def create_boris_chart(self, data_sheet_id):
        domain = [
            get_domain_format(data_sheet_id, 1, 100000000, 0, 1)
        ]

        series = [
            get_series_format(data_sheet_id, 0, 100000000, 11, 12, "RIGHT"),
            get_series_format(data_sheet_id, 0, 100000000, 13, 14, "LEFT"),
            get_series_format(data_sheet_id, 0, 100000000, 16, 17, "LEFT"),
            get_series_format(data_sheet_id, 0, 100000000, 17, 18, "LEFT"),
            get_series_format(data_sheet_id, 0, 100000000, 18, 19, "LEFT"),
            get_series_format(data_sheet_id, 0, 100000000, 19, 20, "LEFT"),
            get_series_format(data_sheet_id, 0, 100000000, 20, 21, "LEFT"),
            get_series_format(data_sheet_id, 0, 100000000, 21, 22, "LEFT"),
            get_series_format(data_sheet_id, 0, 100000000, 22, 23, "LEFT"),
            get_series_format(data_sheet_id, 0, 100000000, 23, 24, "LEFT"),
            get_series_format(data_sheet_id, 0, 100000000, 12, 13, "RIGHT")
        ]

        self.add_chart("Raw data", "Time", "Feed Values (%)", domain, series, right_axis_title="Load Values (W)")

    def create_sweep_chart(self, parameter_sheet_id):
        spindle_load_feed_multiplier_domain = get_domain_format(parameter_sheet_id, 0, 100000000, 24, 25)

        spindle_load_feed_multiplier_series = get_series_format(parameter_sheet_id, 0, 100000000, 25, 26, "LEFT")

        self.add_chart('Spindle Load vs Feed Multiplier', 'Spindle Load', 'Feed Multiplier',
                       [spindle_load_feed_multiplier_domain], [spindle_load_feed_multiplier_series])


def run(title, logger):
    exporter = AutoPilotExporter(title)
    exporter.create_spreadsheet()
    parameters_sheet_id = exporter.get_sheet_id('Sheet1')
    exporter.rename_sheet('Parameters', parameters_sheet_id)
    exporter.add_sheet('Raw data')
    data_sheet_id = exporter.get_sheet_id('Raw data')
    exporter.write_data(logger.get_data_for_sheet())
    exporter.write_parameters(logger.get_parameter_format())
    exporter.write_feed_profile(logger.get_sweep())
    exporter.create_sweep_chart(parameters_sheet_id)
    exporter.create_data_chart(data_sheet_id)
    exporter.create_boris_chart(data_sheet_id)
    exporter.rename_sheet('Spindle Load vs Feed Multiplier', exporter.get_sheet_id('Chart1'))
    exporter.rename_sheet('Spindle Load vs Time', exporter.get_sheet_id('Chart2'))
    exporter.rename_sheet('Motor Loads', exporter.get_sheet_id('Chart3'))
    exporter.move_spreadsheet_to_drive()
