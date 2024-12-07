from typing import Any, Awaitable, Callable, cast

from aiogram.enums import ContentType
from aiogram.types import (
    BusinessConnection,
    BusinessMessagesDeleted,
    CallbackQuery,
    ChatBoostRemoved,
    ChatBoostUpdated,
    ChatJoinRequest,
    ChatMemberUpdated,
    ChosenInlineResult,
    InlineQuery,
    Message,
    MessageReactionCountUpdated,
    MessageReactionUpdated,
    PaidMediaPurchased,
    Poll,
    PollAnswer,
    PreCheckoutQuery,
    ShippingQuery,
    Update,
)
from loguru import logger

from src.services.formatters.logs import chat_log, location, reaction, shipping_address

message_format_dict = {"<": r"\<", "\n": "<light-yellow>\\n</light-yellow>"}
message_format_translate = str.maketrans(message_format_dict)


async def logger_middleware(
    handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
    event: Update,
    data: dict[str, Any],
) -> Any:
    update_logger = logger.bind(update_type=event.event_type.upper().replace("_", " ")).opt(colors=True)

    match event.event_type:
        case (
            "message"
            | "business_message"
            | "edited_message"
            | "edited_business_message"
            | "edited_channel_post"
            | "channel_post"
        ):
            message: Message = cast(Message, event.event)

            log_message = chat_log(message.from_user)

            match message.content_type:
                case ContentType.TEXT:
                    message_text = message.text.translate(message_format_translate)
                    log_message += f" - <yellow>{message_text}</yellow>"
                case ContentType.AUDIO:
                    log_message += f" - <green>🎶 {message.audio.title.translate(message_format_translate) if message.audio.title is not None else "Audio"} by {message.audio.performer.translate(message_format_translate) if message.audio.performer is not None else "Unknown"}</green>"
                case ContentType.ANIMATION:
                    log_message += " - <green>🤡 Animation</green>"
                case ContentType.DOCUMENT:
                    log_message += f" - <green>📄 {message.document.file_name.translate(message_format_translate) if message.document.file_name is not None else "Document"}{f'<fg 127,127,127>({message.document.file_size} bytes)</fg 127,127,127>' if message.document.file_size else ''}</green>"
                case ContentType.GAME:
                    log_message += f" - <green>🎮 {message.game.title.translate(message_format_translate)}</green> - <blue>{message.game.description.translate(message_format_translate)}</blue>"
                    if message.game.text:
                        game_text = message.game.text.translate(message_format_translate)
                        log_message += f"- <yellow>{game_text}</yellow>"
                case ContentType.PHOTO:
                    log_message += " - <green>🖼️ Photos</green>"
                case ContentType.STICKER:
                    log_message += f" - <magenta>💌 Sticker{f'<fg 127>[{message.sticker.set_name}]</fg 127>' if message.sticker.set_name else ''}{f'<fg 127>({message.sticker.emoji})</fg 127>' if message.sticker.emoji else ''}</magenta>"
                case ContentType.STORY:
                    log_message += f" forwarded a story from {chat_log(message.story.chat)}"
                case ContentType.VIDEO:
                    log_message += f" - <green>📺 {message.video.file_name.translate(message_format_translate) if message.video.file_name is not None else "Video"}{f'<fg 127,127,127>({message.video.file_size} bytes)</fg 127,127,127>' if message.video.file_size else ''}</green>"
                case ContentType.VIDEO_NOTE:
                    log_message += " - <green>⚪ Video note</green>"
                case ContentType.VOICE:
                    log_message += " - <green>🔊 Voice message</green>"
                case ContentType.CONTACT:
                    log_message += f" sent <cyan>{f'{message.contact.first_name} {message.contact.last_name}'.strip()}</cyan>{f'<blue>[{message.contact.user_id}]</blue>' if message.contact.user_id else ''} contact with phone <red>{message.contact.phone_number}<red>"
                case ContentType.DICE:
                    log_message += f" - <magenta>{message.dice.emoji} Dice - {message.dice.value}<magenta>"
                case ContentType.POLL:
                    log_message += f" sent a poll <red>{message.poll.question}</red><light-red>[{message.poll.id}]</light-red> with options <yellow>[{', '.join(o.text for o in message.poll.options)}]</yellow>"
                case ContentType.VENUE:
                    log_message += (
                        f" - 📍 Venue <green>{message.venue.address}</green> - {location(message.venue.location)}"
                    )
                case ContentType.LOCATION:
                    log_message += f" - 🗺️ Location {location(message.location)}"
                case ContentType.NEW_CHAT_MEMBERS:
                    if message.from_user.id == message.new_chat_members[0].id:
                        log_message += " joined"
                    else:
                        log_message += f" added [{', '.join(chat_log(u) for u in message.new_chat_members)}]"
                case ContentType.LEFT_CHAT_MEMBER:
                    if message.from_user.id == message.left_chat_member.id:
                        log_message += " left"
                    else:
                        log_message += f" kicked {chat_log(message.left_chat_member)} from"
                case ContentType.NEW_CHAT_TITLE:
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
                case ContentType.MESSAGE_AUTO_DELETE_TIMER_CHANGED:
                    log_message += f" changed message auto delete timer to {message.message_auto_delete_timer_changed.message_auto_delete_time} seconds"
                case ContentType.MIGRATE_TO_CHAT_ID:
                    log_message += f" migrated to chat {chat_log(message.migrate_to_chat_id)}"
                case ContentType.MIGRATE_FROM_CHAT_ID:
                    log_message += f" migrated from chat {chat_log(message.migrate_from_chat_id)}"
                case ContentType.PINNED_MESSAGE:
                    log_message += " pinned message"
                case ContentType.INVOICE:
                    log_message += f" sent invoice for <red>{message.invoice.title}</red> <green>{message.invoice.total_amount}<fg 127,127,127>(smallest unit)</fg 127,127,127> {message.invoice.currency.upper()}</green>"
                case ContentType.SUCCESSFUL_PAYMENT:
                    log_message += f" sent payment for <green>{message.successful_payment.total_amount}<fg 127,127,127>(smallest unit)</fg 127,127,127> {message.successful_payment.currency.upper()}</green>"
                case ContentType.REFUNDED_PAYMENT:
                    log_message += f" refunded payment for <green>{message.refunded_payment.total_amount}<fg 127,127,127>(smallest unit)</fg 127,127,127> {message.refunded_payment.currency.upper()}</green>"
                case ContentType.USERS_SHARED:
                    log_message += f" shared {', '.join(chat_log(u) for u in message.users_shared)}"
                case ContentType.CHAT_SHARED:
                    log_message += f" shared chat <cyan>{message.chat_shared.title or "Chat"}</cyan><blue>{message.chat_shared.chat_id}</blue>"
                case ContentType.CHAT_BACKGROUND_SET:
                    log_message += " set chat background"
                case ContentType.FORUM_TOPIC_CREATED:
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

            if message.from_user is not None and message.from_user.id != message.chat.id:
                log_message += (
                    f" in {"channel" if "channel_post" in event.event_type else "chat"} {chat_log(message.chat)}"
                )

            if "edited" in event.event_type:
                log_message += " <fg 127,127,127>(edited)</fg 127,127,127>"

            if "business" in event.event_type:
                log_message += " <fg 127,127,127>(business)</fg 127,127,127>"
        case "business_connection":
            business_connection: BusinessConnection = cast(BusinessConnection, event.business_connection)

            log_message = f"Business mode was {'<green>enabled</green>' if business_connection.is_enabled else '<red>disabled</red>'}"
            if business_connection.is_enabled:
                log_message += f" {'<green>with</green>' if business_connection.can_reply else '<red>without</red>'} permission to reply"

            log_message += f" for {chat_log(business_connection.user)}"
        case "deleted_business_messages":
            deleted_business_messages: BusinessMessagesDeleted = cast(
                BusinessMessagesDeleted, event.deleted_business_messages
            )

            log_message = f"{len(deleted_business_messages.message_ids)} Message{'s' if len(deleted_business_messages.message_ids) > 1 else ''}<cyan>[{', '.join(str(i) for i in deleted_business_messages.message_ids)}]</cyan> were deleted in chat {chat_log(deleted_business_messages.chat)}"
        case "message_reaction":
            message_reaction_updated: MessageReactionUpdated = cast(MessageReactionUpdated, event.message_reaction)
            actor = message_reaction_updated.user or message_reaction_updated.actor_chat

            log_message = f"{chat_log(actor)}"
            if len(message_reaction_updated.old_reaction) > 0 and len(message_reaction_updated.new_reaction) > 0:
                log_message += f" changed reactions from [{', '.join(reaction(r) for r in message_reaction_updated.old_reaction)}] to ["
                log_message += ", ".join(reaction(r) for r in message_reaction_updated.new_reaction)
                log_message += "] on"
            elif len(message_reaction_updated.new_reaction) == 0:
                log_message += (
                    f" removed [{', '.join(reaction(r) for r in message_reaction_updated.old_reaction)}] reaction from"
                )
            else:
                log_message += " added ["
                log_message += ", ".join(reaction(r) for r in message_reaction_updated.new_reaction)
                log_message += "] reactions to"

            log_message += f" message <red>{message_reaction_updated.message_id}</red>"

            if actor.id != message_reaction_updated.chat.id:
                log_message += f" in chat {chat_log(message_reaction_updated.chat)}"
        case "message_reaction_count":
            message_reaction_count_updated: MessageReactionCountUpdated = cast(
                MessageReactionCountUpdated, event.message_reaction_count
            )

            log_message = f"Reactions were updated to [{', '.join(f"{str(r.type)}<fg 127,127,127>({r.total_count})</fg 127,127,127>" for r in message_reaction_count_updated.reactions)}]"
            log_message += f" on message <red>{message_reaction_count_updated.message_id}</red>"
            log_message += f" in chat {chat_log(message_reaction_count_updated.chat)}"
        case "inline_query":
            inline_query: InlineQuery = cast(InlineQuery, event.inline_query)

            query_text = inline_query.query.translate(message_format_translate)
            offset_text = inline_query.offset.translate(message_format_translate)

            log_message = f"{chat_log(inline_query.from_user)} - <yellow>{query_text}</yellow>"
            if inline_query.chat_type is not None:
                log_message += f" in <cyan>{inline_query.chat_type}</cyan>"
            if len(offset_text) > 0:
                log_message += f" with offset <yellow>{offset_text}</yellow>"
            if inline_query.location:
                log_message += f" located in {location(inline_query.location)}"
        case "chosen_inline_result":
            chosen_inline_result: ChosenInlineResult = cast(ChosenInlineResult, event.chosen_inline_result)

            query_text = chosen_inline_result.query.translate(message_format_translate)

            log_message = f"{chat_log(chosen_inline_result.from_user)} chosen <red>result</red><light-red>[{chosen_inline_result.result_id}]</light-red> for query <yellow>{query_text}</yellow>"
            if chosen_inline_result.inline_message_id:
                log_message += f" for message <red>{chosen_inline_result.inline_message_id}</red>"
            if chosen_inline_result.location:
                log_message += f" located in {location(chosen_inline_result.location)}"
        case "callback_query":
            callback_query: CallbackQuery = cast(CallbackQuery, event.callback_query)

            query_text = callback_query.data.translate(message_format_translate)

            log_message = f"{chat_log(callback_query.from_user)} - <yellow>{query_text}</yellow>"
            if callback_query.message is not None:
                message_text = callback_query.message.text.translate(message_format_translate)
                log_message += f" on message <yellow>{message_text}</yellow><fg #FF8C00>[{callback_query.message.message_id}]</fg #FF8C00>"
                if callback_query.from_user.id != callback_query.message.chat.id:
                    log_message += f" in chat {chat_log(callback_query.message.chat)}"
        case "shipping_query":
            shipping_query: ShippingQuery = cast(ShippingQuery, event.shipping_query)

            log_message = f"{chat_log(shipping_query.from_user)} ordered a shipping<red>[{shipping_query.invoice_payload}]</red> query<red>[{shipping_query.id}]</red> on address <green>{shipping_address(shipping_query.shipping_address)}</green>"

        case "pre_checkout_query":
            pre_checkout_query: PreCheckoutQuery = cast(PreCheckoutQuery, event.pre_checkout_query)

            log_message = f"{chat_log(pre_checkout_query.from_user)} placed a pre-checkout<red>[{pre_checkout_query.invoice_payload}]</red> query<red>[{pre_checkout_query.id}]</red> for <green>{pre_checkout_query.total_amount}<fg 127,127,127>(smallest unit)</fg 127,127,127> {pre_checkout_query.currency.upper()}</green>"

        case "purchased_paid_media":
            purchased_paid_media: PaidMediaPurchased = cast(PaidMediaPurchased, event.purchased_paid_media)

            log_message = f"{chat_log(purchased_paid_media.from_user)} purchased a media<red>[{purchased_paid_media.paid_media_payload}]</red>"
        case "poll":
            poll: Poll = cast(Poll, event.poll)

            log_message = f"<red>{poll.question}</red><light-red>[{poll.id}]</light-red> with options <yellow>[{', '.join(f"{o.text}<fg 127,127,127>({o.voter_count})</fg 127,127,127>" for o in poll.options)}]</yellow> and <green>{poll.total_voter_count}</green> voters"
            if poll.is_closed:
                log_message += " <red>is closed</red>"
        case "poll_answer":
            poll_answer: PollAnswer = cast(PollAnswer, event.poll_answer)

            voter = poll_answer.voter_chat or poll_answer.user

            log_message = f"{chat_log(voter)}" if voter else "<cyan>anonymous</cyan>"
            if poll_answer.option_ids:
                log_message += f"voted for <yellow>[{', '.join(str(o) for o in poll_answer.option_ids)}]</yellow>"
            else:
                log_message += "<red>retracted vote</red>"
            log_message += f" on poll <red>[{poll_answer.poll_id}]</red>"

        case "my_chat_member" | "chat_member":
            chat_member: ChatMemberUpdated = cast(ChatMemberUpdated, event.event)

            log_message = chat_log(chat_member.from_user)
            match chat_member.new_chat_member.status:
                case "kicked":
                    log_message += f" banned {chat_log(chat_member.new_chat_member.user)}"
                    if chat_member.new_chat_member.until_date.timestamp() == 0:
                        log_message += " <red>permanently</red>"
                    else:
                        log_message += f" <red>until {chat_member.new_chat_member.until_date.isoformat()}</red>"

                case "left":
                    log_message += f" left {chat_log(chat_member.new_chat_member.user)}"

                case _:
                    log_message += f" changed status to <yellow>{chat_member.new_chat_member.status}</yellow>"

            if chat_member.chat.id != chat_member.from_user.id:
                log_message += f" in chat {chat_log(chat_member.chat)}"

        case "chat_join_request":
            chat_join_request: ChatJoinRequest = cast(ChatJoinRequest, event.event)

            log_message = (
                f"{chat_log(chat_join_request.from_user)} requested to join {chat_log(chat_join_request.chat)}"
            )

        case "chat_boost":
            chat_boost: ChatBoostUpdated = cast(ChatBoostUpdated, event.chat_boost)

            log_message = f"{chat_log(chat_boost.chat)} was boosted"

        case "removed_chat_boost":
            removed_chat_boost: ChatBoostRemoved = cast(ChatBoostRemoved, event.removed_chat_boost)

            log_message = f"chat boost was removed from {chat_log(removed_chat_boost.chat)}"

        case _:
            log_message = f"Update with id {event.update_id}"

    update_logger.log("UPDATE", log_message)

    with update_logger.catch(message=f"Error while processing update with id {event.update_id}"):
        return await handler(event, data)
