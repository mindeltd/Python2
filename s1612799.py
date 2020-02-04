"""Python kurso antra uzduotis
  atliko Mindaugas Romaska"""

# Evaluation 3 (copy paste)  
  
from collections import namedtuple
import datetime

class DataManipulation:
    """Klase kurioje implementuotos select,filter,sort funkcijos"""
    dict = {}
    data = []

    def __init__(self, csv_reader):
        """sukuria namedTuple ir priskiria reiksmes tinkamui tipui"""
        header = (next(csv_reader))
        tuple_type = namedtuple('tuple_type', [*header])
        temp = []
        tuple_list = []
        for row in csv_reader:
            temp.append(tuple_type(*row))
        for value in header:
            nulls = 0
            for row in temp:
                if(getattr(row, value)) != "":
                    self.todict(row, value)
                    break
                else:
                    nulls = nulls + 1
                    if nulls == len(temp):
                        self.todict(row, value)
                    continue
        for line in temp:
            row = []
            for column in header:
                value = (getattr(line, column))
                try:
                    value = self.dict[column](value)
                except ValueError:
                    pass
                except TypeError:
                    if (self.dict[column] == datetime and getattr(line, column) != ''):
                        value = datetime.datetime.strptime(getattr(line, column), '%Y-%m-%d').date()
                row.append(value)
            tuple_list.append(tuple_type(*row))
        self.data = tuple_list

    def select(self, *args):
        """Pasirenka duomenis pagal pasirinktus stulpelius"""
        tuple_list = self.get()
        keys = []
        for value in args:
            try:
                type(self.dict[value])
                keys.append(value)
            except AttributeError:
                raise KeyError('{} column do not exists!'.format(value))
        tuple_type = namedtuple('tuple_type', [*keys])
        temp_list = []
        for line in tuple_list:
            tuple_row = []
            for key in keys:
                tuple_row.append(getattr(line, key))
            temp_list.append(tuple_type(*tuple_row))
        self.data = temp_list

    def filter(self, column, operator, comparison):
        """Filtruoja pasirinkto stulpelio duomenis"""
        tuple_list = self.get()
        values = []
        for line in tuple_list:
            try:
                if operator(getattr(line, column), comparison):
                    values.append(getattr(line, column))
            except AttributeError:
                raise KeyError('{} column do not exists!'.format(column))
            except TypeError:
                pass
        self.data = values

    def sort(self, *args):
        """Rusiuoja namedTuple'a pagal pasirinktus stulpelius ir tvarka"""
        tuple_list = self.get()
        count = []
        empty_string = ''
        for arg in args:
            count.append(arg[1:])
        if (len(count) != len(set(count)) or not count):
            raise KeyError('No args were given or column was used more than one time')
        for arg in reversed(args):
            if arg[:1] == '+':
                rev = False
            else:
                rev = True
            column = arg[1:]
            try:
                if self.dict[arg[1:]] != str:
                    tuple_list.sort(key=lambda x, clm=column: \
                        (getattr(x, clm) is empty_string, \
                        getattr(x, clm)), reverse=rev)
                    self.data = tuple_list
                else:
                    tuple_list.sort(key=lambda x, clm=column: (getattr(x, clm)), reverse=rev)
                    self.data = tuple_list
            except AttributeError:
                raise KeyError('{} column do not exists!'.format(arg[1:]))

    def get(self, types=False):
        """Grazina NamedTuple'a arba tipu zodyna"""
        if types is False:
            return self.data
        return self.dict

    def save(self, csvreader):
        """Israso duomenis i csv faila"""
        csvreader.writerow(self.data[10]._fields)
        for line in self.data:
            csvreader.writerow(line)

    def todict(self, row, value):
        """Sukuria duomenu tipu dict'a"""
        data = getattr(row, value)
        try:
            temp = datetime.datetime.strptime(data, '%Y-%m-%d')
        except ValueError:
            pass
        else:
            self.dict[value] = datetime
            return
        try:
            temp = int(data)
        except ValueError:
            pass
        else:
            self.dict[value] = type(temp)
            return
        try:
            temp = float(data)
        except ValueError:
            pass
        else:
            self.dict[value] = type(temp)
            return
        try:
            temp = str(data)
        except ValueError:
            pass
        else:
            self.dict[value] = type(temp)
            return
