Commands
========

Alot interprets user input as command line strings given via its prompt
or :ref:`bound to keys <key_bindings>` in the config.
Command lines are semi-colon separated command strings, each of which
starts with a command name and possibly followed by arguments.

.. warning:: a command in a sequence will be fired as soon as its
  predecessor returns control. As some commands use callbacks e.g.
  to read user input without blocking the interface, they will return
  control and hence trigger the next command even if they do not seem
  to have finished. ::

      compose; bnext

  is such a case.

See the sections below for which commands are available in which (UI) mode.
`global` commands are available independently of the mode.


:doc:`modes/global`
    globally available commands
:doc:`modes/search`
    commands available when showing thread search results
:doc:`modes/thread`
    commands available while displaying a thread
:doc:`modes/envelope`
    commands during message composition
:doc:`modes/bufferlist`
    commands while listing active buffers
:doc:`modes/taglist`
    commands while listing all tagstrings present in the notmuch database
