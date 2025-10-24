from num2words import num2words

### A MarketDataTable object is not the table itself, but rather information about the table
class MarketDataTable:
    def __init__(self, acronym, timeunit, denomination, name=None):
        ### acronym is the 3 letter crypto acronym
        self.acronym = acronym
        if timeunit.lower() not in ["hour", "day", "min"]:
            raise ValueError("Invalid value. Allowed values are min, hour, day")
        ### timeunit is min, hour, or day
        self.timeunit = timeunit
        ### denominaiton is the number of timeunit e.g. the 15 in "15min"
        self.denomination = denomination
        ### name is the name of the table derived from the previous 3 vairables automatically
        if name is not None:
            self.name = name
        elif timeunit == "min":
            self.name = acronym + f'_USD_{num2words(denomination).replace('-', '_').upper()}_MINUTE_CANDLES'
        else:
           self.name = acronym + f'_USD_{num2words(denomination).replace('-', '_').upper()}_{timeunit.upper()}_CANDLES'
    ### Converts object to string
    def __str__(self):
        return f"MarketDataTable(acronym={self.acronym}, timeunit={self.timeunit}, denomination={self.denomination}, name={self.name})"
    ### Allows printing of object
    def __repr__(self):
        return f"<MarketDataTable(acronym={self.acronym}, timeunit={self.timeunit}, denomination={self.denomination}, name={self.name})>"
