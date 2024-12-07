from typing import TYPE_CHECKING, Union

from aiogram.enums import ContentType, ReactionTypeType

if TYPE_CHECKING:
    from aiogram.types import (
        Chat,
        Location,
        Message,
        ReactionTypeCustomEmoji,
        ReactionTypeEmoji,
        ReactionTypePaid,
        SharedUser,
        ShippingAddress,
        User,
    )


message_format_dict = {"<": r"\<", "\n": "<light-yellow>\\n</light-yellow>"}
message_format_translate = str.maketrans(message_format_dict)


def chat_log(chat: Union["Chat", "User", "SharedUser", None]) -> str:
    if chat is None:
        return "<red>Unknown</red>"

    from aiogram.types import SharedUser

    t = f"<cyan>{((chat.first_name or '') + ' ' + (chat.last_name or '')).strip()}</cyan>"
    if isinstance(chat, SharedUser):
        return t + f"<blue>[{chat.user_id}]</blue>"
    else:
        return t + f"<blue>[{chat.id}]</blue>"


def reaction(reaction: Union["ReactionTypeEmoji", "ReactionTypeCustomEmoji", "ReactionTypePaid"]) -> str:
    match reaction.type:
        case ReactionTypeType.EMOJI:
            return reaction.emoji  # type: ignore
        case ReactionTypeType.CUSTOM_EMOJI:
            return f"<magenta>{reaction.custom_emoji_id}</magenta><fg 127,127,127>(custom)</fg 127,127,127>"  # type: ignore
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


