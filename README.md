# Warhound

Parse Battlerite telemetry files with ease.

(This library is in early development and doesn't contain any working code!)


## Introduction

The "telemetry" is a per-match file served over HTTP by Stunlock Studios. It
contains detailed events about what occurs in each round of a match--much more
detail than is exposed via the
[Battlerite API](https://developer.battlerite.com).

To get a match telemetry file, you will need a URL located in the "match
details" response body. You can interact with the API using a library like
[furrycorn](https://github.com/odeumgg/furrycorn).

Once you obtain the URL for the match telemetry, use this library to parse it.

More docs as and when the library develops.
