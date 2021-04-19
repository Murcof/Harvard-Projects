document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  //send email
  document.getElementById('compose-form').addEventListener('submit', send); //document.querySelector('#compose-form').onsubmit = send; also works


  // By default, load the inbox
  load_mailbox('inbox');





});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#single_email').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  clear_mailbox();

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

  clear_mailbox();
  
  // Show the mailbox and hide other views
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single_email').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  show_emails(mailbox);

  event.preventDefault();
}

function show_emails(box) {
    clear_mailbox();
    document.querySelector('#single_email').style.display = 'none';
    document.querySelector('#emails-view').style.display = 'block';

    fetch(`/emails/${box}`)
    .then(response => response.json())
    .then(function(emails) {
        emails.forEach(email => {
            const link = document.createElement('a');
            link.setAttribute('class','single_email_row');

            const row = document.createElement('div'); row.setAttribute('class', 'email_row');
            const sbj = document.createElement('div'); sbj.innerHTML = email.subject;
            const sender = document.createElement('div'); sender.innerHTML = email.sender;
            const body_preview = document.createElement('div'); body_preview.innerHTML = email.body;
            const tmstmp = document.createElement('div'); tmstmp.innerHTML = email.timestamp;

            row.appendChild(sbj); row.appendChild(sender); row.appendChild(body_preview); row.appendChild(tmstmp);

            if (email.read == true) {
                row.style.backgroundColor = '#E0E0E0';
                //row.setAttribute('style','background-color: gray'); also works
            } else {
                row.style.backgroundColor = 'white';
                //row.setAttribute('style','background-color: white'); also works
            };

            link.appendChild(row);

            //load single email
            link.addEventListener('click', function() {
                read_unread(email.id, true);
                display_email(email.id);
            });

            document.querySelector('#show_emails').append(link);

        });
        });
}

function clear_mailbox() {
    const loaded_area = document.getElementById('show_emails');
    loaded_area.innerHTML = '';
    const loaded_email = document.getElementById('single_email');
    loaded_email.innerHTML = '';
}


function display_email(email_id){
    clear_mailbox();
    console.clear();

    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#single_email').style.display = 'block';

    fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(function(email) {
        //create elements of top part
        const tmstmp = document.createElement('div'); tmstmp.setAttribute('id', 'email_view_timestamp');
        tmstmp.innerHTML = email.timestamp;
        const sender = document.createElement('div'); sender.setAttribute('id','email_view_sender');
        sender.innerHTML = email.sender;

        //create archive_unarchive button
        let archive_unarchive_button = document.createElement('button');
        if (email.archived == false) {
            archive_unarchive_button.setAttribute('class',"btn btn-secondary");
            archive_unarchive_button.innerHTML = 'Archive';
        } else {
            archive_unarchive_button.setAttribute('class',"btn btn-info");
            archive_unarchive_button.innerHTML = 'Unarchive';
        }

        archive_unarchive_button.addEventListener ('click', function() {
            if (email.archived == true){
                archive_unarchive(email_id, false)
            } else {
               archive_unarchive(email_id, true)
            };
        });


        //appending the above created elements to the grid of the top part
        const top_part = document.createElement('div'); top_part.setAttribute('id', 'email_top_part');
        top_part.append(sender); top_part.append(tmstmp);

        //sent emails cannot be archived
        if (document.querySelector('h2').innerHTML != email.sender) {
            top_part.append(archive_unarchive_button);
        };


        //definnig the heading with the title
        const subj = document.createElement('h4'); subj.setAttribute('id', 'email_view_subject');
        subj.innerHTML = email.subject;

        //create the recipients element
        const recip = document.createElement('div');recip.setAttribute('id', 'email_view_recipients');
        recip.innerHTML = `To: ${email.recipients}`;

        const line = document.createElement('hr'); const brk = document.createElement('br');

        //create the body element
        const content = document.createElement('div'); content.setAttribute('id', 'email_view_content');
        content.innerHTML = email.body;

        //create reply button
        const reply_button = document.createElement('button'); reply_button.setAttribute('class', 'btn btn-success');
        reply_button.innerHTML = 'Reply';

        reply_button.addEventListener ('click', function() {
            reply(email.id);
        });

        //appending elements
        document.querySelector('#single_email').append(subj);
        document.querySelector('#single_email').append(top_part);
        document.querySelector('#single_email').append(recip);
        document.querySelector('#single_email').append(line);
        document.querySelector('#single_email').append(content); document.querySelector('#single_email').append(brk);
        document.querySelector('#single_email').append(reply_button);

        console.log(subj);

    });

}

function send() {

    const email_recip = document.querySelector('#compose-recipients').value;
    const email_subj = document.querySelector('#compose-subject').value;
    const email_body = document.querySelector('#compose-body').value;

    fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: email_recip,
        subject: email_subj,
        body: email_body
    })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    });

    load_mailbox('sent');

}

function archive_unarchive(email_id, true_false) {
    fetch(`/emails/${email_id}`, {
    method:'PUT',
    body: JSON.stringify({
      archived: true_false
    })
    });
    load_mailbox('inbox');
}

function read_unread(email_id, true_false) {
    fetch(`/emails/${email_id}`, {
    method:'PUT',
    body: JSON.stringify({
      read: true_false
  })
    });
}

function reply(email_id){

  // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#single_email').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';
    clear_mailbox();


    fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(function(email) {
        document.querySelector('#compose-recipients').value = email.sender;
        document.querySelector('#compose-body').value = '\n' + '\n' + `On ${email.timestamp} ${email.sender} wrote:\n\n${email.body}`;

        const sbj_3_first = email.subject.slice(0,4)
        if (sbj_3_first == 'Re: '){
            document.querySelector('#compose-subject').value = email.subject;
        } else {
            document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
        }
    })
}