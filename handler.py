import json

from bot import main as bot_main


def lambda_handler(event, context):
    bot_main()

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "success",
        }),
    }
