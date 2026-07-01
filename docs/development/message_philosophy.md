# Message Philosophy

## Main principle

In TgBotScreen, every visually separated message is Message.
It can be:

1) simple text message
2) media (1) message
3) media album of Photo or Video
4) media album of Audio
5) media album of Document
6) voice
7) video note

## Available Message Types

Thus, there are these types of messages:

1) SimpleMessage
2) PhotoMessage
3) VideoMessage
4) AudioMessage
5) DocumentMessage
6) PhotoVideoAlbumMessage
7) AudioAlbumMessage
8) DocumentAlbumMessage
9) VoiceMessage
10) VideoNoteMessage

## Every Message Type Transition Description

### Shortcuts

MediaMessage = PhotoMessage, VideoMessage, DocumentMessage, AudioMessage
Albums = PhotoVideoAlbumMessage, AudioAlbumMessage, DocumentAlbumMessage
Immutable = VoiceMessage, VideoNoteMessage

### Transitions

#### SimpleMessage

Goes into everything, except VoiceMessage, VideoNoteMessage

#### MediaMessage

Goes into MediaMessage

#### Albums

Goes into Self, can only change existing sub-messages or delete them.
Also can go into corresponding MediaMessages

#### Immutable

Doesn't go into anything
