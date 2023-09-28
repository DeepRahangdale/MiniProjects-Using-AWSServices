# GUI for T2S Converter
import tkinter as tk #module in python to prepare the GUI
import boto3
import os
import sys
from tempfile import gettempdir
from contextlib import closing


root=tk.Tk()
root.geometry("400x240")
root.title("T2S-Converter Amazon Polly")

textExample=tk.Text(root,height=10)
textExample.pack()

def getText():
    aws_mag_con=boto3.session.Session(profile_name='text-to-speech')
    client=aws_mag_con.client(service_name='polly',region_name='us-east-1')

 # Get the text entered by the user    
    result=textExample.get("1.0","end")
    print(result)

# Use Polly to synthesize speech from the text    
    response=client.synthesize_speech(VoiceId='Joanna',OutputFormat='mp3',Text=result,Engine='neural')
    print(response)

    if "AudioStream" in response:
        with closing(response['AudioStream']) as stream:
            output=os.path.join(gettempdir(),"speech.mp3")
            try:
                with open(output,"wb") as file:
                    file.write(stream.read())
                print("Text converted to speech successfully!")

            except IOError as error:
                print(error)
                sys.exit(-1)

    else:
        print("Could not find the stream!!")   
        sys.exit(-1)


# If the platform is Windows, open the MP3 file with the default application        
    if sys.platform=='win32':
        os.startfile(output)                     


# Create a button that triggers the text-to-speech conversion when clicked
btnRead=tk.Button(root,height=1,width=10,text="Convert",command=getText)
btnRead.pack()

root.mainloop()