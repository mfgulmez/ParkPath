import keyboard
from myUtils.centroidtracker import CentroidTracker
from myUtils.trackableobject import TrackableObject
from myUtils.classes import classes
from imutils.video import VideoStream
from imutils.video import FPS
from myUtils import config
from csv import DictWriter
import numpy as np
import cv2
import imutils
import time, datetime
import dlib
from tkinter import filedialog, END,Label, Tk, Button,Text,Frame,ttk
import sqlite3
from PIL import Image, ImageTk
import queue
import threading
 
frame_queue = queue.Queue()
 
start_time = datetime.datetime.now()
 
# Arayüzün temel bilseşenleriyle (boyut, başlık) oluşturulması ve sonuç bilgilerinin olduğu text bölgesinin oluşturulması
myForm = Tk()
myForm.title("Capstone Project")
myForm.minsize(width=1100, height=600)
myForm.resizable(width=False, height=False)
 
myForm.grid_rowconfigure(0, weight=0)
myForm.grid_rowconfigure(1, weight=1)
myForm.grid_columnconfigure(0, weight=1)
 
# Create a frame for the video
style = ttk.Style()
style.configure("RoundedFrame.TFrame", corner=10)
 
video_frame = ttk.Frame(myForm, style="RoundedFrame.TFrame")
video_frame.grid_propagate(False)
video_frame.configure(width=410, height=410)
 
video_frame.grid(row=0, column=1, padx=70, pady=70, sticky="nsew")
 
# Configure rows and columns weights for the video frame
video_frame.grid_rowconfigure(0, weight=1)
video_frame.grid_columnconfigure(0, weight=1)
 
# Create a label for the video display
lmain = Label(video_frame, text="Footage")
# Arayüzdeki gerekli komponentlerin ayarı
lmain.grid(row=0, column=0,padx=10, pady=10)
 
controlFrame = Frame(myForm, width=100, height=100)
controlFrame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
 
LabelTxt = Text(controlFrame,height=10, width=50, padx=10, pady=10)
 
class Movie:
    # Video dosya yolunun belirlenmesi ve config dosyasına gönderilmesi
    def openFile(self):
        self.inputFile = filedialog.askopenfilename(initialdir="C:/Users/mfgul/PeopleCount/PeopleCount2", title="Select file",
                                                       filetypes=(("Video files", "*.mp4;*.m4*"), ("all files", "*.*")))
        config.inputSource ='Video'
        config.InputFile = self.inputFile
 
        LabelVideo = Label(controlFrame, text = self.inputFile)
        LabelVideo.grid(row=1, column=0)
   
    # Configdeki kamera enum ına göre belirlenen kamera kaynağının ayarlanması
    def openLive(self):
        config.inputSource = 'Camera'
       
        LabelCam = Label(myForm, text= 'Camera:' + str(config.LiveCamera))
        LabelCam.place(x=140, y=105)
 
    # Configde ayarlanmış seçilen kaynağa göre (video veya kamera) modelin başlatılma fonksiyonu
    def start(self):
        Counter(config.InputFile)
       
    # Programı bitirme fonksiyonu
    def cExit(self):
        exit()
 
 
#Csv dosyasına sonuçların yazdırılma fonksiyonu    
def Write_Csv(totalUp, totalDown, summ1):
    end_time = datetime.datetime.now()
   
    #log_data sözlüğünün gerekli kategorilerle tanımlanıp data_list listesine eklenmesi ve listenin csv dosyasına yazdırılması
    log_data = {}
    data_list = []
    log_data['StartTime'] = 'StartTime:'+ start_time.strftime("%d-%m-%Y %H:%M:%S") + '\n'
    log_data['Total Up'] = 'Total Up:' + totalUp + '\n'
    log_data['Total Down'] = 'Total Down:' + totalDown + '\n'
    log_data['Total_Count'] = 'Total_Count:' + summ1 + '\n'
    log_data['EndTime'] =  'End Time:' + end_time.strftime("%d-%m-%Y %H:%M:%S") + '\n'
    log_data['Duration'] = 'Duration: {}'.format(end_time - start_time) + '\n'
    data_list.append(log_data)
    with open('myUtils\Log.csv', 'w', newline='') as myfile:
        writer = DictWriter(myfile, ('StartTime','Total Up','Total Down','Total_Count','EndTime', 'Duration'))
        writer.writeheader()
        writer.writerows(data_list)
 
    # Sonuçların arayüzdeki text bölgesine eklenmesi
    LabelTxt.insert(END, 'Start Time:' + start_time.strftime("%d-%m-%Y %H:%M:%S") + '\n')
    LabelTxt.insert(END, 'Total Up:' + totalUp + '\n')
    LabelTxt.insert(END, 'Total Down:' + totalDown+ '\n')
    LabelTxt.insert(END, 'Total_Count:' + summ1+ '\n')
    LabelTxt.insert(END, 'End Time:' +  end_time.strftime("%d-%m-%Y %H:%M:%S") + '\n')
    LabelTxt.insert(END, 'Duration: {}'.format(end_time - start_time) + '\n')
 
 
