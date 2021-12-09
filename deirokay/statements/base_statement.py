import pandas as pd


class BaseStatement:
    """Base abstract statement class for all Deirokay statements.

    Parameters
    ----------
    options : dict
        Statement parameters provided by user.

    Attributes
    ----------
    name : str
        Statement name when referred in Validation Documents (only
        valid for non-custom statements).
    expected_parameters : List[str]
        Parameters expected for this statement.
    table_only : bool
        Whether or not this statement in applicable only to the entire
        table, instead of scoped columns.
    """

    name = 'base_statement'
    expected_parameters = ['type', 'severity', 'location']
    table_only = False

    def __init__(self, options: dict):
        self._validate_options(options)
        self.options = options

    def _validate_options(self, options: dict):
        """Make sure all providded statement parameters are expected
        by statement classes"""
        cls = type(self)
        unexpected_parameters = [
            option for option in options
            if option not in (cls.expected_parameters +
                              BaseStatement.expected_parameters)
        ]
        if unexpected_parameters:
            raise ValueError(
                f'Invalid parameters passed to {cls.__name__} statement: '
                f'{unexpected_parameters}\n'
                f'The valid parameters are: {cls.expected_parameters}'
            )

    def __call__(self, df: pd.DataFrame):
        """Run statement instance."""
        internal_report = self.report(df)
        result = self.result(internal_report)

        final_report = {
            'detail': internal_report,
            'result': result
        }
        return final_report

    def report(self, df: pd.DataFrame) -> dict:
        """Receive a DataFrame containing only columns on the scope of
        validation and returns a report of related metrics that can
        be used later to declare this Statement as fulfilled or
        failed.

        Parameters
        ----------
        df : pd.DataFrame
            The scoped DataFrame columns to be analysed in this report
            by this statement.

        Returns
        -------
        dict
            A dictionary of useful statistics about the target columns.
        """
        return {}

    def result(self, report: dict) -> bool:
        """Receive the report previously generated and declare this
        statement as either fulfilled (True) or failed (False).

        Parameters
        ----------
        report : dict
            Report generated by `report` method. Should ideally
            contain all statistics necessary to evaluate the statement
            validity.

        Returns
        -------
        bool
            Whether or not this statement passed.
        """
        return True

    @staticmethod
    def profile(df: pd.DataFrame) -> dict:
        """Given a template data table, generate a statement dict
        from it.

        Parameters
        ----------
        df : pd.DataFrame
            The DataFrame to be used as template.

        Returns
        -------
        dict
            Statement dict.
        """
        raise NotImplementedError
