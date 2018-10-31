class HeatPumpReadout:
    dictionary = None

    def __init__(self, filename):
        self.__read_tsv(filename)

    ## Read a TSV file (same as they use for the SPSs) into a dictionary of sensor readings.
    # @param filename The path to the TSV (or XLS) file to parse
    # @return A dictionary indexed by sensor name with arrays of sensor data
    def __read_tsv(self, filename):
        file = open(filename, 'r')
        lines = file.readlines()
        title_line_number = self.find_first_non_empy_line(lines)
        titles = self.parse_line(lines[title_line_number].replace('\n', ''))

        dictionary = dict()

        for title in titles:
            dictionary[title] = []

        for index in range(title_line_number + 1, len(lines)):
            data = self.parse_line(lines[index].replace('\n', ''))
            for d_index in range(0, len(data)):
                if data[d_index].strip().isnumeric():
                    dictionary[titles[d_index]].append(int(data[d_index]))
                else:
                    dictionary[titles[d_index]].append(data[d_index])

        file.close()

        self.dictionary = dictionary
        return dictionary

    ## Gets a single row of data from the dictionary. This returns a dictionary with the names of the columns but with
    # a single element from the selected row
    # @param number The row number (starting at 0) of the data to return
    # @returns A dictionary containing the names as the keys and the single data points as the values
    def get_row(self, number):
        single_row = dict()
        for col in self.dictionary.keys():
            single_row[col] = self.dictionary[col][number]
        return single_row

    ## Gets a single column of the data from the dictionary by name
    # @param name The name of the column to return
    # @returns An array of data points in that column
    def get_col(self, name):
        return self.dictionary[name]

    ## Gets a single data point from the dictionary based off the name of the column and the row number
    # @param col_name The name of the column selected
    # @param row_num The number of the row selected
    # @returns A single data point (usually a number)
    def get_point(self, col_name, row_num):
        return self.dictionary[col_name][row_num]

    ## Parse a single line of tsv, allowing columns to be empty to comply with the formatting of the SPS's fields
    # @param line The line in a string
    # @return An array of data representing data from each column of the spreadsheet
    @staticmethod
    def parse_line(line):
        prev_i = 0
        i = 0
        entries = []
        while i <= len(line):
            if i >= len(line) or line[i] in "\t\n":
                entries.append(line[prev_i:i])
                prev_i = i + 1
            i += 1
        return entries

    ## Find the first non empty line in a list of lines (useful for finding the title line in the SPS's files)
    # @param lines The array of lines to find the first used line in
    # @return The line number of the first used line
    @staticmethod
    def find_first_non_empy_line(lines):
        ret = 0
        while lines[ret].replace('\n', '') is "":
            ret += 1
        return ret



# row = a.get_row(1)
# point = row['02_Saus2']