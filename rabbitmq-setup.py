import pika

VALID_CATEGORIES = {"basic", "security", "ai"}


def setup_version_update_topology(channel) -> None:
    channel.exchange_declare(
        exchange="version_updates",
        exchange_type="topic",
        durable=True,
    )

    # All-events exchange
    channel.exchange_declare(
        exchange="version_updates.all",
        exchange_type="fanout",
        durable=True,
    )
    channel.exchange_bind(
        destination="version_updates.all",
        source="version_updates",
        routing_key="version.#",
    )

    # Category exchanges
    for category in VALID_CATEGORIES:
        exchange_name = f"version_updates.{category}"
        routing_key = f"version.{category}"

        channel.exchange_declare(
            exchange=exchange_name,
            exchange_type="fanout",
            durable=True,
        )

        channel.exchange_bind(
            destination=exchange_name,
            source="version_updates",
            routing_key=routing_key,
        )


connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

setup_version_update_topology(channel)

connection.close()
