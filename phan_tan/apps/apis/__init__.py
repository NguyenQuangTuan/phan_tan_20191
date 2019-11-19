from flask import Blueprint
from phan_tan.common.api import UApi
from .kpis.views.kpis import KPIs
from .criterias.views.criterias import Criterias
from .departments.views.department import Departments
from .kpi_results.views.kpi_results import KPIResults


app_api = Blueprint('app_api', __name__)
app_apis = UApi(app_api)

app_apis.add_resource(KPIs, '/kpis')
app_apis.add_resource(KPIResults, '/kpi_results')
app_apis.add_resource(Criterias, '/criterias')
app_apis.add_resource(Departments, '/departments')
