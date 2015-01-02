gnunify-site
============

A web2py app that helps with the management of gnunify-like event and also serves as a website.

This is a work-in-progress and still in beta. Many functionalities yet to be added. If you want to contribute or want the complete list of features, let me know at :
sidbhatt11@yahoo.in

You can find me online at :
www.siddharthbhatt.com

========================================================

Update 3/1/15:
Added:
- 'My participation' view for users
- Ability to mail users their individual schedule for GNUnify
- Ability to export .ics files of users' individual schedule for GNUnify
- Recaptcha for user registration

Important Instructions : 
After uploading w2p file and creating new application: 
- edit 0.py and set-up your own SMTP settings. Mailing feature won't work otherwise.
- register with recaptcha (https://www.google.com/recaptcha) if already haven't; then edit db.py and paste your public and private keys in the correct places. Recaptcha won't work otherwise.