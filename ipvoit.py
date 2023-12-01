from yoomoney import Authorize

Authorize(
    client_id="6C70B17B73BED3A4481843977688686C981C6B25DDA2EF906DDB2698702309E8",
    redirect_uri="https://t.me/Sslovopatsanabot",
    scope=[
        "account-info",
        "operation-history",
        "operation-details",
        "incoming-transfers",
        "payment-p2p",
        "payment-shop",
    ]
)