def Write_txt(txtMsg):
    LabelTxt.insert(END, txtMsg + '\n')
 
def main():
    myObj = Movie()
 
    LabelTitle = Label(controlFrame, text=" Capstone Project",font = "Tahoma 12", bg="black", fg="white")
    LabelTitle.grid(row=0, column=0, pady=50, sticky="ew")
   
    BtnVideo = Button(controlFrame, text="Open File", command=myObj.openFile)
    BtnVideo.grid(row=2, column=0, sticky="ew")
   
    ButtonCam = Button(controlFrame, text="Open Camera", command=myObj.openLive)
    ButtonCam.grid(row=3, column=0, sticky="ew")
   
    ButtonCount = Button(controlFrame, text="Count", command=myObj.start)
    ButtonCount.grid(row=4, column=0, sticky="ew")
   
    ButtonExit = Button(controlFrame, text="Exit", command=myObj.cExit)
    ButtonExit.grid(row=5, column=0, sticky="ew")
   
    LabelTxt.grid(row=6, column=0, sticky="ew")
    #Arayüzün devamlı renderlanması için
   
    show_frame()
    # Configure the control_frame to expand
    controlFrame.grid_columnconfigure(1, weight=1)
    controlFrame.grid_rowconfigure(5, weight=1)
    myForm.mainloop()
   
 
def ismorning(time):
    if time < "12:00:00":
        return True
   
def isnoon(time):
    if time >= "12:00:00" and time <= "15:00:00":
        return True
 
def isafternoon(time):
    if time > "15:00:00":
        return True
 
def create_table(c):
    c.execute('CREATE TABLE IF NOT EXISTS DailyData (Date DATE, Visitors VISITORS, Morning_Visitors NUMBER, Noon_Visitors NUMBER, Afternoon_Visitors NUMBER)')
 
def data_entry(visitors, vm, vn, va, c, conn):
    today = datetime.datetime.now()
    formatted_date = today.strftime("%Y-%m-%d")
    c.execute("INSERT INTO DailyData (Date, Visitors, Morning_Visitors, Noon_Visitors, Afternoon_Visitors) VALUES(?, ?, ?, ?, ?)", (formatted_date, visitors, vm, vn, va))
    conn.commit()
 
def Model_Initiation():
    # Configde ayarlanmış model ve prototxt yollarındaki dosyalarla modelin diskten yüklenmesi
    print("[INFO] loading model...")
    return cv2.dnn.readNetFromCaffe(config.Prototxt, config.Model)      
   
def Source_Selection(inputFile):
        #Eğer bir video kaynağı tanımlanmadıysa, kaynağın kamera olarak belirlenip yayının başlatılması
    if config.inputSource == 'Camera':          
        print("[INFO] starting video stream...")
        vs = VideoStream(src=config.LiveCamera).start()
        time.sleep(2.0)
   
    # Video kaynağının seçilmesi
    else:
        print("[INFO] opening video file...")
        vs = cv2.VideoCapture(inputFile)  
    return vs
 
def show_frame():
   
    try:
        # Get the latest frame from the queue
        frame = frame_queue.get_nowait()
        frame = imutils.resize(frame, width = 400, height = 400)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
    except queue.Empty:
        pass
    # Schedule the next frame update
   
 
    lmain.after(2, show_frame)
 
 
