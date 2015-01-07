### we prepend t_ to tablenames and f_ to fieldnames for disambiguity


########################################
db.define_table('t_room',
    Field('f_name', type='integer', notnull=True, unique=True,
          label=T('Room No')),
    Field('f_is_a_lab', type='boolean',
          label=T('Is A Lab ?')),
    Field('f_capacity', type='integer',
          label=T('Capacity')),
    auth.signature,
    format='%(f_name)s %(f_is_a_lab)s %(f_capacity)s',
    migrate=settings.migrate)
db.t_room.f_name.requires = IS_NOT_EMPTY()
db.t_room.f_name.requires = IS_NOT_IN_DB(db,db.t_room.f_name)
db.define_table('t_room_archive',db.t_room,Field('current_record','reference t_room',readable=False,writable=False))

########################################
db.define_table('t_slot',
    Field('f_room', type='reference t_room',
          label=T('Room No')),
    Field('f_date', type='date',
          label=T('Date')),
    Field('f_start_time', type='time',
          label=T('Start Time')),
    Field('f_stop_time', type='time',
          label=T('Stop Time')),
    auth.signature,
    format='%(f_room)s %(f_date)s %(f_start_time)s %(f_stop_time)s',
    migrate=settings.migrate)

db.t_slot.f_room.requires = IS_IN_DB(db,db.t_room.id,'%(f_name)s %(f_is_a_lab)s %(f_capacity)s')
db.define_table('t_slot_archive',db.t_slot,Field('current_record','reference t_slot',readable=False,writable=False))

########################################
db.define_table('t_speaker',
    Field('f_name', type='string', notnull=True,
          label=T('Name')),
    Field('f_subtitle', type='string',
          label=T('Subtitle')),
    Field('f_web', type='string',
          label=T('Website')),
    Field('f_bio', type='text',
          label=T('Bio')),
    auth.signature,
    format='%(f_name)s %(f_subtitle)s',
    migrate=settings.migrate)

db.t_speaker.f_name.requires = IS_NOT_EMPTY()
db.t_speaker.f_web.requires = IS_URL()
db.define_table('t_speaker_archive',db.t_speaker,Field('current_record','reference t_speaker',readable=False,writable=False))

########################################

db.define_table('t_category',
                Field('f_category', 'string', label=T('Category')),
                format='%(f_category)s',
                migrate=settings.migrate)
db.define_table('t_category_archive',db.t_category,Field('current_record','reference t_category',readable=False,writable=False))

########################################
db.define_table('t_talk',
    Field('f_title', type='string', notnull=True,
          label=T('Title')),
    Field('f_speaker', type='reference t_speaker',
          label=T('Speaker')),
    Field('f_slot', type='reference t_slot', unique=True,
          label=T('Slot')),
    Field('f_category', type='reference t_category', label=T('Category')),
    Field('f_description', type='text',
          label=T('Description')),
    Field('f_resource', type='upload',
          label=T('Resource')),
    auth.signature,
    format='%(f_speaker)s %(f_title)s',
    migrate=settings.migrate)

db.t_talk.f_slot.requires = IS_NOT_IN_DB(db,db.t_talk.f_slot)
db.t_talk.f_category.requires = IS_IN_DB(db,db.t_category.id,'%(f_category)s')
db.t_talk.f_slot.requires = IS_IN_DB(db,db.t_slot.id,'%(f_room)s %(f_date)s %(f_start_time)s %(f_stop_time)s')
db.define_table('t_talk_archive',db.t_talk,Field('current_record','reference t_talk',readable=False,writable=False))
########################################

db.define_table('t_attendance',
                Field('f_talk_id', 'reference t_talk', label=T('Talk')),
                Field('f_user_id', 'reference auth_user', label=T('User')),
                Field('f_attending', 'string', length=5, label=T('Whether Attending ?')),
                auth.signature,
                format='%(f_talk_id)s %(f_user_id)s %(f_attending)s',
                migrate=settings.migrate)

db.t_attendance.f_talk_id.requires = IS_IN_DB(db,db.t_talk.id,'%(f_speaker)s %(f_title)s')
db.t_attendance.f_user_id.requires = IS_IN_DB(db,db.auth_user.id,'%(first_name)s %(last_name)s')
db.define_table('t_attendance_archive',db.t_attendance,Field('current_record','reference t_attendance',readable=False,writable=False))
