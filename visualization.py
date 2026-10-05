import csv
import matplotlib.pyplot as plt


def load_performance_results(filename):

    workers = []

    execution_times = []

    speedups = []

    efficiencies = []

    with open(
        filename,
        "r",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["Workers"] == "Sequential":
                continue

            workers.append(
                int(row["Workers"])
            )

            execution_times.append(
                float(row["Execution Time"])
            )

            speedups.append(
                float(row["Speedup"])
            )

            efficiencies.append(
                float(row["Efficiency"])
            )

    return (
        workers,
        execution_times,
        speedups,
        efficiencies
    )


def create_execution_time_graph(
    workers,
    execution_times
):

    plt.figure()

    plt.plot(
        workers,
        execution_times,
        marker="o"
    )

    plt.xlabel(
        "Number of Workers"
    )

    plt.ylabel(
        "Execution Time (seconds)"
    )

    plt.title(
        "Parallel Execution Time vs Number of Workers"
    )

    plt.xticks(workers)

    plt.grid(True)

    plt.savefig(
        "results/execution_time.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()


def create_speedup_graph(
    workers,
    speedups
):

    plt.figure()

    plt.plot(
        workers,
        speedups,
        marker="o"
    )

    plt.xlabel(
        "Number of Workers"
    )

    plt.ylabel(
        "Speedup"
    )

    plt.title(
        "Speedup vs Number of Workers"
    )

    plt.xticks(workers)

    plt.grid(True)

    plt.savefig(
        "results/speedup.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()


def create_efficiency_graph(
    workers,
    efficiencies
):

    plt.figure()

    plt.plot(
        workers,
        efficiencies,
        marker="o"
    )

    plt.xlabel(
        "Number of Workers"
    )

    plt.ylabel(
        "Parallel Efficiency (%)"
    )

    plt.title(
        "Parallel Efficiency vs Number of Workers"
    )

    plt.xticks(workers)

    plt.grid(True)

    plt.savefig(
        "results/parallel_efficiency.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()


if __name__ == "__main__":

    results_file = (
        "results/performance_results.csv"
    )

    (
        workers,
        execution_times,
        speedups,
        efficiencies
    ) = load_performance_results(
        results_file
    )

    print(
        "Generating performance graphs..."
    )

    create_execution_time_graph(
        workers,
        execution_times
    )

    create_speedup_graph(
        workers,
        speedups
    )

    create_efficiency_graph(
        workers,
        efficiencies
    )

    print(
        "\nGraphs generated successfully!"
    )

    print(
        "Saved in:"
    )

    print(
        "results/execution_time.png"
    )

    print(
        "results/speedup.png"
    )

    print(
        "results/parallel_efficiency.png"
    )