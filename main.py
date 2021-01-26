#!/usr/bin/env python
import PySimpleGUI as sg
import cv2
import subprocess
import shutil
import os
import sys
# Demonstrates a number of PySimpleGUI features including:
#   Default element size
#   auto_size_buttons
#   Button
#   Dictionary return values
#   update of elements in form (Text, Input)
def runCommand(cmd, timeout=None, window=None):
    """ run shell command
	@param cmd: command to execute
	@param timeout: timeout for command execution
	@return: (return code from command, command output)
	"""

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ''
    for line in p.stdout:
        line = line.decode(errors='replace' if (sys.version_info) < (3, 5)
                           else 'backslashreplace').rstrip()
        output += line
        print(line)
        if window:
            window.Refresh()

    retval = p.wait(timeout)

    return (retval, output)


def camera():
    sg.theme('LightGreen')

    layout = [[sg.Text(' Python EXE Creator', font='Any 15')],
              [sg.Text('Source Python File'), sg.Input(key='-sourcefile-', size=(45, 1)),
               sg.FileBrowse(file_types=(("Python Files", "*.py"),))],
              [sg.Text('Icon File'), sg.Input(key='-iconfile-', size=(45, 1)),
               sg.FileBrowse(file_types=(("Icon Files", "*.ico"),))],
              [sg.Frame('Output', font='Any 15', layout=[
                  [sg.Output(size=(65, 15), font='Courier 10')]])],
              [sg.Button('Make EXE', bind_return_key=True),
               sg.Button('Quit', button_color=('white', 'firebrick3'))],
              ]

    window = sg.Window('PySimpleGUI EXE Maker', layout, auto_size_text=False, auto_size_buttons=False,
                       default_element_size=(20, 1), text_justification='right')
    # ---===--- Loop taking in user input --- #
    while True:

        event, values = window.read()
        if event in ('Exit', 'Quit', None):
            break

        source_file = values['-sourcefile-']
        icon_file = values['-iconfile-']

        icon_option = '-i "{}"'.format(icon_file) if icon_file else ''
        source_path, source_filename = os.path.split(source_file)
        workpath_option = '--workpath "{}"'.format(source_path)
        dispath_option = '--distpath "{}"'.format(source_path)
        specpath_option = '--specpath "{}"'.format(source_path)
        folder_to_remove = os.path.join(source_path, source_filename[:-3])
        file_to_remove = os.path.join(source_path, source_filename[:-3] + '.spec')
        command_line = 'pyinstaller -wF --clean "{}" {} {} {} {}'.format(source_file, icon_option, workpath_option,
                                                                         dispath_option, specpath_option)

        if event == 'Make EXE':
            try:
                print(command_line)
                print('Making EXE...the program has NOT locked up...')
                window.refresh()
                # print('Running command {}'.format(command_line))
                out, err = runCommand(command_line, window=window)
                shutil.rmtree(folder_to_remove)
                os.remove(file_to_remove)
                print('**** DONE ****')
            except:
                sg.PopupError('Something went wrong',
                              'close this window and copy command line from text printed out in main window',
                              'Here is the output from the run', out)
                print('Copy and paste this line into the command prompt to manually run PyInstaller:\n\n', command_line)






layout = [[sg.Text('Enter Your Passcode')],
          [sg.Input('', size=(10, 1), key='input')],
          [sg.Button('1'), sg.Button('2'), sg.Button('3')],
          [sg.Button('4'), sg.Button('5'), sg.Button('6')],
          [sg.Button('7'), sg.Button('8'), sg.Button('9')],
          [sg.Button('Submit'), sg.Button('0'), sg.Button('Clear')],
          [sg.Text('', size=(15, 1), font=('Helvetica', 18),
                text_color='red', key='out')],
          ]

window = sg.Window('Keypad', layout,
                   default_button_element_size=(5, 2),
                   auto_size_buttons=False,
                   grab_anywhere=False)

# Loop forever reading the form's values, updating the Input field
keys_entered = ''
while True:
    event, values = window.read()  # read the form
    if event == sg.WIN_CLOSED:  # if the X button clicked, just exit
        break
    if event == 'Clear':  # clear keys if clear button
        keys_entered = ''
    elif event in '1234567890':
        keys_entered = values['input']  # get what's been entered so far
        keys_entered += event  # add the new digit
    elif event == 'Submit':
        keys_entered = values['input']
        if values['input']=='123456':
            sg.popup('输入正确')
            camera()
        else:
             sg.popup('输入错误')
        window['out'].update(keys_entered)  # output the final string

    # change the form to reflect current key string
    window['input'].update(keys_entered)
window.close(
