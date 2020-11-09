from tkinter import *
import pygame
import time
pygame.mixer.init()
window = Tk()
window.title('Alarm')
window.geometry()
window.config(background='black')
logo = PhotoImage(file='alarm.gif')
frame_title=Frame(window).grid()
frame_logo=Frame(window).grid()
lab_1 = Label(frame_title, text='Alarm', bg='black', fg='white', font=('Times', 28, 'bold')).grid(column=73, row=0,padx=30)
lab_2 = Label(frame_logo, bg='black', image=logo).grid(column=300, row=0)
lab_3 = Label(window, text='Hours', bg='black', fg='white', font=('Comic', 12, 'bold')).grid(column=60, row=130,padx=30)
lab_4 = Label(window, text='Minutes', bg='black', fg='white', font=('Comic', 12, 'bold')).grid(column=74, row=130)

# Alarm class
class Alarm:
    alarm_id = 1

    def __init__(self, hours, minutes, ampm, sound_file):
        self.sound_file = sound_file
        # Convert hours, minutes, ampm to a timestamp
        # Save time as a timestamp
        t = time.localtime()
        t = time.strptime(f"{t.tm_year}-{t.tm_mon}-{t.tm_mday} {hours} {minutes} {ampm}", "%Y-%m-%d %I %M %p")
        self.alarm_time = time.mktime(t)
        # Number of seconds to snooze
        self.snooze_time = None
        self.completed = False   # Set to True after alarm has gone off
        self.id = Alarm.alarm_id
        Alarm.alarm_id += 1

    # Every time this is called, it checks the time to see if the alarm should go off
    def check_time(self, cur_time):
        # Use alarm time or snooze time?
        on_time = self.snooze_time if self.snooze_time else self.alarm_time
        # Since might not be called when seconds is 0, check if it is with one minute of alarm time
        time_diff = cur_time - on_time
        if not self.completed and time_diff >= 0 and time_diff < 60:
            self.completed = True
            alarm_ringtone = pygame.mixer.music.load(self.sound_file)
            pygame.mixer.music.play()
        # Reset after 30 minutes - add 24 hours (daily timer)
        elif self.completed and time_diff > 1800 and time_diff < 1860:
            self.completed = False
            self.snooze_time = None
            self.alarm_time += 24 * 60 * 60

    def snooze(self, minutes):
        if self.completed and pygame.mixer.music.get_busy():
            self.snooze_time = time.time() + (minutes * 60)
            self.completed = False
            pygame.mixer.music.stop()

    # Convert to string for printing
    def __str__(self):
        id_str = f"[{self.id}]: "
        if self.completed:
            return id_str + ("Alarm in progress" if pygame.mixer.music.get_busy() else "Alarm completed")
        elif self.snooze_time:
            time_left = int(self.snooze_time - time.time())
            minutes = time_left // 60
            seconds = time_left % 60
            if minutes:
                return id_str + f"Snoozing for {minutes} minutes and {seconds} seconds"
            else:
                return id_str + f"Snoozing for {seconds} seconds"
        else:
            return id_str + f"Alarm set for {time.ctime(self.alarm_time)}"

# This list holds all alarms
all_alarms = []

# Tell all alarms to check the time
def check_alarms():
    now = time.time()
    for alarm in all_alarms:
        print(f"Checking: {alarm}");
        alarm.check_time(now)
    # Call again after 1 second
    window.after(1000, check_alarms)

# Creates a single object of the Alarm class
# Uses values from the option controls
def create_alarm():
    hours = int(hrs_opt_ctrl.get())
    minutes = int(min_opt_ctrl.get())
    ampm = tme_ctrl.get()
    alarm = Alarm(hours, minutes, ampm, "sound_file.mp3")
    all_alarms.append(alarm)
    print(f"Adding: {alarm}");

# Snoozes all active alarms for 2 minutes
def snooze_current():
    for alarm in all_alarms:
        alarm.snooze(2)

frame_but=Frame(window).grid()
but = Button(frame_but, text='Set Alarm', font=('Comic',11,'bold'), command=create_alarm).grid(column=60, row=280,padx=20,pady=30,columnspan=15)
snooze = Button(frame_but, text='Snooze', font=('Comic',11,'bold'), command=snooze_current).grid(column=76, row=280,padx=20,pady=30)
exit = Button(frame_but,text='Exit',font=('Comic', 11, 'bold'),command=window.destroy).grid(column=150,row=280,padx=20,pady=30)
opt_hrs = []
opt_min = []
opt_tme = ('AM','PM')
for i in range(1,13):
    opt_hrs.append(i)
for j in range(0,60):
    opt_min.append(j)

hrs_opt_ctrl = StringVar()
min_opt_ctrl = StringVar()
tme_ctrl = StringVar()
hrs_lab = OptionMenu(window, hrs_opt_ctrl, *opt_hrs).grid(column=60, row=130, columnspan=15,padx=20)
min_lab = OptionMenu(window, min_opt_ctrl, *opt_min).grid(column=76, row=130, columnspan=15,padx=20)
tme_lab = OptionMenu(window, tme_ctrl, *opt_tme).grid(column=150, row=130,padx=20)

# Fill with default values of current time
hrs_opt_ctrl.set(str(int(time.strftime('%I'))))
min_opt_ctrl.set(str(int(time.strftime('%M'))))
tme_ctrl.set(time.strftime('%p'))

check_alarms()
window.mainloop()