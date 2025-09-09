def get_commission_rate(provider):
    total_orders = provider.orders.filter(status="done").count()
    if total_orders < 10:
        return 0.20
    elif total_orders < 50:
        return 0.15
    return 0.10