from api.types.handler import HealthCheck
from api.competitor.v1 import AvaiCompetitor, PrepCompetitor

routers = [
    (r"/", HealthCheck),
    (r"/api/v1/competitor/availability", AvaiCompetitor),
    (r"/api/v1/competitor/preparation", PrepCompetitor),
]