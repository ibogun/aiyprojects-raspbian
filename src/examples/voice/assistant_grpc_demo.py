#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo of the Google Assistant GRPC recognizer."""

import logging

import aiy.assistant.grpc
import aiy.audio
import aiy.voicehat
import google_sheets

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)


def process_text(editor, text):
    print('You said "', text, '"')
    if text == 'goodbye':
        status_ui.status('stopping')
        print('Bye!')
        return True

    if text == 'options':
        aiy.audio.say("Options are:")
        aiy.audio.say("add feeding")
        aiy.audio.say("stop feeding")
        aiy.audio.say("dirty diaper")
        aiy.audio.say("wet diaper")
        return True

    if text == 'add feeding':
        aiy.audio.say("Recorded add feeding.")
        editor.add_start_feeding()
        return True

    if text == 'stop feeding':
        aiy.audio.say("Recorded stop feeding.")
        editor.add_end_feeding()
        return True

    if text == 'dirty diaper':
        aiy.audio.say("Recorded dirty diaper.")
        editor.add_pooping()
        return True

    if text == 'wet diaper' or text == 'what diaper':
        aiy.audio.say("Recorded wet diaper.")
        editor.add_peeing()
        return True

    return False


def main():
    status_ui = aiy.voicehat.get_status_ui()
    status_ui.status('starting')
    assistant = aiy.assistant.grpc.get_assistant()
    button = aiy.voicehat.get_button()

    editor = google_sheets.SpreadSheetEditor()
    with aiy.audio.get_recorder():
        while True:
            status_ui.status('ready')
            print('Press the button and speak')
            button.wait_for_press()
            status_ui.status('listening')
            print('Listening...')
            text, audio = assistant.recognize()
            if text:
                aiy.audio.say(text)
                status = process_text(editor, text)
                if not status:
                    aiy.audio.say("Did not understand. Try again.")


if __name__ == '__main__':
    main()
