import csv
import random


def generate_sales_data(filename, number_of_records):

    categories = [
        "Electronics",
        "Food",
        "Clothing",
        "Books",
        "Sports"
    ]

    with open(filename, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Product",
            "Category",
            "Quantity",
            "Price"
        ])

        for i in range(number_of_records):

            product = f"Product_{i + 1}"

            category = random.choice(categories)

            quantity = random.randint(1, 20)

            price = round(
                random.uniform(5.00, 500.00),
                2
            )

            writer.writerow([
                product,
                category,
                quantity,
                price
            ])


if __name__ == "__main__":

    generate_sales_data(
        "sales_data.csv",
        1000000
    )

    print("Sales dataset generated successfully.")