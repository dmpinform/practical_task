from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from reports.adapters.api import controllers
from reports.application import services


class App(FastAPI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO: на проде заменить
        origins = ['*']

        self.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )

    def create_routers_reports(
        self,
        reports: services.Reports,
    ):
        routers = APIRouter(prefix='/api')

        person_control = controllers.Reports(
            report=reports,
        )
        routers.add_api_route(
            '/report/upload',
            endpoint=person_control.upload,
            methods=['GET'],
        )

        self.include_router(routers)
