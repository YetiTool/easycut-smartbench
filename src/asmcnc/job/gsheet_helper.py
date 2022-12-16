from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

dev_mode_credentials_path = 'credentials.json'
dev_mode_token_path = 'token.json'

prod_mode_credentials_path = 'asmcnc/job/credentials.json'
prod_mode_token_path = 'asmcnc/job/token.json'


def authorize():
    creds = None

    if os.path.exists(dev_mode_token_path):
        creds = Credentials.from_authorized_user_file(dev_mode_token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                dev_mode_credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(dev_mode_token_path, 'w') as token:
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


def write_other_data_to_sheet(spreadsheet_id, spindle_v_main, spindle_target_watts, bias, m_coefficient, c_coefficient, increase_cap, decerease_cap):
    creds = authorize()

    try:
        service = build('sheets', 'v4', credentials=creds)

        values = [
            ["Spindle V Main", "Spindle Target Watts", "Bias", "M Coefficient", "C Coefficient", "Increase Cap", "Decrease Cap"],
            [spindle_v_main, spindle_target_watts, bias, m_coefficient, c_coefficient, increase_cap, decerease_cap]
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
            spreadsheetId=spreadsheet_id, range="Data!A1:M",
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
                                                        "startColumnIndex": 2,
                                                        "endColumnIndex": 3
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
                                                        "startColumnIndex": 0,
                                                        "endColumnIndex": 1
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
                                                        "startColumnIndex": 1,
                                                        "endColumnIndex": 2
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


def add_picture_to_sheet(spreadsheet_id, image):
    creds = authorize()

    sheet_id = get_sheet_id(spreadsheet_id, "Data")

    try:
        service = build('sheets', 'v4', credentials=creds)

        requests = [
            {
                "addImage": {
                    "url": image,
                    "anchorCell": {
                        "sheetId": sheet_id,
                        "rowIndex": 1,
                        "columnIndex": 3
                    },
                    "width": 500,
                    "height": 500
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

