"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TwelfthDoctor1's MasterApprentice Logger

(C) Copyright TD1 & TWoCC 2021

Licensed under MIT License
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The MasterApprentice Logger is a library that consists of two loggers named:
    > ApprenticeLogger
    > MasterLogger

Usage of this Module can either be a direct import usage or a try except usage:

    Where try:
    imports Module

    returns True for variable for Test Checking.

    While except checks for ImportError:

    returns False for variable for Test Checking.

    Variable Usages:
        These variables should not be made global, keep them as LOCAL.

        ~ apprentice_logger
        ~ master_logger

    When logging:
        Run this conditional statement:

        if [VARIABLE] is not None and [VARIABLE] is not False:
            logger_var.level_type(message, owner)

"""