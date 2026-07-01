# Telegram Message Editing Capabilities

This document summarizes the rules for editing messages via the Telegram
Bot API, focusing on the `editMessageMedia`, `editMessageCaption`, and
`editMessageText` methods.

---

## General Restrictions

- **Ownership**: A bot can only edit messages that **it sent itself**
  (except for channel posts where it has admin rights).
- **Time limit**: Messages sent by users (not the bot) that contain an
  inline keyboard can only be edited for **up to 48 hours** after sending.
- **New files**: When editing an **inline message** (sent via Inline Mode),
  you **cannot upload a new file**; you must use an existing `file_id` or
  a public URL.

---

## Media Groups (Albums)

A media group (album) is technically a **group of separate messages** that
are displayed together in the client. The `sendMediaGroup` method returns
a `tuple[Message, ...]` because each media item in the album is a separate
message with its own `message_id`.

When editing albums, the following rules apply:

- **Photo/Video album** → can only be edited into another Photo/Video album
- **Audio album** → can only be edited into another Audio album
- **Document album** → can only be edited into another Document album

**Important constraints:**

- You **cannot** change the type of an album (e.g., Photo album → Audio album)
- You **cannot** turn an album into a single media message
- You **cannot** turn a single media message into an album
- To edit an album, you must edit **each message** in the group individually,
  using its own `message_id`

---

## What Can Be Edited Into What?

The table below applies to **single‑media messages** (not albums).

| Original message type | Can be edited into |
|-----------------------|-------------------|
| **Text** | Text, Audio (1), Document (1), Photo (1), Video (1) |
| **Audio (1)** | Audio (1), Document (1), Photo (1), Video (1), Text |
| **Document (1)** | Document (1), Audio (1), Photo (1), Video (1), Text |
| **Photo (1)** | Photo (1), Video (1) |
| **Video (1)** | Video (1), Photo (1) |
| **Voice** | **Not editable** (only caption can be changed) |
| **VideoNote** | **Not editable** (only caption can be changed) |

> **Important**:
>
> - Single‑media messages allow **free type change** – you can turn an
>   audio into a photo, or a document into a video, etc.
> - This freedom does **not** apply to albums. Albums can only be edited
>   into another album of the **same** media type.
> - **Voice** and **VideoNote** cannot be replaced with any other media;
>   they only support caption editing.

---

## Editing Captions

- You can **edit the caption** of any media message (including albums)
  using `editMessageCaption`.
- You can **remove** the caption entirely by passing `None` or an empty
  string (`""`) as the new caption.
- Caption editing is independent of the media content; it does not affect
  the file.

---

## Summary of Allowed Operations

| Action | Supported |
|--------|-----------|
| Text → single media (1 item) | ✅ Yes |
| Single media → any other single media | ✅ Yes (except Voice/VideoNote) |
| Voice/VideoNote → other media | ❌ No |
| Album → album of same type | ✅ Yes |
| Album → different type | ❌ No |
| Album → single media | ❌ No |
| Single media → album | ❌ No |
| Edit caption of any media message | ✅ Yes |
| Remove caption | ✅ Yes (by passing `None` or empty string) |
| Edit each message in an album individually | ✅ Required |

---

## Notes for Implementation

- The Python Telegram Bot (PTB) library provides `edit_message_media`,
  `edit_message_caption`, and `edit_message_text`.
- When using `edit_message_media`, you must provide an `InputMedia`
  object (e.g., `InputMediaPhoto`, `InputMediaVideo`).
- PTB's `edit_message_media` will raise a `BadRequest` if the new media
  is not allowed for the original message type (the library will forward
  the API error).
- Always handle exceptions like `MessageNotModified` (when the content is
  identical) gracefully.

---

## Official Documentation

Always refer to the official Telegram Bot API documentation for the
latest updates:
<https://core.telegram.org/bots/api>
