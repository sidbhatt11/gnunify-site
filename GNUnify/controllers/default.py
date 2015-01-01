# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
    return dict()

def talks():
    talks = db(db.t_talk).select()
    return dict(talks=talks)

def speakers():
    speakers = db(db.t_speaker).select(orderby=db.t_speaker.id)
    return dict(speakers=speakers)


def faq():
    return dict()


def contact_us():
    return dict()

def error():
    return dict()

def show_talk():
    if not request.args:
        redirect(URL('index'))
    talkid = request.args[0]
    talk = db(db.t_talk.id == talkid).select().first()
    if talk == None:
        session.flash="No such Talk exists !"
        redirect(URL('talks'))
    return dict(talk=talk)

def show_speaker():
    if not request.args:
        redirect(URL('index'))
    speakerid = request.args[0]
    speaker = db(db.t_speaker.id == speakerid).select().first()
    if speaker == None:
        session.flash="No such speaker exists !"
        redirect(URL('speakers'))
    talksbyspeaker = db(db.t_talk.f_speaker == speaker).select()
    return dict(speaker=speaker,talksbyspeaker=talksbyspeaker)

@auth.requires_membership('manager')
def speaker_manage():
    form = SQLFORM.smartgrid(db.t_speaker,onupdate=auth.archive)
    return locals()

@auth.requires_membership('manager')
def room_manage():
    form = SQLFORM.smartgrid(db.t_room,onupdate=auth.archive)
    return locals()

@auth.requires_membership('manager')
def slot_manage():
    form = SQLFORM.smartgrid(db.t_slot,onupdate=auth.archive)
    return locals()

@auth.requires_membership('manager')
def talk_manage():
    form = SQLFORM.smartgrid(db.t_talk,onupdate=auth.archive)
    return locals()
