class ELFWithoutSymbols(Exception):
    """
    Class that represent an exception that occurs when the offset finder tries to find symbols in a ELF that contains
    no symbols
    """
    pass
