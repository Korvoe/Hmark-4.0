.. _readtags(1):

==============================================================
readtags
==============================================================
--------------------------------------------------------------
Find tag file entries matching specified names
--------------------------------------------------------------
:Version: 0.0.0
:Manual group: Universal-ctags
:Manual section: 1

SYNOPSIS
--------
|	**readtags** -h | --help
|	**readtags** (-H | --help-expression) (filter|sorter)
|	**readtags** [OPTION]... ACTION

DESCRIPTION
-----------
The **readtags** program filters, sorts and prints tag entries in a tags file.
The basic filtering is done using **actions**, by which you can list all
regular tags, pseudo tags or regular tags matching specific name. Then, further
filtering and sorting can be done using **post processors**, namely **filter
expressions** and **sorter expressions**.

ACTIONS
-------
``-l``, ``--list``
	List regular tags.

``[-] NAME``
	List regular tags matching NAME.
	"-" as NAME indicates arguments after this as NAME even if they start with -.

``-D``, ``--list-pseudo-tags``
	Equivalent to ``--list-pseudo-tags``.

OPTIONS
-------

Controlling the Tags Reading Behavior
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The behavior of reading tags can be controlled using these options:

``-t TAGFILE``, ``--tag-file TAGFILE``
	Use specified tag file (default: "tags").

``-s[0|1|2]``, ``--override-sort-detection METHOD``
	Override sort detection of tag file.
	METHOD: unsorted|sorted|foldcase

The NAME action will perform binary search on sorted (including "foldcase")
tags files, which is much faster then on unsorted tags files.

Controlling the NAME Action Behavior
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The behavior of the NAME action can be controlled using these options:

``-i``, ``--icase-match``
	Perform case-insensitive matching in the NAME action.

``-p``, ``--prefix-match``
	Perform prefix matching in the NAME action.

Controlling the Output
~~~~~~~~~~~~~~~~~~~~~~
By default, the output of readtags contains only the name, input and pattern
field. The Output can be tweaked using these options:

``-d``, ``--debug``
	Turn on debugging output.

``-E``, ``--escape-output``
	Escape characters like tabs in output as described in :ref:`tags(5) <tags(5)>`.

``-e``, ``--extension-fields``
	Include extension fields in output.

``-n``, ``--line-number``
	Also include the line number field when ``-e`` option is give.

About the ``-E`` option: certain characters are escaped in a tags file, to make
it machine-readable. e.g., ensuring no tabs character appear in fields other
than the pattern field. By default, readtags translates them to make it
human-readable, but when utilizing readtags output in a script or a client
tool, ``-E`` option should be used. See :ref:`ctags-client-tools(7) <ctags-client-tools(7)>` for more
discussion on this.

Filtering and Sorting
~~~~~~~~~~~~~~~~~~~~~
Further filtering and sorting on the tags listed by actions are performed using:

``-Q EXP``, ``--filter EXP``
	Filter the tags listed by ACTION with EXP before printing.

``-S EXP``, ``--sorter EXP``
	Sort the tags listed by ACTION with EXP before printing.

These are discussed in the `EXPRESSION`_ section.

Examples
~~~~~~~~
* List all tags in "/path/to/tags":

  .. code-block:: console

     $ readtags -t /path/to/tags -l

* List all tags in "tags" that start with "mymethod":

  .. code-block:: console

     $ readtags -p - mymethod

* List all tags matching "mymethod", case insensitively:

  .. code-block:: console

     $ readtags -i - mymethod

* List all tags start with "myvar", and printing all fields (i.e., the whole line):

  .. code-block:: console

     $ readtags -p -ne - myvar

EXPRESSION
----------
Scheme-style expressions are used for the ``-Q`` and ``-S`` options. For those
who doesn't know Scheme or Lisp, just remember:

* A function call is wrapped in a pair of parenthesis. The first item in it is
  the function/operator name, the others are arguments.
* Function calls can be nested.

So, ``(+ 1 (+ 2 3))`` means add 2 and 3 first, then add the result with 1.

Filtering
~~~~~~~~~
The tag entries that makes the filter expression produces non-#f values are
filtered out (#f means false).

The basic operators for filtering are ``eq?``, ``prefix?``, ``suffix?``,
``substr?``, and ``#/PATTERN/``. Language common fields can be accessed using
variables starting with ``$``, e.g., ``$language`` represents the language field.
For example:

* List all tags start with "myfunc" in Python code files:

  .. code-block:: console

     $ readtags -p -Q '(eq? $language "Python")' - myfunc

``downcase`` or ``upcase`` operators can be used to perform case-insensitive
matching:

* List all tags containing "my", case insensitively:

    .. code-block:: console

     $ readtags -Q '(substr? (downcase $name) "my")' -l

We have logical operators like ``and``, ``or`` and ``not``. The value of a
missing field is #f, so we could deal with missing fields:

* List all tags containing "impl" in Python code files, but allow the
  ``language:`` field to be missing:

  .. code-block:: console

     $ readtags -Q '(and (substr? $name "impl")\
                         (or (eq? $language "Python")\
                             (not $language)))' -l

``#/PATTERN/`` is for the case when string predicates (``prefix?``, ``suffix``,
and ``substr?``) are not enough. You can use "Posix extended regular expression"
as PATTERN.

