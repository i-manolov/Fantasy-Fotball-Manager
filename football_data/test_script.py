import csv



def rewrite_top_row():
    bottle_list = []
    with open('temp.csv', 'rb') as file:
        bottles = csv.reader(file)
        bottle_list.extend(bottles)
    # data to override in the format {line_num_to_override:data_to_write}. 
    line_to_override = {1:['e', 'c', 'd'] }

    # Write data to the csv file and replace the lines in the line_to_override dict.
    with open('temp.csv', 'wb') as file:
        writer = csv.writer(file)
        for line, row in enumerate(bottle_list):
            data = line_to_override.get(line, row)
            writer.writerow(data)

rewrite_top_row()



