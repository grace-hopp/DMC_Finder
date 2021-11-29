import logging

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages

from .models import *
from bootstrap_modal_forms.forms import BSModalForm

logger = logging.getLogger(__name__)

