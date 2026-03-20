import pika

VALID_CATEGORIES = {"basic", "security", "ai"}


def setup_version_update_topology(channel) -> None:
    # All-events exchange
    channel.exchange_declare(
        exchange="plugin.analysis.all",
        exchange_type="fanout",
        durable=True,
    )

    # Reporting exchange
    channel.exchange_declare(
        exchange="plugin.analysis.reports",
        durable=True,
    )

    channel.queue_declare(
        queue="plugin.analysis.reports",
        durable=True,
    )

    channel.queue_bind(
        exchange="plugin.analysis.reports",
        queue="plugin.analysis.reports",
    )

    # Category exchanges
    for category in VALID_CATEGORIES:
        exchange_name = f"plugin.analysis.{category}"

        channel.exchange_declare(
            exchange=exchange_name,
            exchange_type="fanout",
            durable=True,
        )

    # Bind all category exchanges to the all-events exchange
    for category in VALID_CATEGORIES:
        channel.exchange_bind(
            destination=f"plugin.analysis.{category}",
            source="plugin.analysis.all",
        )


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

setup_version_update_topology(channel)

connection.close()