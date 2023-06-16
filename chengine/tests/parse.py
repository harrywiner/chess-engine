import csv

# Chat GPT
def read_csv(file_path):
    data = []
    
    with open(file_path, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        
        # Read the data rows
        for row in reader:
            data.append(row)
    
    return data