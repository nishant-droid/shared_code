from tkinter import filedialog
from os import rename as rn
from os import remove as rm

from pathlib import Path
from os import path as path
import csv

final_file_destination = "/home/nishant/Documents/try/shared_code/app/static/uploads"

class File_Handle():
    def __init__(self):
        self.f_ext = None


    def File_check(self,hfile):
        f_name,f_ext = path.splitext(hfile.filename)
        if f_ext == "":
            save_path = path.join(final_file_destination,f_name)
            hfile.save(save_path)
            return save_path
        else:
            return False


    def File_Selection(self,filename,hopper_date,hopper_time):

        #Converts the Hopper.txt fixed width file to out.csv delimited file
        IN_FILE = filename
        OUT_FILE = filename + ".csv"
        RANGES = ((0, 10), (18, 19), (45, 18), (66, 19), (88, 19), (114, 19),
                (136, 19), (157, 19), (179, 19), (203, 19), (223, 10))
        try:
            rfp = open(IN_FILE, 'r', encoding="UTF-8")
        except IOError:
            print("Could not read from", IN_FILE)
            raise SystemExit

        try:
            wfp = open(OUT_FILE, 'w', encoding="UTF-8")
        except IOError:
            print("Could not write to", OUT_FILE)
            raise SystemExit
        for line in rfp:
            parts = []
            for rng in RANGES:
                parts.append(line[rng[0]:rng[0] + rng[1]].strip())
            wfp.write(",".join(parts) + "\n")

        rfp.close()
        wfp.close()

        # Removes the unncessary data from the file.
        file_path = OUT_FILE
        with open(file_path, "r", encoding="UTF-8") as file:
            lines = file.readlines()
        with open(file_path, "w", encoding="UTF-8") as file:
            check = "M1GMG"
            for line in lines:
                if check in line:
                    file.write(line)


        # Date and time column are added to the hopper file
        ReadFile = OUT_FILE
        DateStamp = [hopper_date]
        TimeStamp = [hopper_time]
        destination_folder = path.dirname(ReadFile)
        destination_file = destination_folder + "/Hopper.csv"
        with open(ReadFile, "r+", encoding="UTF-8") as f_in, open(destination_file, 'w', encoding="UTF-8") as f_out:
            reader = csv.reader(f_in, delimiter=',')
            FileWriter = csv.writer(f_out)
            for line in reader:
                FileWriter.writerow(line + DateStamp + TimeStamp)

    def Push_Data_Into_Table():
        if path.exists(initial_file): 
            my_cursor.execute("use Hopper")
            my_cursor.execute("load data infile 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Hopper.csv' into table File_History fields terminated by ',' lines terminated by '\n'")
            mydb.commit()