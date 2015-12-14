import numpy, matplotlib



def extract_file(file):
    reader = open(file, 'r')
    flag_first_line = True
    buffer = ''
    for line in reader:
        if flag_first_line:
            flag_first_line = False
            continue

        buffer = buffer + line

    # print 'End of file: {0}'.format(file)
    return buffer



def import_csv(file):
    file_data = extract_file(file)
    print file_data

def plot_matplotlib(data):
    print 'Plotting'
    

def _main():
    files = ['0.csv']
    # files = ['1.csv', '2.csv']
    for file in files:
        data = import_csv(files)
        plot_matplotlib(data)


if __name__ == '__main__':
    _main()