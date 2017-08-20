Bradley
=======

|build-status| |coverage-status| |docs|

Bradley is a Personal Relationship Management (PRM) system, similar to Monica_,
but written in Python.

Well, it isn't that *yet*. Right now, I'm just playing around with Flask_
and GraphQL_. But that's the eventual goal.

.. _Monica: https://monicahq.com/
.. _Flask: http://flask.pocoo.org/
.. _GraphQL: http://graphql.org/

Install & Run
-------------

Make sure you have a local PostgreSQL_ server running. Then run:

.. code-block:: bash

    pip install -r requirements.txt
    export FLASK_APP=bradley/app.py
    flask db create
    flask run

You can run ``flask --help`` to see what other commands are available.

.. _PostgreSQL: https://www.postgresql.org/

.. |build-status| image:: https://travis-ci.org/singingwolfboy/bradley.svg?branch=master&style=flat
   :target: https://travis-ci.org/singingwolfboy/bradley
   :alt: Build status
.. |coverage-status| image:: http://codecov.io/github/singingwolfboy/bradley/coverage.svg?branch=master
   :target: http://codecov.io/github/singingwolfboy/bradley?branch=master
   :alt: Test coverage
.. |docs| image:: https://readthedocs.org/projects/bradley/badge/?version=latest&style=flat
   :target: http://bradley.readthedocs.org/
   :alt: Documentation
