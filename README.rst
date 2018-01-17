Warhound
========

Battlerite API telemetry parser.


Introduction
-----------


The "telemetry" is a per-match file served over HTTP by Stunlock Studios. It
contains detailed events about what occurs in each round of a match--much more
detail than is exposed via the `Battlerite API <https://developer.battlerite.com>`_.

To get a match telemetry file, you will need a URL located in the "match
details" response body. You can interact with the API using a library like
`furrycorn <https://github.com/odeumgg/furrycorn>`_.

Once you obtain the URL for the match telemetry, use this library to parse it.

The parsed result is a structured object model of telemetry data, rendering it
much easier to find the data you need.


Wiki
----

We're using the `wiki <https://github.com/odeumgg/warhound/wiki>`_ to document
warhound. Feel free to make contributions.


Installation
------------

``pip install warhound`` should do it for your projects.


Development
-----------

Requirement setup should be a breeze using `pipenv <https://docs.pipenv.org/>`_.

If you're using `nixos <https://nixos.org>`_, simply boot a ``nix-shell`` in the
project directory to get a development shell.

For the rest of the world:

1. Clone the directory and navigate to your local repo in a command line.
2. ``pipenv install --three``
3. ``pipenv shell``

For development, make sure ``PYTHONPATH`` includes the project root. Run tests
with ``py.test``.

Please submit changes by pull request on an *aptly named topic branch*.


Code Style
----------

The author of this library prefers a functional style of coding which centers
on "types". It's a lot easier to reason about types than logical steps, and
given the highly structured nature of jsonapi, it felt like a good fit.

Feel free to message with any questions you have. I'm happy to help and explain.


License
-------

This project is Copyright © 2018 odeum.gg and licensed under the MIT license.
View `the license <https://github.com/odeumgg/warhound/blob/master/LICENSE>`_
for details.

