import pandas as pd
import numpy as np
import os
import re
from datetime import datetime

def preprocess_sent(line):
    """
    extracts name of messenger, removes time sent and find message sent.

    :param line:
    :return: name and message

    """
    right_bracket_index = line.find(']')

    name = None
    msg = None

    if right_bracket_index != -1:
        name = line[:right_bracket_index].replace('[', ' ').strip()
        line = line[right_bracket_index + 1 : ]

        right_bracket_index = line.find(']')

        msg = line[right_bracket_index + 1 : ].strip()

    return name, msg

def cleanMessage(message):
    """
    remove english and unnecessary letters

    :param message:
    :return: cleaned_message
    """
    # leave only hangul
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')

    cleanedMessage = hangul.sub('', message).strip()

    # delete hangul 자음, 모음 삭제
    cleanedMessage = re.sub('([ㄱ-ㅎㅏ-ㅣ])+', "", cleanedMessage)

    return cleanedMessage

me = '배승학'
friend = '김지수'

with open("kakaotalk_jisoo.txt", 'r', encoding='UTF-8') as f:
    lines = f.readlines()

    speaker = ''
    msg_log = []
    msgs = ""

    # for each line, find speaker
    # if speaker does not change, same person is speaking so keep adding msg
    # if speaker has changed, change to speaker's msg
    for index, line in enumerate(lines):

        name, msg = preprocess_sent(line)
        
        if name == None:
            continue
        
        msg = cleanMessage(msg).strip()

        if msg == "":
            continue

        # if conversation just started and speaker is me, then simply pass
        if not speaker and name == me:
            pass

        # if conversation just started and speaker is my friend, start collecting data
        elif not speaker and name == friend:
            speaker = name
            msgs += msg
        elif speaker:
            # conversation started

            # if speaker has not changed
            # keep adding sentences
            if speaker == name:
                msgs += (" " + msg)

            # if speaker has changed
            # append msgs to msg_log and speaker changes
            else:
                msg_log.append(msgs)
                msgs = msg
                speaker = name

# append last chat
msg_log.append(msgs)

# create source and target iter
source_iter = (msg.strip() for index, msg in enumerate(msg_log) if index % 2 == 0)
target_iter = (msg.strip() for index, msg in enumerate(msg_log) if index % 2 == 1)


# save source_iter to source.txt
with open('source_test.txt', 'w') as f:
    for msg in source_iter:
    #     if msg == "":
    #         pass
    #     else:
        f.write(msg + "\n")

with open('target_test.txt', 'w') as f:
    for msg in target_iter:
    #     if msg == "":
    #         pass
    #     else:
        f.write(msg + "\n")