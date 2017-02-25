#!/usr/bin/python3
from table_print import print_title, print_empty, print_left, \
    print_separator, print_end, print_enter_to_continue, print_center


# Define custom options here
def command_signs():

    # Store the sign lines here
    lines = [''] * 3

    def print_step(step):
        print_title('Command wall sign generator [{}/7]'.format(step))
        print_left('Current sign preview:')
        print_center('┌────────────────────────┐')
        print_center('│                        │')
        for line in lines:
            print_center('│{}│'.format(line.center(24)))
        print_center('└────────────────────────┘')
        print_empty()

    # Step 1: Welcome
    print_step(1)
    print_left('This assistant will guide you through the process of')
    print_left('creating a clickable wall sign which runs a command.')
    print_empty()
    print_left('A preview of the sign will appear as shown above.')
    print_left('Note that too long texts will be cropped in Minecraft!')
    print_left('And the preview will look odd.')
    print_enter_to_continue()

    # Step [2..4]: Enter line [2..4]
    for i in range(3):
        line_number = i + 2
        print_step(line_number)
        print_left('Please enter the line {} of the sign.'.format(line_number))
        print_end()
        lines[i] = input('⬜️ ')

    # Step 5: Enter command
    print_step(5)
    print_left('Please enter the command to execute.')
    print_end()
    cmd = input('⬜️ ')

    # Step 6: Enter where will it face
    facing = ''
    facing_to_int = {'north': 3, 'east': 4, 'west': 5, 'south': 6}

    print_step(6)
    print_left('Please enter to where you face to place the sign.')
    print_left('Available options are: north/east/west/south.')
    print_end()
    while facing not in facing_to_int:
        facing = input('⬜️ ')

    # Step 7: End
    print_step(7)
    print_left('The command has been generated. Steps to follow:')
    print_left('1. Ensure you can use command blocks', 3)
    print_left('2. /give @e[c=1] command_block', 3)
    print_left('3. Copy and paste (Ctrl+V) the generated command', 3)
    print_left('4. Activate the command block with redstone', 3)
    print_left('5. Right click the sign to use it', 3)
    print_empty()
    print_left('Press enter to exit the assistant.')
    print_end()

    base_command = r'/setblock ~ ~1 ~ minecraft:wall_sign {} replace {{Text1:"{{\"text\":\"\",\"clickEvent\":{{\"action\":\"run_command\",\"value\":\"{}\"}}}}",Text2:"[\"{}\"]",Text3:"[\"{}\"]",Text4:"[\"{}\"]"}}'
    print(base_command.format(facing_to_int[facing], cmd, lines[0], lines[1], lines[2]))
    input('⬜️ ')


def command_tips():
    print_title('Command tips [1/2]')
    print_left('You can use selectors for some commands. For example:')
    print_left('/tp @e[r=2,c=1,type=!Player]', 3)
    print_empty()
    print_left('Where:')
    print_left('r= Specifies radius', 3)
    print_left('c= Specifies maximum entities', 3)
    print_left('=! Negates', 3)
    print_left('type= Specifies entity type', 3)
    print_enter_to_continue()

    print_title('Command tips [2/2]')
    print_left('Types usually start by a capital letter. For example:')
    print_left('Chicken, Player, Wolf...', 3)
    print_empty()
    print_left('If you want to list all the types, enter "/summon "')
    print_left('and then press the TAB key on your keyboard.')
    print_enter_to_continue()


def about():
    print_title('About')
    print_left('This program has been made by:')
    print_left('Lonami Exo (c) LonamiWebs 2017', 3)
    print_empty()
    print_left('For more information, check:')
    print_left('https://lonamiwebs.github.io', 3)
    print_enter_to_continue()


should_quit = False


def quit_app():
    global should_quit
    should_quit = True


# Add them to an options array, with a title
options = (
    ('Generate command signs', command_signs),
    ('Display tips for commands', command_tips),
    ('About', about),
    ('Exit', quit_app)
)


# Store notes here that should be printed the next time the main menu appears
notes = ''

# Print main menu
while not should_quit:
    print_title('Minecraft Utils')

    # Check if we have pending notes
    if notes != '':
        print_left('Note: {}'.format(notes))
        notes = ''
        print_separator()

    print_left('Please enter a number to continue.')
    print_empty()

    # Print options
    index = 1
    for option, _ in options:
        print_left('{}. {}'.format(index, option), 3)
        index += 1

    print_end()
    command = input('⬜️ ')
    try:
        selected_option = int(command)
        selected_option -= 1
        if -1 < selected_option < len(options):
            options[selected_option][1]()
        else:
            notes = 'Invalid option number'

    except ValueError:
        notes = "Entered option was't an integer"


# Use this to write more tables:
'''
┌───────────┬───────────┐
│ header  1 │ header  2 │
├───────────┼───────────┤
│ content 1 │ content 2 │
└───────────┴───────────┘
'''
