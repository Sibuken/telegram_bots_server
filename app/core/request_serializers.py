from typing import Any, Optional
from pydantic import BaseModel


class UpdateSerializer(BaseModel):
    update_id: int
    message: Optional[Any] = None
    edited_message: Optional[Any] = None
    channel_post: Optional[Any] = None
    edited_channel_post: Optional[Any] = None
    inline_query: Optional[Any] = None
    chosen_inline_result: Optional[Any] = None
    callback_query: Optional[Any] = None
    shipping_query: Optional[Any] = None
    pre_checkout_query: Optional[Any] = None
    poll: Optional[Any] = None
    poll_answer: Optional[Any] = None
