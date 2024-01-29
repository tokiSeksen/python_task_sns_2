import json
import os
import pymysql
import logging


class ResourceTable:
    TABLE_NAME = "resources"


def connect_database():
    return pymysql.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', ''),
        database=os.environ.get('DB_NAME', ''),
        port=int(os.environ.get('DB_PORT', 3306))
    )


def add_limits_data(cursor, user_data, limits_data):
    sql = f"INSERT INTO {ResourceTable.TABLE_NAME} " \
          f"(user_id, domains_used, workspaces_used, links_used, clicks_used, reports_used, teammates_used, tags_used, scripts_used, apps_used) " \
          f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    cursor.execute(sql, (
        user_data.get('id'),
        limits_data.get('domains', {}).get('used', 0),
        limits_data.get('workspaces', {}).get('used', 0),
        limits_data.get('cycle', {}).get('links-classic', {}).get('used', 0),
        limits_data.get('cycle', {}).get('clicks', {}).get('used', 0),
        limits_data.get('cycle', {}).get('reports', {}).get('used', 0),
        limits_data.get('cycle', {}).get('teammates', {}).get('used', 0),
        limits_data.get('tags', {}).get('used', 0),
        limits_data.get('scripts', {}).get('used', 0),
        limits_data.get('apps', {}).get('used', 0)
    ))


def lambda_handler(event):

    sns_message = json.loads(event['Records'][0]['Sns']['Message'])
    user_data = sns_message.get('data', {}).get('user', {}).get('public', {})
    limits_data = user_data.get('subscription', {}).get('limits', {})
    logging.info(f"Loading user data {user_data} and limits {limits_data} from sns message")

    try:
        with connect_database() as connection, connection.cursor() as cursor:
            add_limits_data(cursor, user_data, limits_data)
            connection.commit()
    except pymysql.Error as e:
        logging.error(f"Error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # For local testing, simulate an SNS event
    os.environ['DB_HOST'] = 'mysql'
    os.environ['DB_USER'] = 'root'
    os.environ['DB_PASSWORD'] = 'password'
    os.environ['DB_NAME'] = 'db'
    os.environ['DB_PORT'] = '3306'

    body = {
        "id": "9a3ac8477ce5430dbf12996e7e067850",
        "timestamp": "2024-01-23T00:02:20.148Z",
        "event": "cycle-renewed",
        "publisher": "api",
        "issuer": "api",
        "data": {
            "user": {
                "public": {
                    "id": "4c8ff5f4b64446dea5a74eb74a3e826b",
                    "createdAt": "2020-04-09T08:07:44.000Z",
                    "username": "armando+test10@rebrandly.com",
                    "email": "armando+test10@rebrandly.com",
                    "fullName": "armando+test10@rebrandly.com",
                    "avatarUrl": "https://s.gravatar.com/avatar/75fbf9db5fa154a6e97e85719df74124?size=80&d=retr o&rating=g",
                    "registration": {
                        "country": "it"
                    },
                    "integrations": [],
                    "subscription": {
                        "id": "34041057f71c47f99b154956609d51b0",
                        "version": 1,
                        "category": "enterprise",
                        "addonsEligible": False,
                        "createdAt": "2023-06-23T10:08:21.000Z",
                        "due": 8,
                        "billing": {
                            "cycle": {
                                "price": {
                                    "full": 7499,
                                    "net": 7499,
                                    "vat": 0
                                },
                                "expiresAt": "2024-06-23T10:08:21.000Z",
                                "recurrence": {
                                    "unit": "year",
                                    "units": 1
                                },
                                "resetsAt": "2024-01-23T10:08:21.000Z"
                            },
                            "addons": [],
                            "extra": {
                                "cycle": {}
                            }
                        },
                        "plan": {
                            "id": "440a262fbb4b40bdb56ff3dc1ec33235"
                        },
                        "external": {
                            "id": "None",
                            "line": "None"
                        },
                        "status": {
                            "renew": True,
                            "suspend": False
                        },
                        "sequence": {
                            "id": "4c8ff5f4b64446dea5a74eb74a3e826b",
                            "createdAt": "2022-10-20T09:50:34.000Z"
                        },
                        "limits": {
                            "domains": {
                                "used": 3,
                                "included": 20
                            },
                            "workspaces": {
                                "used": 1,
                                "included": 5
                            },
                            "cycle": {
                                "links-classic": {
                                    "used": 0,
                                    "included": 20000
                                },
                                "clicks": {
                                    "used": 0,
                                    "included": 2000000
                                },
                                "reports": {
                                    "used": 0,
                                    "included": 5
                                },
                                "teammates": {
                                    "used": 0,
                                    "included": 5
                                }
                            },
                            "tags": {
                                "used": 0,
                                "included": 1000
                            },
                            "scripts": {
                                "used": 0,
                                "included": 50
                            },
                            "apps": {
                                "used": 0,
                                "included": 50
                            }
                        }
                    },
                    "clicks": 0
                }
            }
        }
    }
    event = {
        'Records': [
            {'Sns': {'Message': json.dumps(body)}}
        ]
    }
    lambda_handler(event)
