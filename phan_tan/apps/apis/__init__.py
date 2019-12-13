from flask import Blueprint
from phan_tan.common.api import UApi
from .kpis.views.kpis import KPIs
from .kpis.views.all_kpis import AllKPIs
from .kpis.views.kpi import KPI
from .criterias.views.criterias import Criterias
from .departments.views.departments import Departments
from .departments.views.department import Department
from .kpi_results.views.kpi_results import KPIResults
from .kpi_results.views.all_kpi_results import AllKPIResults


app_api = Blueprint('app_api', __name__)
app_apis = UApi(app_api)

app_apis.add_resource(KPIs, '/kpis')
app_apis.add_resource(AllKPIs, '/kpis/all')
app_apis.add_resource(KPI, '/kpis/<id>')
app_apis.add_resource(KPIResults, '/kpi_results')
app_apis.add_resource(AllKPIResults, '/kpi_results/all')
app_apis.add_resource(Criterias, '/criterias')
app_apis.add_resource(Departments, '/departments')
app_apis.add_resource(Department, '/departments/<id>')