def Counter(inputFile):
   # Frame boyutlarının tanımı
    W = None
    H = None
   
    # Centroid tracker (merkez noktası takipçisinin) ve depolanması için listenin tanımı
    ct = CentroidTracker(maxDisappeared=40, maxDistance=50)
    trackers = []
 
    # Her bir obje için dlib korelasyon takipçisi ile birlikte onu kendine has bir ID atanan sözlüğün tanımı
    trackableObjects = {}
 
    # İşlenen frame sayısı ile birlikte çizgiden yukarı veya aşağı giden insanların sayıldığı değişkenlerin tanımı
    totalFrames = 0
    totalDown = 0
    totalUp = 0
    upMorning = 0
    upNoon = 0
    upAfternoon = 0
    totalx = []
    empty=[]
    empty1=[]
    # FPS sayacının başlatılması
    fps = FPS().start()
    # Configde ayarlanmış model ve prototxt yollarındaki dosyalarla modelin diskten yüklenmesi
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe(config.Prototxt, config.Model)      
   
    #Eğer bir video kaynağı tanımlanmadıysa, kaynağın kamera olarak belirlenip yayının başlatılması
    if config.inputSource == 'Camera':          
        print("[INFO] starting video stream...")
        vs = VideoStream(src=config.LiveCamera).start()
        time.sleep(2.0)
   
    # Video kaynağının seçilmesi
    else:
        print("[INFO] opening video file...")
        vs = cv2.VideoCapture(inputFile)  
   
    # FPS sayacının başlatılması
    fps = FPS().start()
    threading.Thread(target=Update_Frame, args=(vs, inputFile, net, ct, trackableObjects, trackers, empty, empty1, fps, W, H, totalFrames, totalUp, totalDown,totalx, upMorning, upAfternoon, upNoon)).start()
 
 
   
