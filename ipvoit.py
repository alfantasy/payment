from yoomoney import Authorize

Authorize(
    client_id="85A5A958FDA36EAF6C598D6DA29CD06B77D610B5ECE434B457FE0C1B0ECFB9B2",
    redirect_uri="https://t.me/examplepayment_bot",
    scope=[
        "account-info",
        "operation-history",
        "operation-details",
        "incoming-transfers",
        "payment-p2p",
        "payment-shop",
    ]
)