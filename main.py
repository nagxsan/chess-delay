"""
Chess Delay
In professional chess tournaments, there is often a delay in the online broadcasting of the moves played by the players on the live chessboards. This is done as an anti-cheating measure. I am trying to automate this process by accessing the original file at the ith minute, reading and storing it, and then sending it to an FTP server which will broadcast it at the (i + delay)th minute.
"""

# Import necessary modules
from ftplib import FTP
import time
import threading


# Flag to exit the loop
exitFlag = False

# Command listener to exit the loop
def commandListener():
  
  global exitFlag

  command = input("Enter 'exit' to break the loop: ")
  if command.lower() == "exit":
    exitFlag = True
    return

# Upload to FTP function
def uploadToFTP(delay, host, username, password, remoteDirectory, localPath):

  global exitFlag

  # Create a dictionary to store the file values at different points in time
  storeFileValues = {time: "" for time in range(delay)}

  # Connect to the FTP server
  ftp = FTP(host)
  ftp.login(username, password)

  # Change to the remote directory
  ftp.cwd(remoteDirectory)

  # Keep track of time in mins
  minsPassed = 0

  while not exitFlag:

    if minsPassed >= delay:
      # Upload the file to the FTP server
      ftp.storbinary(f'STOR games.pgn', storeFileValues.get(minsPassed % delay))
    
    # Open the local file in binary mode
    with open(localPath, 'rb') as file:
      storeFileValues[minsPassed % delay] = file
    
    minsPassed += 1
    time.sleep(60)
  
  # Close the FTP connection
  ftp.quit()

# Start execution
if __name__ == "__main__":

  delay = int(input("Please enter desired delay time (just the number of minutes): "))
  host = input("Please enter the FTP host address: ")
  username = input("Please enter the FTP server username: ")
  password = input("Please enter the FTP server password: ")
  remoteDirectory = input("Please enter the path on the FTP server where you want to store this file: ")
  localPath = input("Please enter the local file path (complete file path): ")

  # Start the uploading file loop in a separate thread
  loopThread = threading.Thread(target=uploadToFTP(delay, host, username, password, remoteDirectory, localPath))
  loopThread.start()

  # Start the command listener in main thread
  commandListener()

  # Wait for the file upload thread to finish
  loopThread.join()

  print("Program ended successfully.")


