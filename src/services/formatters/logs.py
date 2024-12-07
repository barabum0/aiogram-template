from typing import TYPE_CHECKING, Union

from aiogram.enums import ReactionTypeType

if TYPE_CHECKING:
    from aiogram.types import (
        Chat,
        Location,
        ReactionTypeCustomEmoji,
        ReactionTypeEmoji,
        ReactionTypePaid,
        SharedUser,
        ShippingAddress,
        User,
    )


def chat_log(chat: Union["Chat", "User", "SharedUser", None]) -> str:
    if chat is None:
        return "<red>Unknown</red>"
    return f"<cyan>{((chat.first_name or '')+' '+(chat.last_name or '')).strip()}</cyan><blue>[{chat.id}]</blue>"


def reaction(reaction: Union["ReactionTypeEmoji", "ReactionTypeCustomEmoji", "ReactionTypePaid"]) -> str:
    match reaction.type:
        case ReactionTypeType.EMOJI:
            return reaction.emoji
        case ReactionTypeType.CUSTOM_EMOJI:
            return f"<magenta>{reaction.custom_emoji_id}</magenta><fg 127,127,127>(custom)</fg 127,127,127>"
        case ReactionTypeType.PAID:
            return "⭐<fg 127,127,127>(paid)</fg 127,127,127>"

    return "=)"


def location(location: "Location") -> str:
    l = f"<green>{location.latitude}' {location.longitude}'</green>"
    if location.horizontal_accuracy:
        l += f"<fg 127,127,127>(±{location.horizontal_accuracy})</fg 127,127,127>"
    if location.live_period:
        l += f"<fg 127,127,127>(live {location.live_period}s)</fg 127,127,127>"
    return l


def shipping_address(address: "ShippingAddress") -> str:
    return ", ".join(
        p
        for p in (address.country_code.upper(), address.state, address.city, address.street_line1, address.street_line2)
        if len(p) > 0
    )
