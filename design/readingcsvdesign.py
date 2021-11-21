import csv


def reading_csv_design(name_of_file):
    """
    The function reads special csv table with design and
    makes of it format dict
    :param name_of_file:
    :return: (dict)
    """
    with open(file=name_of_file) as csvfile:
        design = csv.reader(csvfile, delimiter=';', quotechar='"')

        design_dict = dict()

        for widget, name, value in design:
            if widget not in design_dict:
                design_dict[widget] = str()

            design_dict[widget] += f'{name}: {value};'

        return design_dict


if __name__ == '__main__':
    from pprint import pprint
    pprint(reading_csv_design('design.csv'))
