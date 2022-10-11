document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector("#compose-form").onsubmit = () => {
    fetch("/emails", {
      method: "POST",
      body: JSON.stringify({
        "recipients": document.querySelector('#compose-recipients').value,
        "subject": document.querySelector('#compose-subject').value,
        "body": document.querySelector('#compose-body').value
      })
    })
    .then(function(response) {return(response.json())})
    .then(result => {
        // Print result
        console.log(result);
        if (result.error) {
          console.log(result.error);
          document.querySelector('#email-error').style.display = 'block';
          document.querySelector('#error-message').innerText = result.error
          document.querySelector('#email-success').style.display = 'none';
        }
        else {
          console.log(result)
          load_mailbox('sent')
          document.querySelector('#email-error').style.display = 'none';
          document.querySelector('#email-success').style.display = 'block';
        }
      })
    return false
  }

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(email = null) {

  // Show compose view and hide other views
  document.querySelector('#inbox-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-error').style.display = 'none';
  document.querySelector('#email-success').style.display = 'none';

  // If function is provided with email object, prepopulate fields
  if (email) {
    document.querySelector('#compose-recipients').value = email.sender
    document.querySelector('#compose-subject').value = `Re: ${email.subject}`
    document.querySelector('#compose-body').value = ` \n \n On ${email.timestamp}, ${email.sender} wrote: \n ${email.body}`
  }

  // If no argument is provided clear out composition fields
  else {
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  }
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#inbox-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-error').style.display = 'none';
  document.querySelector('#email-success').style.display = 'none';
  let inbox_view = document.querySelector('#inbox-view')
  // Show the mailbox name and clears out the previous emails
  document.querySelector('#inbox-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`emails/${mailbox}`).then(response => response.json())
  .then(mailbox=> {
      for (email of mailbox) {
        let email_box = document.createElement("div")
        let email_sender = document.createElement("div")
        let email_subject = document.createElement("div")
        let email_time = document.createElement("div")
        email_sender.innerHTML= `<strong>From:</strong> ${email.sender}`
        email_time.innerHTML= `<strong>Timestamp:</strong> ${email.timestamp}`
        email_subject.innerHTML= `<strong>Subject:</strong> ${email.subject}`
        let mail_id = parseInt(email.id)
        email_box.addEventListener("click", ()=> {
          load_email(mail_id)
          console.log(mail_id)
        })
        email_box.append(email_sender, email_time, email_subject)
        email_box.classList.add("p-3", "mb-2", "bg-light", "text-dark", "border", "email-box")
        inbox_view.appendChild(email_box)
      }
  })

  function load_email(email_id) {
    let email_view = document.querySelector("#email-view")
      // Show the email and hide other views
    email_view.innerHTML = ""
    // clear the email_view of any previous emails
    document.querySelector('#inbox-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-error').style.display = 'none';
    document.querySelector('#email-success').style.display = 'none';
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
      let email_time = document.createElement("div")
      let archive_button = document.createElement("button")
      let reply_button = document.createElement("button")
      email_sender.innerHTML= `<strong>From:</strong> ${email.sender}`
      email_time.innerHTML= `<strong>Timestamp:</strong> ${email.timestamp}`
      email_subject.innerHTML= `<strong>Subject:</strong> ${email.subject}`
      email_body.innerText = email.body
      email_body.classList.add("p-3", "mb-2", "bg-light", "text-dark", "border")
      archive_button.classList.add("btn", "btn-sm", "btn-outline-primary")
      reply_button.classList.add("btn", "btn-sm", "btn-outline-primary")
      
      if (email.archived == false) {
        archive_button.innerText = "Archive"
        archive_button.addEventListener("click", ()=> {
          fetch(`/emails/${email_id}`, {
            method: "put",
            body: JSON.stringify({
              archived: true
              })
            }).then(response => {
              if(response.status == 204){
              load_mailbox('inbox')
              }
          })
      })
    }
      else {
        archive_button.innerText = "Unarchive"
        archive_button.addEventListener("click", ()=> {
          fetch(`/emails/${email_id}`, {
            method: "put",
            body: JSON.stringify({
              archived: false
            })
            }).then(response => {
              if(response.status == 204){
              load_mailbox('inbox')
              }
            })
        })
      }

      reply_button.innerText = "Reply"
      reply_button.addEventListener("click", ()=> {
        compose_email(email)
      })
      email_box.append(email_sender, email_time, email_subject, email_body, reply_button, archive_button)
      email_view.append(email_box)
  });
  }
}