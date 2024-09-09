def calculator(consumption: list, distributor_tax: float, tax_type: str) -> tuple:
    """
    Returns a tuple of floats containing annual savings, monthly savings, applied_discount, and coverage.
    """
    average_consumption = sum(consumption) / len(consumption)
    
    discount_rates = {
        "Residencial": [(10000, 0.18), (20000, 0.22), (float('inf'), 0.25)],
        "Comercial": [(10000, 0.16), (20000, 0.18), (float('inf'), 0.22)],
        "Industrial": [(10000, 0.12), (20000, 0.15), (float('inf'), 0.18)]
    }
    
    coverage_rates = [
        (10000, 0.90),
        (20000, 0.95),
        (float('inf'), 0.99)
    ]
    
    applied_discount = 0
    for limit, discount in discount_rates[tax_type]:
        if average_consumption <= limit:
            applied_discount = discount
            break

    coverage = 0
    for limit, cov in coverage_rates:
        if average_consumption <= limit:
            coverage = cov
            break

    
    total_annual_cost = average_consumption * 12 * distributor_tax

    annual_savings = total_annual_cost * applied_discount * coverage
    monthly_savings = annual_savings / 12

    return (
        round(annual_savings, 2),
        round(monthly_savings, 2),
        applied_discount,
        coverage,
    )

if __name__ == "__main__":
    print("Testing...")

    result = calculator([1518, 1071, 968], 0.95871974, "Industrial")
    print(f"Expected: (1473.19, 122.77, 0.12, 0.9), Got: {result}")
    assert result == (1473.19, 122.77, 0.12, 0.9)

    result = calculator([1000, 1054, 1100], 1.12307169, "Residencial")
    print(f"Expected: (2295.32, 191.28, 0.18, 0.9), Got: {result}")
    assert result == (2295.32, 191.28, 0.18, 0.9)

    result = calculator([973, 629, 726], 1.04820025, "Comercial")
    print(f"Expected: (1405.56, 117.13, 0.16, 0.9), Got: {result}")
    assert result == (1405.56, 117.13, 0.16, 0.9)

    result = calculator([15000, 14000, 16000], 0.95871974, "Industrial")
    print(f"Expected: (24591.16, 2049.26, 0.15, 0.95), Got: {result}")
    assert result == (24591.16, 2049.26, 0.15, 0.95)

    result = calculator([12000, 11000, 11400], 1.12307169, "Residencial")
    print(f"Expected: (32297.74, 2691.48, 0.22, 0.95), Got: {result}")
    assert result == (32297.74, 2691.48, 0.22, 0.95)

    result = calculator([17500, 16000, 16400], 1.04820025, "Comercial")
    print(f"Expected: (35776.75, 2981.40, 0.18, 0.95), Got: {result}")
    assert result == (35776.75, 2981.40, 0.18, 0.95)

    result = calculator([30000, 29000, 29500], 0.95871974, "Industrial")
    print(f"Expected: (60478.73, 5039.89, 0.18, 0.99), Got: {result}")
    assert result == (60478.73, 5039.89, 0.18, 0.99)

    result = calculator([22000, 21000, 21400], 1.12307169, "Residencial")
    print(f"Expected: (71602.56, 5966.88, 0.25, 0.99), Got: {result}")
    assert result == (71602.56, 5966.88, 0.25, 0.99)

    result = calculator([25500, 23000, 21400], 1.04820025, "Comercial")
    print(f"Expected: (63832.12, 5319.34, 0.22, 0.99), Got: {result}")
    assert result == (63832.12, 5319.34, 0.22, 0.99)

    print("Everything passed")
