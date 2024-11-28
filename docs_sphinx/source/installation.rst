Installation Guide
=================

Requirements
-----------

- Python 3.7 or later
- pip package manager

Installation Methods
------------------

Using pip
~~~~~~~~~

The recommended way to install Evo Client Python is using pip:

.. code-block:: bash

    pip install evo-client-python

From Source
~~~~~~~~~~

You can also install from source:

.. code-block:: bash

    git clone https://github.com/your-org/evo-client-python.git
    cd evo-client-python
    pip install -e .

Development Installation
~~~~~~~~~~~~~~~~~~~~~~

For development, install additional dependencies:

.. code-block:: bash

    pip install -r requirements.txt
    pip install -r test-requirements.txt

Verification
-----------

To verify the installation:

.. code-block:: python

    import evo_client
    print(evo_client.__version__)

Troubleshooting
--------------

Common Issues
~~~~~~~~~~~~

1. **ImportError**: Make sure you have all required dependencies installed
2. **VersionError**: Ensure you're using Python 3.7 or later
3. **SSL Certificate Error**: Check your SSL certificates and network connection

Getting Help
~~~~~~~~~~~

If you encounter any issues:

1. Check the :doc:`examples/index` for proper usage
2. Search existing GitHub issues
3. Create a new issue if the problem persists
