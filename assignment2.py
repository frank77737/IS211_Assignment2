import argparse
import urllib.request
import logging
import datetime
import sys

def downloadData(url):
    with urllib.request.urlopen(url) as response:
        data = response.read().decode('utf-8')
    return data

def processData(file_content):
    lines = file_content.strip().split('\n')
    line_num = 1

    logger = logging.getLogger('assignment2')
    personData = {}
    

    for line in lines:
        if line.startswith("id,"):
            #If first row skip it
            line_num += 1
            continue

        columns = line.split(',')
        # split into 3 columns 
        if len(columns) != 3:
            line_num += 1
            continue

        # shuffle columns around to order specificiations
        id_str = columns[0].strip()     
        name = columns[1].strip()      
        birthday_str = columns[2].strip() 

        #change stirng to int 
        try:
            row_id = int(id_str)
        except ValueError:
            line_num += 1
            continue

        # Normalzies data column into d/m/y if possible if not possible it throws a error 
        try:
            birthday = datetime.datetime.strptime(birthday_str, "%d/%m/%Y")
        except ValueError:
            logger.error(f"Error processing line #{line_num} for ID #{row_id}")
            line_num += 1
            continue

        # Add to dictionary lookup if everything works 
        personData[row_id] = (name, birthday)
        line_num += 1

    return personData


def displayPerson(row_id, personData):
    if row_id not in personData:
        print("No user found with that id")
    else:
        name, bday = personData[row_id] #extract data from the row id 
        print(f"Person #{row_id} is {name} with a birthday of {bday.strftime('%Y%m%d')}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    args = parser.parse_args()
    
    logging.basicConfig(
        filename='error.log',
        level=logging.ERROR,
        filemode='w',
        format='%(message)s'
    )

    try:
        csvData = downloadData(args.url)
    except Exception as e:
        print(f"Error downloading data: {e}")
        sys.exit(1)

    personData = processData(csvData)

    # Loop asking for user input
    while True:
        console_input = input("Enter an ID to look up (<= 0 to quit): ")
        try:
            console_id_number = int(console_input)
        except ValueError:
            print("Enter a number above 0.")
            continue

        if console_id_number <= 0:
            print("Ending Program.")
            break

        displayPerson(console_id_number, personData)

if __name__ == "__main__":
    main()
