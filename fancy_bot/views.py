import json
import logging

from django.http import JsonResponse
from django.views import View
from django.conf import settings

from .bot.dispatcher import process_telegram_event

logger = logging.getLogger(__name__)


def index(request):
    logger.info('Calling index')
    return JsonResponse({"ok": "OK"})


def ping(request):
    logger.info('Calling ping')
    return JsonResponse({"ping": "pong"})


class TelegramBotWebhookView(View):
    def post(self, request, *args, **kwargs):
        logger.info('Calling post')
        logger.info(f"TELEGRAM_URL: {settings.TELEGRAM_URL}")
        t_data = json.loads(request.body)
        logger.info(f'POST data: {t_data}')
        process_telegram_event(json.loads(request.body))
        return JsonResponse({"ok": "POST request processed"})
