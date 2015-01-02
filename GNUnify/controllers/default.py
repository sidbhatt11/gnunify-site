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
    for talk in talks:
        talk.count = db((db.t_attendance.f_talk_id == talk.id) & (db.t_attendance.f_attending == "yes")).count()
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
    talk.count = db((db.t_attendance.f_talk_id == talk.id) & (db.t_attendance.f_attending == "yes")).count()
    if auth.is_logged_in():
        user.name = "%s %s" % (auth.user.first_name, auth.user.last_name)
        user.altstr = "Changed your mind ?"
        x = db.t_attendance( (db.t_attendance.f_talk_id == talk.id) & (db.t_attendance.f_user_id == auth.user.id) )
        if x:
            if x.f_attending == "yes":
                user.str = "You are going."
            elif x.f_attending == "no":
                user.str = "You are not going."
            elif x.f_attending == "maybe":
                user.str = "You may be going."
            else:
                user.str = "You haven't decided yet."
                user.altstr = "Are you going ?"
        else:
            user.str = "You haven't decided yet."
            user.altstr = "Are you going ?"
    else:
        user.name = ""
        user.str = ""
        user.altstr = ""
    return dict(talk=talk, user=user)

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

def action():
    if not request.args:
        redirect(URL('index'))
    talkid = request.args[0]
    userid = request.args[1]
    choice = request.args[2]
    db.t_attendance.update_or_insert((db.t_attendance.f_talk_id == talkid) & (db.t_attendance.f_user_id == userid), f_talk_id=talkid, f_user_id=userid, f_attending=choice)
    db.commit()
    redirect(URL('show_talk',args=[talkid]))

@auth.requires_login()
def talks_attending():
    talks_attending = db((db.t_attendance.f_user_id == auth.user.id) & (db.t_attendance.f_attending == "yes")).select(db.t_talk.ALL, left=db.t_talk.on(db.t_talk.id==db.t_attendance.f_talk_id))
    for talk in talks_attending:
        talk.count = db((db.t_attendance.f_talk_id == talk.id) & (db.t_attendance.f_attending == "yes")).count()
    return dict(talks_attending=talks_attending)

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

@auth.requires_membership('manager')
def attendance_manage():
    form = SQLFORM.smartgrid(db.t_attendance,onupdate=auth.archive)
    return locals()

@auth.requires_login()
def send_mail():
    talks = db((db.t_attendance.f_user_id == auth.user.id) & (db.t_attendance.f_attending == "yes")).select(db.t_talk.ALL, left=db.t_talk.on(db.t_talk.id==db.t_attendance.f_talk_id), orderby=db.t_talk.f_slot)
    content ="<html><body><h2>Hi %s !</h2><p>Here is your GNUnify 2015 schedule :</p><p><ul>" % auth.user.first_name
    for talk in talks:
        content+="<li><h4>%s</h4><h4>by %s</h4><h4>on %s From %s To %s in %s</h4></li>" % (talk.f_title, talk.f_speaker.f_name, talk.f_slot.f_date, talk.f_slot.f_start_time, talk.f_slot.f_stop_time, talk.f_slot.f_room.f_name)
    content += "</ul></p><h3>Venue:</h3><p>Symbiosis Institute Of Computer Studies and Research,<br>Atur Centre,<br>Near Gokhale Cross Road,<br>Model Colony, Shivajinagar,<br>Pune, Maharashtra 411016<br>Contact : 020 2567 5601<br>Website: http://sicsr.ac.in</p><p>See you at GNUnify 2015 !<br>Team GNUnify<br>http://gnunify.in</p></body></html>"
    mail.send(to=[auth.user.email],
          subject='Your GNUnify Schedule',
          # If reply_to is omitted, then mail.settings.sender is used
          #reply_to='us@example.com',
          message=content)
    session.flash = T('Mail sent !')
    redirect(URL('talks_attending'))

@auth.requires_login()
def get_ics():
    import datetime
    response.view = 'default/get_ics.ics'
    talks = db((db.t_attendance.f_user_id == auth.user.id) & (db.t_attendance.f_attending == "yes")).select(db.t_talk.ALL, left=db.t_talk.on(db.t_talk.id==db.t_attendance.f_talk_id), orderby=db.t_talk.f_slot)
    for talk in talks:
        talk.title = talk.f_title
        talk.start_datetime = datetime.datetime.combine(talk.f_slot.f_date, talk.f_slot.f_start_time)
        talk.stop_datetime = datetime.datetime.combine(talk.f_slot.f_date, talk.f_slot.f_stop_time)
    return dict(talks=talks, title='GNUnify 2015',link='http://gnunify.in',timeshift=0)
