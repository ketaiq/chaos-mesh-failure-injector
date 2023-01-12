from app.failures.network.network_delay import NetworkDelayFailure


def submit_linear_network_delay_failure(num: int, initial_delay: int, inc: int):
    address = "34.132.63.119:31767"
    duration = "3m"
    device = "eth0"
    workflow = []
    for i in range(num):
        latency = initial_delay + i * inc
        network_delay = NetworkDelayFailure(
            address,
            f"{latency}ms-network-delay",
            duration,
            device=device,
            latency=f"{latency}ms",
        )
        workflow.append(network_delay)

    for process in workflow:
        print(f"Submit process {process.name}")
        process.submit()


def main():
    submit_linear_network_delay_failure(5, 50, 50)


if __name__ == "__main__":
    main()
