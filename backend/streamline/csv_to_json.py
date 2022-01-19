import csv
import json
 
 
# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_json(csvFilePath):
     
    # create a dictionary
    data = {}
     
    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
         
        # Convert each row into a dictionary
        # and add it to data
        for i,rows in enumerate(csvReader):
             
            # Assuming a column named 'No' to
            # be the primary key
            i = str(i)
            data[i] = rows

    return data
 
    # # Open a json writer, and use the json.dumps()
    # # function to dump data
    # with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
    #     jsonf.write(json.dumps(data, indent=4))
         
