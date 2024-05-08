from typing import Optional, Literal

from pydantic import Field, BaseModel


class StatusRequest(BaseModel):
    txn_id: str = Field(description="Plisio transaction ID")
    ipn_type: Literal["invoice"] = Field(description="Type of IPN notification, always 'invoice'", default="invoice")
    merchant: str = Field(description="Merchant site name")
    merchant_id: str = Field(description="Merchant site ID")
    amount: str = Field(description="Received amount in the selected cryptocurrency")
    currency: str = Field(description="Selected cryptocurrency")
    order_number: str = Field(description="Merchant internal order number")
    order_name: str = Field(description="Merchant internal order name")
    confirmations: str = Field(description="Block confirmations number")
    status: Literal["new", "pending", "pending internal", "expired", "completed", "mismatch", "error", "cancelled"] = Field(
        description="Invoice status")
    source_currency: Optional[str] = Field(description="Source currency if stated")
    source_amount: Optional[str] = Field(description="Amount in the source currency if stated")
    source_rate: Optional[str] = Field(description="Source currency cryptocurrency exchange rate")
    comment: Optional[str] = Field(description="Plisio’s comments")
    verify_hash: str = Field(description="Hash to verify the 'POST' data signed with your SECRET_KEY")
    invoice_commission: Optional[str] = Field(description="Plisio commission")
    invoice_sum: Optional[str] = Field(
        description="Invoice amount minus Plisio commission if shop pays commission, or invoice amount if client pays commission")
    invoice_total_sum: Optional[str] = Field(
        description="Invoice amount if shop pays commission, or invoice amount plus Plisio commission if client pays commission")