def message_content(message: "Message") -> str:
    log_message = chat_log(message.from_user)

    match message.content_type:
        case ContentType.TEXT if message.text:
            message_text = message.text.translate(message_format_translate)
            log_message += f" - <yellow>{message_text}</yellow>"
        case ContentType.AUDIO if message.audio:
            log_message += f" - <green>🎶 {message.audio.title.translate(message_format_translate) if message.audio.title is not None else "Audio"} by {message.audio.performer.translate(message_format_translate) if message.audio.performer is not None else "Unknown"}</green>"
        case ContentType.ANIMATION:
            log_message += " - <green>🤡 Animation</green>"
        case ContentType.DOCUMENT if message.document:
            log_message += f" - <green>📄 {message.document.file_name.translate(message_format_translate) if message.document.file_name is not None else "Document"}{f'<fg 127,127,127>({message.document.file_size} bytes)</fg 127,127,127>' if message.document.file_size else ''}</green>"
        case ContentType.GAME if message.game:
            log_message += f" - <green>🎮 {message.game.title.translate(message_format_translate)}</green> - <blue>{message.game.description.translate(message_format_translate)}</blue>"
            if message.game.text:
                game_text = message.game.text.translate(message_format_translate)
                log_message += f"- <yellow>{game_text}</yellow>"
        case ContentType.PHOTO:
            log_message += " - <green>🖼️ Photos</green>"
        case ContentType.STICKER if message.sticker:
            log_message += f" - <magenta>💌 Sticker{f'<fg 127>[{message.sticker.set_name}]</fg 127>' if message.sticker.set_name else ''}{f'<fg 127>({message.sticker.emoji})</fg 127>' if message.sticker.emoji else ''}</magenta>"
        case ContentType.STORY if message.story:
            log_message += f" forwarded a story from {chat_log(message.story.chat)}"
        case ContentType.VIDEO if message.video:
            log_message += f" - <green>📺 {message.video.file_name.translate(message_format_translate) if message.video.file_name is not None else "Video"}{f'<fg 127,127,127>({message.video.file_size} bytes)</fg 127,127,127>' if message.video.file_size else ''}</green>"
        case ContentType.VIDEO_NOTE:
            log_message += " - <green>⚪ Video note</green>"
        case ContentType.VOICE:
            log_message += " - <green>🔊 Voice message</green>"
        case ContentType.CONTACT if message.contact:
            log_message += f" sent <cyan>{f'{message.contact.first_name} {message.contact.last_name}'.strip()}</cyan>{f'<blue>[{message.contact.user_id}]</blue>' if message.contact.user_id else ''} contact with phone <red>{message.contact.phone_number}<red>"
        case ContentType.DICE if message.dice:
            log_message += f" - <magenta>{message.dice.emoji} Dice - {message.dice.value}<magenta>"
        case ContentType.POLL if message.poll:
            log_message += f" sent a poll <red>{message.poll.question}</red><light-red>[{message.poll.id}]</light-red> with options <yellow>[{', '.join(o.text for o in message.poll.options)}]</yellow>"
        case ContentType.VENUE if message.venue:
            log_message += f" - 📍 Venue <green>{message.venue.address}</green> - {location(message.venue.location)}"
        case ContentType.LOCATION if message.location:
            log_message += f" - 🗺️ Location {location(message.location)}"
        case ContentType.NEW_CHAT_MEMBERS if message.new_chat_members and message.from_user:
            if message.from_user.id == message.new_chat_members[0].id:
                log_message += " joined"
            else:
                log_message += f" added [{', '.join(chat_log(u) for u in message.new_chat_members)}]"
        case ContentType.LEFT_CHAT_MEMBER if message.left_chat_member and message.from_user:
            if message.from_user.id == message.left_chat_member.id:
                log_message += " left"
            else:
                log_message += f" kicked {chat_log(message.left_chat_member)} from"
        case ContentType.NEW_CHAT_TITLE if message.new_chat_title:
            log_message += f" changed title to <green>{message.new_chat_title}</green>"
        case ContentType.NEW_CHAT_PHOTO:
            log_message += " changed chat photo"
        case ContentType.DELETE_CHAT_PHOTO:
            log_message += " deleted chat photo"
        case ContentType.GROUP_CHAT_CREATED:
            log_message += " created group chat"
        case ContentType.SUPERGROUP_CHAT_CREATED:
            log_message += " created supergroup chat"
        case ContentType.CHANNEL_CHAT_CREATED:
            log_message += " created channel chat"
        case ContentType.MESSAGE_AUTO_DELETE_TIMER_CHANGED if message.message_auto_delete_timer_changed:
            log_message += f" changed message auto delete timer to {message.message_auto_delete_timer_changed.message_auto_delete_time} seconds"
        case ContentType.MIGRATE_TO_CHAT_ID if message.migrate_to_chat_id:
            log_message += f" migrated to chat {message.migrate_to_chat_id}"
        case ContentType.MIGRATE_FROM_CHAT_ID if message.migrate_from_chat_id:
            log_message += f" migrated from chat {message.migrate_from_chat_id}"
        case ContentType.PINNED_MESSAGE:
            log_message += " pinned message"
        case ContentType.INVOICE if message.invoice:
            log_message += f" sent invoice for <red>{message.invoice.title}</red> <green>{message.invoice.total_amount}<fg 127,127,127>(smallest unit)</fg 127,127,127> {message.invoice.currency.upper()}</green>"
        case ContentType.SUCCESSFUL_PAYMENT if message.successful_payment:
            log_message += f" sent payment for <green>{message.successful_payment.total_amount}<fg 127,127,127>(smallest unit)</fg 127,127,127> {message.successful_payment.currency.upper()}</green>"
        case ContentType.REFUNDED_PAYMENT if message.refunded_payment:
            log_message += f" refunded payment for <green>{message.refunded_payment.total_amount}<fg 127,127,127>(smallest unit)</fg 127,127,127> {message.refunded_payment.currency.upper()}</green>"
        case ContentType.USERS_SHARED if message.users_shared:
            log_message += f" shared {', '.join(chat_log(u) for u in message.users_shared.users)}"
        case ContentType.CHAT_SHARED if message.chat_shared:
            log_message += f" shared chat <cyan>{message.chat_shared.title or "Chat"}</cyan><blue>{message.chat_shared.chat_id}</blue>"
        case ContentType.CHAT_BACKGROUND_SET:
            log_message += " set chat background"
        case ContentType.FORUM_TOPIC_CREATED if message.forum_topic_created:
            log_message += f" created forum topic <red>{message.forum_topic_created.name}</red>"
        case ContentType.FORUM_TOPIC_CLOSED:
            log_message += " closed forum topic"
        case ContentType.FORUM_TOPIC_EDITED:
            log_message += " edited forum topic"
        case ContentType.FORUM_TOPIC_REOPENED:
            log_message += " reopened forum topic"
        case ContentType.GENERAL_FORUM_TOPIC_HIDDEN:
            log_message += " hidden forum topic"
        case ContentType.GENERAL_FORUM_TOPIC_UNHIDDEN:
            log_message += " unhidden forum topic"
        case _:
            log_message += f" sent a message with type <cyan>{message.content_type}</cyan>"

    if message.caption:
        caption_text = message.caption.translate(message_format_translate)
        log_message += f" - <yellow>{caption_text}</yellow>"

    return log_message
