# swappable_models.py
from django.db import models
from django.db.models.signals import m2m_changed
from decimal import Decimal, ROUND_HALF_UP
from DistribuidoraCarne.validaciones import *
from simple_history.models import HistoricalRecords
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone  import now
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db import models

