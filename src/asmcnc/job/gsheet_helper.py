from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file"]

dev_mode_credentials_path = 'credentials.json'
dev_mode_token_path = 'token.json'

prod_mode_credentials_path = 'asmcnc/job/credentials.json'
prod_mode_token_path = 'asmcnc/job/token.json'

credentials_path = prod_mode_credentials_path
token_path = prod_mode_token_path


def authorize():
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


creds = authorize()


def create(title):
    try:
        service = build('sheets', 'v4', credentials=creds)
        spreadsheet = {
            'properties': {
                'title': title
            }
        }

        spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                                    fields='spreadsheetId').execute()

        return spreadsheet.get('spreadsheetId')
    except HttpError as e:
        print(e)
        return e


def add_sheet(spreadsheet_id, title):
    try:
        service = build('sheets', 'v4', credentials=creds)

        requests = [
            {
                "addSheet": {
                    "properties": {
                        "title": title
                    }
                }
            }
        ]

        body = {
            'requests': requests
        }

        result = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body).execute()

        return result
    except HttpError as e:
        print(e)
        return e


def add_img_to_sheet(spreadsheet_id, url):
    try:
        service = build('sheets', 'v4', credentials=creds)

        values = [
            ['=image("' + url + '", 4, 480, 360)']
        ]

        body = {
            'values': values
        }

        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range="Feed Factor Profile!A1",
            valueInputOption="USER_ENTERED", body=body).execute()

        return result
    except HttpError as e:
        print(e)
        return e


def add_feed_multiplier_sweep(spreadsheet_id, sweep_values):
    try:
        service = build('sheets', 'v4', credentials=creds)

        body = {
            'values': sweep_values
        }

        result = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range="Parameters!Y1:Z",
                                                        valueInputOption="USER_ENTERED", body=body).execute()

        return result
    except HttpError as e:
        print(e)
        return e


def write_other_data_to_sheet(spreadsheet_id, spindle_v_main, spindle_target_watts, increase_bias,  decrease_bias, m_coefficient, c_coefficient,
                              increase_cap, decerease_cap, delay_between_feed_adjustments, outlier_amount, cap_for_feed_increase_during_z_movement):
    try:
        service = build('sheets', 'v4', credentials=creds)

        values = [
            ["Spindle Mains Voltage", spindle_v_main],
            ["Spindle Target Watts", spindle_target_watts],
            ["Bias for Feed Increase", increase_bias],
            ["Bias for Feed Decrease", decrease_bias],
            ["M Coefficient", m_coefficient],
            ["C Coefficient", c_coefficient],
            ["Cap for Feed Increase", increase_cap],
            ["Cap for Feed Decrease", decerease_cap],
            ["Delay Between Feed Adjustments", delay_between_feed_adjustments],
            ["Outlier Amount", outlier_amount],
            ["Cap for Feed-Up Change When Moving in Z", cap_for_feed_increase_during_z_movement]
        ]

        body = {
            'values': values
        }

        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range="Parameters!A1:G",
            valueInputOption="USER_ENTERED", body=body).execute()

        return result
    except HttpError as e:
        print(e)
        return e


def get_sheet_id(spreadsheet_id, old_name):
    try:
        service = build('sheets', 'v4', credentials=creds)

        spreadsheet = service.spreadsheets().get(
            spreadsheetId=spreadsheet_id).execute()

        for sheet in spreadsheet['sheets']:
            if sheet['properties']['title'] == old_name:
                return sheet['properties']['sheetId']
    except HttpError as e:
        print(e)
        return e


def rename_sheet(spreadsheet_id, old_name, new_name):
    try:
        service = build('sheets', 'v4', credentials=creds)

        requests = [
            {
                "updateSheetProperties": {
                    "properties": {
                        "sheetId": get_sheet_id(spreadsheet_id, old_name),
                        "title": new_name
                    },
                    "fields": "title"
                }
            }
        ]

        body = {
            'requests': requests
        }

        result = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body).execute()

        return result
    except HttpError as e:
        print(e)
        return e


def write_data_to_sheet(spreadsheet_id, data):
    try:
        service = build('sheets', 'v4', credentials=creds)

        values = data

        body = {
            'values': values
        }

        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range="Data!A1:Q",
            valueInputOption="USER_ENTERED", body=body).execute()

        return result
    except HttpError as e:
        print(e)
        return e


