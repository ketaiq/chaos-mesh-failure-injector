from app.failures.network.network_delay import NetworkDelayFailure


def main():
    network_delay_failure = NetworkDelayFailure(
        "34.132.63.119:31767",
        "network-delay-failure",
        "5m",
        device="eth0",
        latency="100ms",
    )
    network_delay_failure.submit()


if __name__ == "__main__":
    main()
