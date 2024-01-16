import pika
from reports.adapters.api.app import App
from reports.adapters.broker.pub import Pub
from reports.adapters.database import repositories
from reports.application import services
from reports.application.transaction import context_db_app


class Repositories:
    reports = repositories.ReportsRepo(context=context_db_app)


class Broker:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()
    channel.queue_declare(queue='reports_for_generation', durable=True)
    pub = Pub(connection, channel)


class Services:
    reports = services.Reports(
        reports_repo=Repositories.reports,
        pub=Broker.pub,
    )


app = App()
app.create_routers_reports(
    reports=Services.reports,
)