def Update_Frame(vs, inputFile, net, ct, trackableObjects, trackers, empty, empty1, fps, W, H, totalFrames, totalUp, totalDown,totalx, upMorning, upAfternoon, upNoon):
    # Yayındaki framelerin üzerine döngü
    while True:
        #Sıradaki frame in okunması
        frame = vs.read()
        frame = frame[1] if config.inputSource == 'Video' else frame
 
        # Eğer video kaynağı okunuyorsa ve videonun sonuna gelinirse programın durdurulması
        if inputFile is not None and frame is None:
            break
 
        # Framein maximum genişliğinin 1000 olarak ayarlanması
        frame = imutils.resize(frame, width = 800)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
   
        # Frame boyutları boşsa frame boyutlarının okunması
        if W is None or H is None:
            (H, W) = frame.shape[:2]
 
            # if (H>500): H=500
 
        # Obje etrafındaki dörtgenin (1) obje saptayıcı veya (2) korelasyon takipçisi
        # tarafından gönderilmesine göre durum değişkeninin tanımı
 
        status = "Waiting"
        rects = []
 
        # Configdeki frame atlayıcı değişkenine
        # göre belirli bir sayıda bir framelerin obje saptanma üzerinme işlenmesi
        if totalFrames % config.SkipFrames == 0:
            # Durum ve yeni takipçi setinin tanımı
            status = "Detecting"
            trackers = []
 
            # frame i blob a çevirerek saptamaları elde etme
            blob = cv2.dnn.blobFromImage(frame, 0.007843, (W, H), 127.5)
            net.setInput(blob)
            detections = net.forward()
 
            # saptamaların döngüsü
            for i in np.arange(0, detections.shape[2]):
                # Model öngörüsü olasılığına dayanan confidence (olasılık)
                # değerinin çıkarılması
             
                confidence = detections[0, 0, i, 2]
 
                # Configdeki confidence değerine göre zayıf gözlemlerinin elenmesi
                if confidence > config.Confidence:
                    # saptama listesindeki sınıf etiketlerinin çıkarılması
                    idx = int(detections[0, 0, i, 1])
 
                    # sınıf etiketi insan değilse görmezden gelinmesi
                    if classes[idx] != "person":
                        continue
 
                    # obje dörtgeninin (x, y) koordinatlarının çıkarılması
                    box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                    (startX, startY, endX, endY) = box.astype("int")
 
                    # Elde edilen koordinatlardan dlib dörtgen objesinin ayarlanması
                    # dlib korelasyon takibinin başlatılması
                    tracker = dlib.correlation_tracker()
                    rect = dlib.rectangle(startX, startY, endX, endY)
                    tracker.start_track(rgb, rect)
 
                    # Atlanılan framelerde faydalanmak üzere takipçi objelerinin listeye eklenmesi
                    trackers.append(tracker)
 
       
        # Atlanılan framelerde obje saptama yerine takipçilerden faydalanılarak
        # Daha iyi bir frame işleme akışının sağlanması
        else:
            # Takipçiler üzerine döngü
            for tracker in trackers:
                # durumun "takip" olarak ayarlanması
                status = "Tracking"
 
                # takipçileri güncelleyerek yeni konumların alınması
                tracker.update(rgb)
                pos = tracker.get_position()
 
                # konumun sayısal verilerinin alınması
                startX = int(pos.left())
                startY = int(pos.top())
                endX = int(pos.right())
                endY = int(pos.bottom())
 
                # add the bounding box coordinates to the rectangles list
                rects.append((startX, startY, endX, endY))
 
        # draw a horizontal line in the center of the frame -- once an
        # object crosses this line we will determine whether they were
        # moving 'up' or 'down'
           
        cv2.line(frame, (0, H // 2), (W, H // 2), (0, 0, 0), 3)#horizontal
        # cv2.line(frame, (W//2, 0), (W//2, H), (0, 255, 255), 2)  #vertical
        cv2.putText(frame, "-Prediction border - Entrance-", (1, (H //2) + 20 )  ,cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        # ((i * 20) + 200)
        # use the centroid tracker to associate the (1) old object
        # centroids with (2) the newly computed object centroids
        objects = ct.update(rects)
        # loop over the tracked objects
        for (objectID, centroid) in objects.items():
            # check to see if a trackable object exists for the current
            # object ID
            to = trackableObjects.get(objectID, None)
 
            # if there is no existing trackable object, create one
            if to is None:
                to = TrackableObject(objectID, centroid)
 
            # otherwise, there is a trackable object so we can utilize it
            # to determine direction
            else:
                # the difference between the y-coordinate of the *current*
                # centroid and the mean of *previous* centroids will tell
                # us in which direction the object is moving (negative for
                # 'up' and positive for 'down')
                y = [c[1] for c in to.centroids]
                direction = centroid[1] - np.mean(y)
                to.centroids.append(centroid)
 
                # check to see if the object has been counted or not
                if not to.counted:
                    # if the direction is negative (indicating the object
                    # is moving up) AND the centroid is above the center
                    # line, count the object
                    if direction < 0 and centroid[1] < H // 2:
                        totalUp += 1
                        empty.append(totalUp)
                       
                        to.counted = True
 
                    # if the direction is positive (indicating the object
                    # is moving down) AND the centroid is below the
                    # center line, count the object
                    elif direction > 0 and centroid[1] > H // 2:
                        totalDown += 1
                        today1 = datetime.datetime.now()
                        hour = today1.strftime("%H:%M:%S")
                        if ismorning(hour):
                            upMorning += 1
                        if isnoon(hour):
                            upNoon +=1
                        if isafternoon(hour):
                            upAfternoon +=1
 
                        empty.append(upMorning)
                        empty.append(upNoon)
                        empty.append(upAfternoon)
                        empty1.append(totalDown)
                        to.counted = True
                       
                    totalx = []
                   
                    # compute the sum of total people inside
                    if(len(empty) != 0 and len(empty1) != 0):
                        totalx.append(max(empty1)-max(empty))
 
            # store the trackable object in our dictionary
            trackableObjects[objectID] = to
 
            # draw both the ID of the object and the centroid of the
            # object on the output frame
            text = "ID {}".format(objectID)
            cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
 
        # construct a tuple of information we will be displaying on the
        info = [
        ("Exit", totalUp),
        ("Enter", totalDown),
        ("Status", status),
        ("Morning Visitors", upMorning),
        ("Noon Visitors", upNoon),
        ("Afternoon Visitors", upAfternoon)
        ]
 
        info2 = [
        ("Total people inside", totalx),
        ]
 
         # Display the output
        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, H - ((i * 20) + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
 
        for (i, (k, v)) in enumerate(info2):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (265, H - ((i * 20) + 60)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
 
        # show the output frame
        if(frame is not None):
            frame = cv2.resize(frame, (500, 500))
            frame_queue.put(frame)
 
        # increment the total number of frames processed thus far and  then update the FPS counter
        totalFrames += 1    
        fps.update()
        if(keyboard.is_pressed("q")):
            break
   
   
    Save(vs, totalUp, totalDown, totalx, upMorning, upAfternoon, upNoon)
 
def Save(vs, totalUp, totalDown, totalx, upMorning, upAfternoon, upNoon):
    conn = sqlite3.connect('pythonDB.db')
    c = conn.cursor()
    create_table(c)
    data_entry(totalDown, upMorning, upAfternoon, upNoon, c, conn)
    # Initiate a simple log to save data at end of the day
    if config.Log:
        Write_Csv(str(totalUp), str(totalDown), str(totalx))
 
    # # if we are not using a video file, stop the camera video stream
    if config.inputSource == 'Camera':
        vs.stop()
 
    # otherwise, release the video file pointer
    else:
        vs.release()
   
 
    # close any open windows
    cv2.destroyAllWindows()
 
if __name__ == "__main__":
    main()