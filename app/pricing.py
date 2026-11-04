def cost(usage,price_in,price_out):
    input_tokens = usage.get("input_tokens", 0)
    output_tokens = usage.get("output_tokens", 0)

    input_cost = (
        input_tokens * price_in / 1_000_000
    )

    output_cost = (
        output_tokens * price_out / 1_000_000
    )

    return round(input_cost + output_cost, 8)