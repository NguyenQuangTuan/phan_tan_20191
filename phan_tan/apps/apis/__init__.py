from flask import Blueprint
from phan_tan.common.api import UApi
from .kpis.views.kpis import KPIs


app_api = Blueprint('app_api', __name__)
app_apis = UApi(app_api)

app_apis.add_resource(KPIs, '/kpis')
