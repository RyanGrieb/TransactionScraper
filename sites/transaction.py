from datetime import datetime
from multiprocessing.sharedctypes import Value


class Transaction:
    def __init__(self, date, desc, amount, account):

        if isinstance(date, datetime):
            self.date = date
        else:
            self.date = None
            year = date.split('/')[-1]

            try:
                if (len(year) > 2):
                    self.date = datetime.strptime(date, '%m/%d/%Y')
                else:
                    self.date = datetime.strptime(date, '%m/%d/%y')
            except ValueError:
                # FIXME: This might be a problem in a few millenia
                # This is set when the transaction is pending to provide proper sorting
                self.date = datetime(9999, 9, 9)

        self.desc = desc
        self.amount = amount
        self.account = account

    def __str__(self):
        return "{} {} {}".format(
            self.pretty_date(), self.desc, self.amount, self.account)

    def pretty_date(self):
        if self.date.year >= 9999:
            return 'Pending...'

        return self.date.strftime('%m/%d/%y')

    def matches(self, other_transaction):
        return self.desc == other_transaction.desc and self.account == other_transaction.account and self.amount == other_transaction.amount and self.date == other_transaction.date and self.desc == other_transaction.desc
