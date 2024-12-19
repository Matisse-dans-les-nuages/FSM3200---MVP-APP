# import os
#
# path_to_images = "../../MASC_IMAGES/"
# month=os.listdir(path_to_images)
#
# path_march = path_to_images+month[0]+"/"
#
# path_april = path_to_images+month[1]+"/"
#
# march_days = os.listdir(path_march)[1:-2]
#
# april_days = os.listdir(path_april)[1:-4]
# print(april_days)
#
# condition = ".mat"
#
# for day in march_days:
#     print(day)
#     if '2021' in day:
#         day_path = os.listdir(path_march+"/"+day)
#         print(day_path)
#         for hour in day_path :
#             if "." not in hour:
#                 print(hour)
#                 hour_path = os.listdir(path_march+"/"+day+"/"+hour+"/")
#                 # print(hour_path)
#                 for file in hour_path:
#                     if condition in file:
#                         file_path = path_march+day+"/"+hour+"/"+file
#                         file_path = file_path.replace("._","")
#                         # print(file_path)
#                         try:
#                             os.remove(file_path)
#                         except:
#                             pass
#
# for day in april_days:
#     print(day)
#     if '2021' in day:
#         day_path = os.listdir(path_april+day)
#         print(day_path)
#         for hour in day_path :
#             if "." not in hour:
#                 print(hour)
#                 hour_path = os.listdir(path_april+day+"/"+hour+"/")
#                 # print(hour_path)
#                 for file in hour_path:
#                     if condition in file:
#                         file_path = path_april+day+"/"+hour+"/"+file
#                         file_path = file_path.replace("._", "")
#                         # print(file_path)
#                         try:
#                             os.remove(file_path)
#                         except:
#                             pass

import tkinter as tk


def on_key_press(event):
    # Get key information
    key_name = event.keysym
    key_char = event.char
    key_code = event.keycode

    # Display key information in the label
    info = f"Key Pressed: {key_name}\nCharacter: {key_char}\nKey Code: {key_code}"
    label.config(text=info)


# Create the main window
root = tk.Tk()
root.title("Key Press Information")

# Create a label to display key information
label = tk.Label(root, text="Press any key", font=("Helvetica", 16), padx=20, pady=20)
label.pack(expand=True)

# Bind the key press event to the window
root.bind('<KeyPress>', on_key_press)

# Start the Tkinter event loop
root.mainloop()
