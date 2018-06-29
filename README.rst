#############################
BlackMarket's Molecule Parser
#############################

MoleculeParser is a Python project, designed by BlackMarket(Fr) to assess possible job candidates.


************
Requirements
************

MoleculeParser requires Python3.5+. 

No other library or dependencies are required to `run` this project.
But in order to generate coverage reports, installing coverage is recommended.
Requirements can be installed using the following command:

.. code-block:: shell
    pip install -r requirements.txt
    # Or since only coverage is required
    pip install coverage

***************
Getting Started
***************

Simply issue the following commands in project directory:

.. code-block:: shell

    python molecule_parser/main.py
    # OR
    cd molecule_parser
    python main.py

Project's root directory (e.g. blackmarket) is automatically added to your python path so
imports should be fine and you won't need to do any setup.

*************
Running Tests
*************

To run the tests, simply run them using the following command

.. code-block:: shell

    cd blackmarket
    python -m unittest

To run the tests with coverage, simply run the following:

.. code-block:: shell

    cd blackmarket
    coverage run -m unittest
    coverage report

Please notice that these commands should be run on the same level as the molecule_parser directory [so, in PROJECT_DIRECTORY]

**********
References
**********

I examined several approaches, and meanwhile checked out different resources.

Most notable of those were the following:

https://docs.python.org/3.5/library/re.html
http://folk.ntnu.no/haugwarb/TKP4106/Tore/Syllabus/topic_03/index.html
https://stackoverflow.com/questions/546433/regular-expression-to-match-outer-brackets

*******
Contact
*******

Email me at alireza@pushe.co / alirezasadeghi71@gmail.com and I'll get back to you asap.

