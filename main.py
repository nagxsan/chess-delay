"""
Chess Delay
In professional chess tournaments, there is often a delay in the online broadcasting of the moves played by the players on the live chessboards. This is done as an anti-cheating measure. I am trying to automate this process by accessing the original file at the ith minute, reading and storing it, and then sending it to an FTP server which will broadcast it at the (i + delay)th minute.
"""

# Import necessary modules
from ftplib import FTP, error_perm
import time
import tempfile
import socket


loginFlag = False
storeFileValues = {}

# Upload to FTP function
def uploadToFTP(delay, host, username, password, remoteDirectory, localPath, secondsPassed = 0):

  global loginFlag, storeFileValues

  delayInSec = delay * 60
  numOfBuckets = delayInSec // 10

  print("Entered uploadToFTP func")

  if secondsPassed == 0:
    # Create a dictionary to store the file values at different points in time
    storeFileValues = {time: b'' for time in range(numOfBuckets)}

  try:
    while True:
      
      delayBucket = (secondsPassed // 10) % numOfBuckets

      if secondsPassed >= delayInSec:
        
        if not loginFlag:
          # Connect to the FTP server
          try:
            ftp = FTP(host=host, user=username, passwd=password)
          except socket.error:
            print("Error connecting to FTP server due to internet issues.")
            time.sleep(5)
            uploadToFTP(delay, host, username, password, remoteDirectory, localPath, secondsPassed)
          except error_perm as e:
            print("Credentials are bad!")

          print("Logged in to FTP server!")

          # Change to the remote directory
          ftp.cwd(remoteDirectory)

          print("Connected to FTP server!")

          loginFlag = True

        # Upload the file to the FTP server
        with tempfile.TemporaryFile() as fp:
          fp.write(storeFileValues[delayBucket])
          fp.seek(0)
          print("Start uploading file")
          try:
            ftp.storbinary('STOR games.pgn', fp)
          except error_perm as e:
            print(f"Error uploading file: {e}")
          print("Completed uploading file!")
          fp.close()
      
      # Open the local file in binary mode
      with open(localPath, 'rb') as file:
        storeFileValues[delayBucket] = file.read()
      
      time.sleep(10)
      secondsPassed += 10
      print("Seconds passed: ", secondsPassed)
  except socket.error:
    print("Maybe connection timed out. Retrying...")
    loginFlag = False
    time.sleep(5)
    uploadToFTP(delay, host, username, password, remoteDirectory, localPath, secondsPassed)
  except KeyboardInterrupt:
    print("Terminating Program! Please wait.")

# Start execution
if __name__ == "__main__":

  print("Developed and maintained by Sanchet Sandesh Nagarnaik.")

  delay = int(input("Please enter desired delay time (just the number of minutes): "))
  host = input("Please enter the FTP host address: ")
  username = input("Please enter the FTP server username: ")
  password = input("Please enter the FTP server password: ")
  remoteDirectory = input("Please enter the path on the FTP server where you want to store this file: ")
  localPath = input("Please enter the local file path (complete file path): ")

  uploadToFTP(delay, host, username, password, remoteDirectory, localPath)

  print("Program ended successfully.")