* List all tags inherits from the class "A":

  .. code-block:: console

     $ readtags -Q '(#/(^|, )A(,|$)/ $inherits)' -l

Here ``$inherits`` is a comma-separated class list like "A, B, C", "Z, A", "P, A,
Q", or just "A". The tags file may have tag entries that has no ``inherits:``
field. In that case ``$inherits`` is #f, and the regular expression matching
raises an error, since it works only for strings. To avoid this problem:

* Safely list all tags inherits from the class "A":

  .. code-block:: console

     $ readtags -Q '(and $inherits (#/(^|, )A(,|$)/ $inherits))' -l


Case-insensitive matching can be performed by ``#/PATTERN/i``.

* Safely list all tags inherits from the class "A" or "a":

  .. code-block:: console

     $ readtags -Q '(and $inherits (#/(^|, )A(,|$)/i $inherits))' -l

To include "/" in a pattern, prefix "\" to the "/".

NOTE: The above regular expression pattern for inspecting inheritances is just an
example to show how to use ``#/PATTERN/`` expression.  Tags file generators have
no consensus about the format of ``inherits:``.  Even parsers in ctags have no
consensus. Noticing the format of the ``inherits:`` field of specific languages
is needed for such queries.

The expressions ``#/PATTERN/`` and ``#/PATTERN/i`` are for interactive use.
Readtags also offers an alias ``string->regexp``, so ``#/PATTERN/`` is equal to
``(string->regexp "PATTERN")``, and ``#/PATTERN/i`` is equal to
``(string->regexp "PATTERN" :case-fold #t)``. ``string->regexp`` doesn't need to
prefix "\" for inclulding "/" in a pattern. ``string->regexp`` may simplify a
client tool building an expression. See also :ref:`ctags-client-tools(7) <ctags-client-tools(7)>` for making an
expression in your tool.

Run "readtags -H filter" to know about all valid functions and variables.

Sorting
~~~~~~~
When sorting, the sorter expression is evaluated on two tag entries to decide
which should sort before the other one, until the order of all tag entries is
decided.

In a sorter expression, ``$`` and ``&`` are used to access the fields in the
two tag entries, and let's call them $-entry and &-entry. The sorter expression
should have a value of -1, 0 or 1. The value -1 means the $-entry should sort
before the &-entry, 1 means the contrary, and 0 makes their order in the output
uncertain.

The core operator of sorting is ``<>``. It's used to compare two strings or two
numbers (numbers are for the ``line:`` or ``end:`` fields). In ``(<> a b)``, if
``a`` < ``b``, the result is -1; ``a`` > ``b`` produces 1, and ``a`` = ``b``
produces 0. Strings are compared using the ``strcmp`` function, see strcmp(3).

For example, sort by names, and make those shorter or alphabetically smaller
ones appear before the others:

.. code-block:: console

   $ readtags -S '(<> $name &name)' -l

This reads "If the tag name in the $-entry is smaller, it goes before the
&-entry".

The ``<or>`` operator is used to chain multiple expressions until one returns
-1. For example, sort by input file names, then line numbers if in the same
file:

.. code-block:: console

   $ readtags -S '(<or> (<> $input &input) (<> $line &line))' -l

The ``*-`` operator is used to flip the compare result. i.e., ``(*- (<> a b))``
is the same as ``(<> b a)``.

Inspecting the Behavior of Expressions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The `print` operator can be used to print the value of an expression. For
example:

.. code-block:: console

   $ readtags -Q '(print $name)' -l

prints the name of each tag entry before it. Since the return value of
``print`` is not #f, all the tag entries are printed. We could control this
using the ``begin`` or ``begin0`` operator. ``begin`` returns the value of its
last argument, and ``begin0`` returns the value of its first argument. For
example:

.. code-block:: console

   $ readtags -Q '(begin0 #f (print (prefix? "ctags" "ct")))' -l

prints a bunch of "#t" (depending on how many lines are in the tags file), and
the actual tag entries are not printed.

BUGS
----
Sometimes readtags exits with status 0 even when an error occurs, e.g., when a
directory is passed to the ``-t`` option.

SEE ALSO
--------
See :ref:`tags(5) <tags(5)>` for the details of tags file format.

See :ref:`ctags-client-tools(7) <ctags-client-tools(7)>` for the tips writing a
tool utilizing tags file.

The official Universal-ctags web site at:

https://ctags.io/

The git repository for the library used in readtags command:

https://github.com/universal-ctags/libreadtags

CREDITS
-------
Universal-ctags project
https://ctags.io/

Darren Hiebert <dhiebert@users.sourceforge.net>
http://DarrenHiebert.com/

The readtags command and libreadtags maintained at Universal-ctags
are derrived from readtags.c and readtags.h developd at
http://ctags.sourceforge.net.
