#imports
import os

#config stuff

###do not touch unless you edit in vs code
vsc_extra_path = ""
vsc_enabled = True
vsc_path = "HTML\\HTML Game Generator"

if vsc_enabled:
    vsc_extra_path = vsc_path
###

ask_description_file_name_enabled = True

#classes
class scene():
    def __init__(self, file_name):
        self.file_name = file_name
        self.title = file_name
        self.text = None
        self.image = None
        self.image_width = None
        self.image_height = None
        self.choices = []

class choice():
    def __init__(self, title):
        self.title = title
        self.link = None

#variables
description_file_name = "game description.txt"

ask_project_directory_enabled = False

doctype = '<!DOCTYPE html>'
project_directory = None
missing_link_location = "WIP"

images_enabled = True
break_count = 5
text_size = 3
width = 900
border = 0
spacing = 0
restart_button_enabled = True

background_color = "200, 200, 200"
fill_color = "100, 100, 100"
text_color = "black"

scenes = []

#methods
def process_description_file():
    description_file = open(get_description_file_path())
    description = description_file.readlines()
    description_file.close()

    current_scene = None
    current_choice = None

    for line in description:
        line = line.replace("\n", "")

        #comments or empty lines
        if(line.replace(" ", "") == "" or (line.__contains__("/") and line.split("/")[0].replace(" ", "") == "")):
            continue

        #config
        elif len((line.split("="))) >= 2:
            first_part = (line.split("=")[0]).strip(" ")
            second_part = line.split("=")[1].strip(" ")

            while second_part[0] == " ":
                second_part = second_part[1:]

            if(first_part == "doctype"):
                global doctype
                doctype = second_part

            elif(first_part == "project_directory"):
                global project_directory
                project_directory = second_part

            elif(first_part == "link" and current_scene == None):
                global missing_link_location
                missing_link_location = second_part

            elif first_part == "images_enabled":
                global images_enabled
                images_enabled = to_bool(second_part)

            elif first_part == "break_count":
                global break_count
                break_count = int(second_part)

            elif first_part == "text_size":
                global text_size
                text_size = int(second_part)

            elif first_part == "width":
                global width
                width = int(second_part)

            elif first_part == "border":
                global border
                border = int(second_part)

            elif first_part == "spacing":
                global spacing
                spacing = int(second_part)

            elif first_part == "restart_enabled":
                global restart_button_enabled
                if(second_part[0].lower() == "t"):
                    restart_button_enabled = True
                else:
                    restart_button_enabled = False

            elif first_part == "background_color":
                global background_color
                background_color = second_part

            elif first_part == "fill_color":
                global fill_color
                fill_color = second_part

            elif first_part == "text_color":
                global text_color
                text_color = second_part


            elif first_part == "text":
                current_scene.text = second_part            

            elif first_part == "title":
                current_scene.title = second_part
            
            elif first_part == "image":
                current_scene.image = second_part

            elif first_part == "image_width":
                current_scene.image_width = second_part

            elif first_part == "image_height":
                current_scene.image_height = second_part

            elif first_part == "link":
                current_choice.link = second_part

        #scenes
        else:
            space_amount = 0

            while(line[0] == " "):
                line = line[1:]
                space_amount += 1
            
            if(space_amount == 0):
                if(current_scene != None):
                    if(current_choice.link == None):
                        current_choice.link = missing_link_location
                    current_scene.choices.append(current_choice)
                    current_choice = None
                    scenes.append(current_scene)
                current_scene = scene(line)

            elif(space_amount == 4):
                if(current_choice != None):
                    if(current_choice.link == None):
                        current_choice.link = missing_link_location
                    current_scene.choices.append(current_choice)
                current_choice = choice(line)
    
    if(current_choice.link == None):
        current_choice.link = missing_link_location
    current_scene.choices.append(current_choice)
    scenes.append(current_scene)

def ask_description_file_name():
    if(ask_description_file_name_enabled):
        global description_file_name
        description_file_name = input("Game Description File Name: ")

def ask_project_directory():
    global project_directory
    if(project_directory == None):
        project_directory = input("Project Directory: ")

def get_directory_path():
    return os.path.join(os.getcwd(), vsc_extra_path, project_directory)

def get_file_path(file_name):
    return os.path.join(get_directory_path(), file_name)

def get_description_file_path():
    return os.path.join(os.getcwd(), vsc_extra_path, description_file_name)

def to_bool(text):
    return text[0].lower() in ["t", "y", "r", "i"]

def ensure_project_directory_exists():
    if not os.path.exists(get_directory_path()):
        os.mkdir(get_directory_path())

def create_HTML_files():
    ensure_project_directory_exists()

    for current_scene in scenes:
        HTML_file = open(get_file_path(current_scene.file_name + ".html"), "w")

        HTML_file.write(doctype + '\n')

        HTML_file.write('<html>\n')
        HTML_file.write('<head>\n')
        HTML_file.write('  <meta content="text/html; charset=UTF-8"\n')
        HTML_file.write(' http-equiv="content-type">\n')
        HTML_file.write('  <title>' + current_scene.title + '</title>\n')
        HTML_file.write('</head>\n')

        HTML_file.write('<body\n')
        HTML_file.write(" style=" + '"' + "color: rgb(" + text_color + ");" + 'background-color: rgb(' + background_color + ');"\n')
        HTML_file.write(" alink=" + '"' + text_color + '"' + "link=" + '"' + text_color + '"' + "vlink=" + '"' + text_color +'"' + ">\n")

        HTML_file.write('<br>\n' * break_count)

        HTML_file.write('<table\n')
        HTML_file.write(' style="width: ' + str(width) +'px; height: 100px; text-align: center; margin-left: auto; margin-right: auto;"\n')
        HTML_file.write(' border="' + str(border) + '" cellpadding="2" cellspacing="' + str(spacing) + '">\n')

        HTML_file.write('  <tbody>\n')

        if current_scene.text != None:
            HTML_file.write('    <tr>\n')
            HTML_file.write('      <td style=" background-color: rgb(' + fill_color + ')" colspan="' + str(len(current_scene.choices)) + '" rowspan="1"> ' + '<big>' * text_size + current_scene.text + '</big>' + ' </td>\n')
            HTML_file.write('    </tr>\n')

        if current_scene.image != None and images_enabled:
            HTML_file.write('    <tr>\n')
            HTML_file.write('      <td style=" background-color: rgb(' + fill_color + ')" colspan="3" rowspan="1"><img style="width: ' + current_scene.image_width + 'px; height: ' + current_scene.image_height + 'px;" alt="" src="' + current_scene.image + '"></td>')
            HTML_file.write('    </tr>\n')

        HTML_file.write('    <tr>\n')
        for current_choice in current_scene.choices:
            HTML_file.write('      <td style=" background-color: rgb(' + fill_color + '); width: ' + str(int(width / len(current_scene.choices))) + 'px;"> <a style="text-decoration:none" ' + 'href="' + current_choice.link + '.html">' + '<big>' * text_size + current_choice.title + '</big>' * text_size + '</td>\n')
        HTML_file.write('    </tr>\n')

        HTML_file.write('  </tbody>')

        HTML_file.write('</table>\n')

        HTML_file.write('</body>\n')
        HTML_file.write('</html>\n')

        HTML_file.close()

#method calls
ask_description_file_name()

process_description_file()

ask_project_directory()

create_HTML_files()