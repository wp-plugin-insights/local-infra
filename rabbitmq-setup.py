import pika

VALID_CATEGORIES = {"basic", "security", "ai"}


def setup_version_update_topology(channel) -> None:
    # All-events exchange
    channel.exchange_declare(
        exchange="version_updates.all",
        exchange_type="fanout",
        durable=True,
    )

    # Category exchanges
    for category in VALID_CATEGORIES:
        exchange_name = f"version_updates.{category}"

        channel.exchange_declare(
            exchange=exchange_name,
            exchange_type="fanout",
            durable=True,
        )

    # Bind all category exchanges to the all-events exchange
    for category in VALID_CATEGORIES:
        channel.exchange_bind(
            destination=f"version_updates.{category}",
            source="version_updates.all",
        )


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

setup_version_update_topology(channel)

connection.close()