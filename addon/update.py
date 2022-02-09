from aqt import mw
from anki.notes import NoteId
from datetime import datetime
import requests

config = mw.addonManager.getConfig(__name__)


def updateAnswer(question: str, format: list = ['plaintext'], location: str = None, appid: str = None):
    url =  'http://Jeida456.pythonanywhere.com/query'
    params = {
        'question': question,
        'appid': appid,
        'format': ','.join(format),
        'location': location,
    }  

    r = requests.get(url, params)
    try:
        print(r.text)
    except:
        print('No result received.')

def validateNotes(nids: list[NoteId]) -> list[NoteId]:
    vnids = list()
    for nid in nids:
        note = mw.col.get_note(nid)
        fields = ['Question', 'Answer', 'Query', 'Topic', 'Notes', 'Sources', 'Last Updated', 'Last Checked']
        for field in fields:
            if field not in note:
                continue
        vnids.append(nid)
    return vnids

def updateNotes(nids):
    nids = validateNotes(nids)

    unotes = list()
    for nid in nids:
        note = mw.col.get_note(nid)
        if int(note["Last Checked"]) < datetime.now() - config["Update Interval"]:
            note["Last Checked"] = datetime.now()
            answer = updateAnswer(note["Query"])
            if answer != note["Answer"]:
                note["Answer"] = answer
                note["Last Updated"] = datetime.now()
            unotes.append(note)

    mw.col.update_notes(unotes)

updateNotes(mw.col.find_notes(f'tag:SelfUpdate' ))