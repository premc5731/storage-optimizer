import os
import sys
import time
import hashlib # used to calculate checksum
import schedule
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
from S3_upload import upload_file_to_s3

def SendMail(log_filename,files_data):

    print("Sending email...")
    
    from_address = "ajay194703@gmail.com"
    to_address = sys.argv[3]
    load_dotenv()
    password = os.getenv("EMAIL_PASSWORD")
    
    msg = MIMEMultipart()

    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = "Delete Duplicate Files"

    body =(
    "Starting time of scanning : %s \n"
    "Total number of files scanned : %s \n"
    "Total number of duplicate files found : %s \n"
    "This is a log file of python script scheduled to delete duplicate files \n"
    )%(files_data[0],files_data[1],files_data[2])

    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent 
    filename = os.path.basename(log_filename)
    attachment = open(log_filename, "rb")

    # instance of MIMEBase
    mimebase_obj = MIMEBase('application', 'octet-stream')
    # To change the payload into encoded form
    mimebase_obj.set_payload((attachment).read())
    encoders.encode_base64(mimebase_obj)
    
    mimebase_obj.add_header('Content-Disposition', "attachment; filename= %s" %(filename))

    msg.attach(mimebase_obj)

    server_connection = smtplib.SMTP('smtp.gmail.com', 587)
    server_connection.starttls()
    server_connection.login(from_address, password)
    text = msg.as_string()
    server_connection.sendmail(from_address, to_address, text)
    server_connection.quit()

    print("Email sent successfully")


def CreateLog(FolderName, Data,files_data):

    flag = os.path.isabs(FolderName)
    if(flag == False):
        FolderName = os.path.abspath(FolderName)

    FolderName = os.path.join(FolderName,"LogFiles")

    flag = os.path.exists(FolderName)
    if flag == False:
        os.mkdir(FolderName)

    timestamp = time.ctime()
    filename = "Delete_Duplicate_Files_Log %s.log" %(timestamp)
    filename = filename.replace(" ","_")
    filename = filename.replace(":","_")
    filename = filename.replace("__","_")

    filename = os.path.join(FolderName,filename)

    fobj = open(filename, "w")

    border = "-"*80
    fobj.write(border+"\n")
    fobj.write("This is a log file of delete_duplicate_files automation script\n")
    fobj.write(border+"\n")

    for value in Data:
        fobj.write(value)


    fobj.write(border+"\n")
    fobj.write("Total deleted files : %s \n"%(len(Data)))
    fobj.write("This file is created at\n"+timestamp+"\n")
    fobj.write(border+"\n")

    fobj.close()

    files_data.append(len(Data))
    SendMail(filename,files_data)

    object_name = f'logs/Delete_Duplicate_Files_Log{timestamp}.log'
    upload_file_to_s3(filename,'delete-duplicate-files',object_name)


def CalculateCheckSum(path,BlockSize = 1024):
    fobj = open(path,'rb')

    hobj = hashlib.md5()

    buffer = fobj.read(BlockSize)
    while(len(buffer) > 0):
        hobj.update(buffer)
        buffer = fobj.read(BlockSize)

    fobj.close()

    return hobj.hexdigest()

def FindDuplicate(DirectoryName):
    
    flag = os.path.isabs(DirectoryName)

    if(flag == False):
        DirectoryName = os.path.abspath(DirectoryName)

    flag = os.path.exists(DirectoryName)

    if(flag == False):
        print("The path is invalid")
        exit()

    flag = os.path.isdir(DirectoryName)

    if (flag == False):
        print("Path is valid but target is not a directory")
        exit()
    files_data = []
    files_data.append(time.ctime())
    count = 0
    Duplicate = {}

    for FolderName, SubFolderNames, FileNames in os.walk(DirectoryName) :
        
        for fname in FileNames:
            count += 1
            fname = os.path.join(FolderName,fname)
            checksum = CalculateCheckSum(fname)

            if(checksum in Duplicate):
                Duplicate[checksum].append(fname)

            else:
                Duplicate[checksum] = [fname]
    
    files_data.append(count)

    return Duplicate , files_data
            
def DeleteDuplicate(path):

    MyDict, files_data = FindDuplicate(path)
    Result = list(filter(lambda x : len(x) > 1, MyDict.values()))

    Count = 0
    Cnt = 0
    log_data = []

    for value in Result:
        for subvalue in value:
            Count = Count + 1
            
            if(Count > 1):
                log_string = "%s deleted at : %s \n"%(subvalue,time.ctime())
                log_data.append(log_string)
                os.remove(subvalue)
                Cnt = Cnt + 1
        Count = 0

    print("Total deleted files : ",Cnt)

    CreateLog(path,log_data,files_data)
    
def main():

    Border = "-"*44
    print(Border)
    print("Automation Script Starting...")
    print(Border)   
     
    if(len(sys.argv) == 2) :
        if((sys.argv[1] == "--h")  or (sys.argv[1] == '--H')):
            print("This application is used to perform directory cleaning")
            print("This is the directory automation script")
        elif((sys.argv[1] == "--u")  or (sys.argv[1] == '--U')):
            print("Use the given script as ")
            print("ScriptName.py  NameOfDirectory TimeInterval(minutes) Receiver'sMailId ")
            print("Please provide valid absolute path")
        else:
            print("Invalid number of command line arguments")
            print("Use the given flags as : ")
            print("--h is used to display the help")
            print("--u is used to display the usage")

    if(len(sys.argv) == 4):
            schedule.every(int(sys.argv[2])).minutes.do(lambda : DeleteDuplicate(sys.argv[1]))

            while True:
                schedule.run_pending()
                time.sleep(1)
    elif((len(sys.argv) != 2) and (len(sys.argv) != 4) ):
        print("Invalid number of command line arguments")
        print("Use the given flags as : ")
        print("--h is used to display the help")
        print("--u is used to display the usage")

    print(Border)
    print("-------Thank you for using our script-------")
    print(Border)
            
if __name__ == "__main__":
    main() 