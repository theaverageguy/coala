from coalib.output.printers.Printer import Printer


class ClosablePrinter(Printer):
    """
    This is a printer that needs to be closed. If it is not closed the
    programmer will be warned, hopefully the user will never see any
    functionality coming from this printer.
    """
    def __del__(self):  # pragma: no cover
        """
        May warn if not closed properly - programmer error!

        Cannot deterministically be tested.
        """
        if not self._closed:
            self.print("{} needs to be closed manually.".format(
                self.__class__.__name__))
            self.close()