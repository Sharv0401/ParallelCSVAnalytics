from collections import Counter
import multiprocessing


def analyze_chunk(data):

    record_count = 0

    total_quantity = 0
    total_revenue = 0.0
    total_price = 0.0
    total_discount = 0.0
    total_tax = 0.0
    total_profit = 0.0

    min_price = float("inf")
    max_price = float("-inf")

    category_counts = Counter()

    for row in data:

        category = row[1]
        quantity = int(row[2])
        price = float(row[3])

        revenue = quantity * price

        if revenue >= 1000:
            discount_rate = 0.10

        elif revenue >= 500:
            discount_rate = 0.05

        else:
            discount_rate = 0.02

        discount = revenue * discount_rate

        taxable_amount = revenue - discount

        tax = taxable_amount * 0.06

        final_amount = taxable_amount + tax

        cost = revenue * 0.70

        profit = final_amount - cost

        record_count += 1
        total_quantity += quantity
        total_revenue += revenue
        total_price += price
        total_discount += discount
        total_tax += tax
        total_profit += profit

        if price < min_price:
            min_price = price

        if price > max_price:
            max_price = price

        category_counts[category] += 1

    return {
        "record_count": record_count,
        "total_quantity": total_quantity,
        "total_revenue": total_revenue,
        "total_price": total_price,
        "total_discount": total_discount,
        "total_tax": total_tax,
        "total_profit": total_profit,
        "min_price": min_price,
        "max_price": max_price,
        "category_counts": category_counts
    }


def sequential_analysis(data):

    return analyze_chunk(data)


def combine_results(results):

    combined = {
        "record_count": 0,
        "total_quantity": 0,
        "total_revenue": 0.0,
        "total_price": 0.0,
        "total_discount": 0.0,
        "total_tax": 0.0,
        "total_profit": 0.0,
        "min_price": float("inf"),
        "max_price": float("-inf"),
        "category_counts": Counter()
    }

    for result in results:

        combined["record_count"] += result["record_count"]

        combined["total_quantity"] += result["total_quantity"]

        combined["total_revenue"] += result["total_revenue"]

        combined["total_price"] += result["total_price"]

        combined["total_discount"] += result["total_discount"]

        combined["total_tax"] += result["total_tax"]

        combined["total_profit"] += result["total_profit"]

        if result["min_price"] < combined["min_price"]:
            combined["min_price"] = result["min_price"]

        if result["max_price"] > combined["max_price"]:
            combined["max_price"] = result["max_price"]

        combined["category_counts"].update(
            result["category_counts"]
        )

    return combined


def parallel_analysis(data, number_of_workers):

    chunk_size = len(data) // number_of_workers

    chunks = []

    for i in range(number_of_workers):

        start = i * chunk_size

        if i == number_of_workers - 1:
            end = len(data)

        else:
            end = start + chunk_size

        chunks.append(
            data[start:end]
        )

    with multiprocessing.Pool(
        number_of_workers
    ) as pool:

        results = pool.map(
            analyze_chunk,
            chunks
        )

    return combine_results(results)


def calculate_average_price(result):

    if result["record_count"] == 0:
        return 0

    return (
        result["total_price"]
        / result["record_count"]
    )