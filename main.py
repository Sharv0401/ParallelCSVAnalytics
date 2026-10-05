import csv
import os

from analytics import calculate_average_price

from benchmark import (
    measure_sequential,
    measure_parallel,
    calculate_speedup,
    calculate_efficiency
)


def load_csv(filename):

    data = []

    with open(
        filename,
        "r",
        newline=""
    ) as file:

        reader = csv.reader(file)

        next(reader)

        for row in reader:
            data.append(row)

    return data


def display_results(title, result):

    print("\n" + "=" * 40)

    print(title)

    print("=" * 40)

    print(
        "Total Records:",
        result["record_count"]
    )

    print(
        "Total Quantity:",
        result["total_quantity"]
    )

    print(
        "Total Revenue: RM",
        round(result["total_revenue"], 2)
    )

    print(
        "Total Discount: RM",
        round(result["total_discount"], 2)
    )

    print(
        "Total Tax: RM",
        round(result["total_tax"], 2)
    )

    print(
        "Total Profit: RM",
        round(result["total_profit"], 2)
    )

    print(
        "Average Price: RM",
        round(
            calculate_average_price(result),
            2
        )
    )

    print(
        "Minimum Price: RM",
        round(result["min_price"], 2)
    )

    print(
        "Maximum Price: RM",
        round(result["max_price"], 2)
    )

    print("\nCategory Counts:")

    for category, count in result["category_counts"].items():

        print(
            category + ":",
            count
        )


def verify_results(
    sequential_result,
    parallel_result
):

    if (

        sequential_result["record_count"]
        == parallel_result["record_count"]

        and sequential_result["total_quantity"]
        == parallel_result["total_quantity"]

        and round(
            sequential_result["total_revenue"],
            2
        )
        == round(
            parallel_result["total_revenue"],
            2
        )

        and round(
            sequential_result["total_discount"],
            2
        )
        == round(
            parallel_result["total_discount"],
            2
        )

        and round(
            sequential_result["total_tax"],
            2
        )
        == round(
            parallel_result["total_tax"],
            2
        )

        and round(
            sequential_result["total_profit"],
            2
        )
        == round(
            parallel_result["total_profit"],
            2
        )

        and round(
            calculate_average_price(
                sequential_result
            ),
            2
        )
        == round(
            calculate_average_price(
                parallel_result
            ),
            2
        )

        and round(
            sequential_result["min_price"],
            2
        )
        == round(
            parallel_result["min_price"],
            2
        )

        and round(
            sequential_result["max_price"],
            2
        )
        == round(
            parallel_result["max_price"],
            2
        )

        and sequential_result["category_counts"]
        == parallel_result["category_counts"]

    ):

        return True

    return False


def save_performance_results(
    filename,
    dataset_size,
    sequential_time,
    performance_results
):

    # Overwrite old benchmark results
    with open(
        filename,
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Dataset Size",
            "Workers",
            "Execution Time",
            "Speedup",
            "Efficiency"
        ])

        writer.writerow([
            dataset_size,
            "Sequential",
            round(sequential_time, 6),
            "1.00",
            "100.00"
        ])

        for result in performance_results:

            writer.writerow([
                dataset_size,
                result["workers"],
                round(result["time"], 6),
                round(result["speedup"], 2),
                round(result["efficiency"], 2)
            ])


if __name__ == "__main__":

    filename = "sales_data.csv"

    print("========================================")
    print("PARALLEL CSV DATA ANALYTICS TOOL")
    print("========================================")

    print("\nLoading CSV data...")

    data = load_csv(filename)

    dataset_size = len(data)

    print("Dataset loaded successfully.")

    print(
        "Records loaded:",
        dataset_size
    )

    # ======================================
    # SEQUENTIAL
    # ======================================

    print(
        "\nRunning sequential analysis..."
    )

    sequential_result, sequential_time = (
        measure_sequential(data)
    )

    display_results(
        "SEQUENTIAL RESULTS",
        sequential_result
    )

    print(
        "Average Sequential Execution Time:",
        round(sequential_time, 6),
        "seconds"
    )

    # ======================================
    # PARALLEL
    # ======================================

    worker_counts = [2, 4, 8]

    performance_results = []

    for number_of_workers in worker_counts:

        print(
            "\nRunning parallel analysis with",
            number_of_workers,
            "workers..."
        )

        parallel_result, parallel_time = (
            measure_parallel(
                data,
                number_of_workers
            )
        )

        display_results(
            "PARALLEL RESULTS (" +
            str(number_of_workers) +
            " WORKERS)",
            parallel_result
        )

        speedup = calculate_speedup(
            sequential_time,
            parallel_time
        )

        efficiency = calculate_efficiency(
            speedup,
            number_of_workers
        )

        print(
            "Average Parallel Execution Time:",
            round(parallel_time, 6),
            "seconds"
        )

        print(
            "Speedup:",
            round(speedup, 2),
            "x"
        )

        print(
            "Parallel Efficiency:",
            round(efficiency, 2),
            "%"
        )

        performance_results.append({
            "workers": number_of_workers,
            "time": parallel_time,
            "speedup": speedup,
            "efficiency": efficiency
        })

        if verify_results(
            sequential_result,
            parallel_result
        ):

            print(
                "Result Verification: MATCH"
            )

        else:

            print(
                "Result Verification: DO NOT MATCH"
            )

    # ======================================
    # PERFORMANCE SUMMARY
    # ======================================

    print("\n" + "=" * 60)

    print("PERFORMANCE SUMMARY")

    print("=" * 60)

    print(
        "\nDataset Size:",
        dataset_size,
        "records"
    )

    print("\nSequential:")

    print(
        "Average Execution Time:",
        round(sequential_time, 6),
        "seconds"
    )

    print("\nParallel:")

    print(
        "{:<10} {:<15} {:<15} {:<15}".format(
            "Workers",
            "Time (s)",
            "Speedup",
            "Efficiency"
        )
    )

    print("-" * 60)

    for result in performance_results:

        print(
            "{:<10} {:<15} {:<15} {:<15}".format(
                result["workers"],
                round(result["time"], 6),
                round(result["speedup"], 2),
                str(
                    round(
                        result["efficiency"],
                        2
                    )
                ) + "%"
            )
        )

    # ======================================
    # SAVE RESULTS
    # ======================================

    os.makedirs(
        "results",
        exist_ok=True
    )

    results_file = os.path.join(
        "results",
        "performance_results.csv"
    )

    save_performance_results(
        results_file,
        dataset_size,
        sequential_time,
        performance_results
    )

    print(
        "\nPerformance results saved to:"
    )

    print(results_file)

    print(
        "\nBenchmark completed successfully."
    )