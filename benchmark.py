import time

from analytics import (
    sequential_analysis,
    parallel_analysis
)


def measure_sequential(
    data,
    number_of_runs=3
):

    times = []

    result = None

    for i in range(number_of_runs):

        start_time = time.perf_counter()

        result = sequential_analysis(data)

        end_time = time.perf_counter()

        execution_time = (
            end_time - start_time
        )

        times.append(execution_time)

    average_time = (
        sum(times) / len(times)
    )

    return result, average_time


def measure_parallel(
    data,
    number_of_workers,
    number_of_runs=3
):

    times = []

    result = None

    for i in range(number_of_runs):

        start_time = time.perf_counter()

        result = parallel_analysis(
            data,
            number_of_workers
        )

        end_time = time.perf_counter()

        execution_time = (
            end_time - start_time
        )

        times.append(execution_time)

    average_time = (
        sum(times) / len(times)
    )

    return result, average_time


def calculate_speedup(
    sequential_time,
    parallel_time
):

    return (
        sequential_time / parallel_time
    )


def calculate_efficiency(
    speedup,
    number_of_workers
):

    return (
        speedup
        / number_of_workers
        * 100
    )