def create_time_chart(spreadsheet_id):
    sheet_id = get_sheet_id(spreadsheet_id, "Data")

    try:
        service = build('sheets', 'v4', credentials=creds)

        requests = [
            {
                "addChart": {
                    "chart": {
                        "spec": {
                            "title": "Spindle Load vs Time",
                            "basicChart": {
                                "chartType": "LINE",
                                "legendPosition": "BOTTOM_LEGEND",
                                "axis": [
                                    {
                                        "position": "BOTTOM_AXIS",
                                        "title": "Time"
                                    },
                                    {
                                        "position": "LEFT_AXIS",
                                        "title": "Spindle Load"
                                    }
                                ],
                                "domains": [
                                    {
                                        "domain": {
                                            "sourceRange": {
                                                "sources": [
                                                    {
                                                        "sheetId": sheet_id,
                                                        "startRowIndex": 1,
                                                        "endRowIndex": 100000000,
                                                        "startColumnIndex": 0,
                                                        "endColumnIndex": 1
                                                    }
                                                ]
                                            }
                                        }
                                    }
                                ],
                                "series": [
                                    {
                                        "series": {
                                            "sourceRange": {
                                                "sources": [
                                                    {
                                                        "sheetId": sheet_id,
                                                        "startRowIndex": 0,
                                                        "endRowIndex": 100000000,
                                                        "startColumnIndex": 11,
                                                        "endColumnIndex": 12
                                                    }
                                                ]
                                            }
                                        },
                                        "targetAxis": "LEFT_AXIS"
                                    },
                                    {
                                        "series": {
                                            "sourceRange": {
                                                "sources": [
                                                    {
                                                        "sheetId": sheet_id,
                                                        "startRowIndex": 0,
                                                        "endRowIndex": 100000000,
                                                        "startColumnIndex": 13,
                                                        "endColumnIndex": 14
                                                    }]
                                            }
                                        },
                                        "targetAxis": "LEFT_AXIS"
                                    },
                                    {
                                        "series": {
                                            "sourceRange": {
                                                "sources": [
                                                    {
                                                        "sheetId": sheet_id,
                                                        "startRowIndex": 0,
                                                        "endRowIndex": 100000000,
                                                        "startColumnIndex": 16,
                                                        "endColumnIndex": 17
                                                    }
                                                ]
                                            }
                                        },
                                        "targetAxis": "LEFT_AXIS"
                                    }
                                ],
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

        result = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body).execute()

        return result
    except HttpError as e:
        print(e)
        return e


def create_chart(spreadsheet_id):
    sheet_id = get_sheet_id(spreadsheet_id, "Parameters")

    try:
        service = build('sheets', 'v4', credentials=creds)

        requests = [
            {
                "addChart": {
                    "chart": {
                        "spec": {
                            "title": "Spindle Load vs Feed Multiplier",
                            "basicChart": {
                                "chartType": "LINE",
                                "legendPosition": "BOTTOM_LEGEND",
                                "axis": [
                                    {
                                        "position": "BOTTOM_AXIS",
                                        "title": "Spindle Load"
                                    },
                                    {
                                        "position": "LEFT_AXIS",
                                        "title": "Feed Multiplier"
                                    }
                                ],
                                "domains": [
                                    {
                                        "domain": {
                                            "sourceRange": {
                                                "sources": [
                                                    {
                                                        "sheetId": sheet_id,
                                                        "startRowIndex": 1,
                                                        "endRowIndex": 100000000,
                                                        "startColumnIndex": 24,
                                                        "endColumnIndex": 25
                                                    }
                                                ]
                                            }
                                        }
                                    }
                                ],
                                "series": [
                                    {
                                        "series": {
                                            "sourceRange": {
                                                "sources": [
                                                    {
                                                        "sheetId": sheet_id,
                                                        "startRowIndex": 1,
                                                        "endRowIndex": 100000000,
                                                        "startColumnIndex": 25,
                                                        "endColumnIndex": 26
                                                    }
                                                ]
                                            }
                                        },
                                        "targetAxis": "LEFT_AXIS"
                                    }
                                ]
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

        result = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body).execute()

        return result
    except HttpError as e:
        print(e)
        return e


def move_spreadsheet(spreadsheet_id, folder_id):
    try:
        service = build('drive', 'v3', credentials=creds)

        file_id = spreadsheet_id

        f = service.files().get(fileId=file_id,
                                fields='parents').execute()
        previous_parents = ",".join(f.get('parents'))

        f = service.files().update(fileId=file_id,
                                   addParents=folder_id,
                                   removeParents=previous_parents,
                                   fields='id, parents',
                                   supportsAllDrives=True).execute()

        return f
    except HttpError as e:
        print(e)
        return e
