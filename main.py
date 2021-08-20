'''
Script helps to export files from the Skype
'''
import os
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path

import skpy


def setup_parser(parser) -> None:
    '''
    Argument parser
    '''
    parser.add_argument('--cropdate', type=str,
                        help='Input date like this 31.12.2001')
    parser.add_argument('--output', type=str,
                        help='Output folder for images')
    parser.add_argument('--login', type=str,
                        help='Skype login')
    parser.add_argument('--password', type=str,
                        help='Skype password')
    parser.add_argument('--chat', type=str,
                        help='Chat id')


def get_messages(chat, cropdate) -> list:
    '''
    Gets all messages from the date
    '''
    messages = []
    while True:
        message_batch = chat.getMsgs()
        for message in message_batch:
            messages.append(message)
            if message.time < cropdate:
                return messages


def only_images(messages) -> list:
    '''
    Makes list of only images
    '''
    image_messages = []
    for message in messages:
        if(isinstance(message, skpy.msg.SkypeImageMsg)
           and message.file is not None):
            image_messages.append(message)
    return image_messages


def export_images(messages, path) -> None:
    '''
    Exports images
    '''
    if os.path.isdir(path) is False:
        os.makedirs(path)

    for idx, image in enumerate(messages):
        num = str(idx + 1).rjust(3, '0')
        name = 'image_' + num + '.jpg'
        with open(Path(path) / Path(name), 'wb') as content:
            content.write(image.fileContent)


def main() -> None:
    '''
    Main finction
    '''
    parser = ArgumentParser()
    setup_parser(parser)
    args = parser.parse_args()

    skype = skpy.Skype(args.login, args.password)
    chat = skype.chats.chat(args.chat)

    cropdate = [int(elem) for elem in reversed(args.cropdate.split('.'))]
    cropdate = datetime(*cropdate)

    messages = get_messages(chat, cropdate)
    messages = only_images(messages)

    export_images(messages, args.output)


if __name__ == '__main__':
    main()
