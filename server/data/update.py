from aqt import mw
from anki.notes import NoteId
from datetime import datetime
from data.wolfram import getAnswer

config = mw.addonManager.getConfig(__name__)

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
            answer = getAnswer(note["Query"])
            if answer != note["Answer"]:
                note["Answer"]
                note["Last Updated"] = datetime.now()
        note["Last Checked"] = datetime.now()
        unotes.append(note)

    mw.col.update_notes(unotes)


updateNotes(mw.col.find_notes('tag:SelfUpdate'))