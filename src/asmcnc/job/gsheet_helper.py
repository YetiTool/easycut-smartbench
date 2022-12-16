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


def authorize():
    creds = None

    if os.path.exists(prod_mode_token_path):
        creds = Credentials.from_authorized_user_file(prod_mode_token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                prod_mode_credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(prod_mode_token_path, 'w') as token:
            token.write(creds.to_json())

    return creds


def create(title):
    creds = authorize()

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
    creds = authorize()

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
    creds = authorize()

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


def write_other_data_to_sheet(spreadsheet_id, spindle_v_main, spindle_target_watts, bias, m_coefficient, c_coefficient,
                              increase_cap, decerease_cap, delay_between_feed_adjustments, outlier_amount):
    creds = authorize()

    try:
        service = build('sheets', 'v4', credentials=creds)

        values = [
            ["Spindle Mains Voltage", spindle_v_main],
            ["Spindle Target Watts", spindle_target_watts],
            ["Bias for Feed Decrease", bias],
            ["M Coefficient", m_coefficient],
            ["C Coefficient", c_coefficient],
            ["Cap for Feed Increase", increase_cap],
            ["Cap for Feed Decrease", decerease_cap],
            ["Delay Between Feed Adjustments", delay_between_feed_adjustments],
            ["Outlier Amount", outlier_amount]
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
    creds = authorize()

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
    creds = authorize()

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
    creds = authorize()

    try:
        service = build('sheets', 'v4', credentials=creds)

        values = data

        body = {
            'values': values
        }

        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range="Data!A1:P",
            valueInputOption="USER_ENTERED", body=body).execute()

        return result
    except HttpError as e:
        print(e)
        return e


def create_time_chart(spreadsheet_id):
    creds = authorize()

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
                                                        "startRowIndex": 1,
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
                                                        "startRowIndex": 1,
                                                        "endRowIndex": 100000000,
                                                        "startColumnIndex": 12,
                                                        "endColumnIndex": 13
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
                                                        "startRowIndex": 1,
                                                        "endRowIndex": 100000000,
                                                        "startColumnIndex": 15,
                                                        "endColumnIndex": 16
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


def create_chart(spreadsheet_id):
    creds = authorize()

    sheet_id = get_sheet_id(spreadsheet_id, "Data")

    try:
        service = build('sheets', 'v4', credentials=creds)

        requests = [
            {
                "addChart": {
                    "chart": {
                        "spec": {
                            "title": "Spindle Load vs Calculated Feed Multiplier",
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
                                                        "startColumnIndex": 11,
                                                        "endColumnIndex": 12
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
                                                        "startColumnIndex": 12,
                                                        "endColumnIndex": 13
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
    creds = authorize()

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
