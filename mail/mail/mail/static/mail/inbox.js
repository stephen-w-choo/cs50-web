document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector("#compose-form").onsubmit = () => {
    fetch("/emails", {
      method: "POST",
      body: JSON.stringify( {
        "recipients": document.querySelector('#compose-recipients').value,
        "subject": document.querySelector('#compose-subject').value,
        "body": document.querySelector('#compose-body').value
      }).then(response => response.json())
      .then(result => {
          // Print result
          console.log(result);
      })
    })
    return(false)
  }

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#inbox-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#inbox-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  let inbox_view = document.querySelector('#inbox-view')
  // Show the mailbox name
  document.querySelector('#inbox-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`emails/${mailbox}`).then(response => response.json())
  .then(mailbox=> {
      for (email of mailbox) {
        let email_box = document.createElement("div")
        let email_sender = document.createElement("div")
        let email_subject = document.createElement("div")
        let email_time = document.createElement("div")
        email_sender.innerText= email.sender
        email_subject.innerText= email.subject
        email_time.innerText = email.timestamp
        email_box.addEventListener("click", ()=> {
          load_email(email.id)
        })
        email_box.append(email_sender, email_subject, email_time)
        inbox_view.appendChild(email_box)
      }
  })

  function load_email(email_id) {
    let email_view = document.querySelector("#email-view")
      // Show the email and hide other views
  document.querySelector('#inbox-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  fetch(`/emails/${email_id}`).then(response => response.json())
    .then(email => {
      fetch(`/emails/${email_id}`, {
        method: "put",
        body: JSON.stringify({
          read: true
        })
      })
      console.log(email)
      let email_box = document.createElement("div")
      let email_sender = document.createElement("div")
      let email_subject = document.createElement("div")
      let email_body = document.createElement("div")
      let archive_button = document.createElement("button")
      email_sender.innerText= email.sender
      email_subject.innerText= email.subject
      email_body.innerText = email.body
      archive_button.innerText = "Archive"
      archive_button.addEventListener("click", ()=> {
        fetch(`/emails/${email_id}`, {
          method: "put",
          body: JSON.stringify({
            archived: true
          })
        })
      })
      email_box.append(email_sender, email_subject, email_body, archive_button)
      email_view.append(email_box)
  });
  }
}