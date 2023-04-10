function editPost(id) {
  // get the post content
  // get this specific edit, save buttons and forms in this block
  let postText = document.getElementById(id);
  let editButton = document.getElementById(`edit-${id}`);

  editButton.addEventListener('click', () => {
    // hide the edit button
    editButton.style.display = 'none';
    // replace the card-text area with the form
    let postContent = postText.innerText;
    postText.style.display='none';
    const saveButton = document.getElementById(`save-${id}`);
    const form = document.getElementById(`form-${id}`);
    form.style.display = 'block';

    saveButton.addEventListener('click', () => {
      // prevent the form from refreshing the page
      event.preventDefault();
      // disable the save button
      saveButton.disabled = true;
      // make a request to the server to save the post
      let formData = new FormData(form);
      fetch(`/posts/${id}`, {
        method: 'POST',
        body: formData
      })
      // await server response, then update the card-text area with the new content
      .then(response => response.json())
      .then(result => {
        console.log(result);
        postText.innerHTML = result.content;
        form.value = result.content;
        // enable the save button
        saveButton.disabled = false;
        // hide the form
        form.style.display = 'none';
        // show the edit button and text
        editButton.style.display = 'block';
        postText.style.display = 'block';
      });
    });
  });
}


function likePost(id) {
  // get the like button
  let likeButton = document.getElementById(`like-${id}`);
  let likeCount = document.getElementById(`like-count-${id}`);

  likeButton.addEventListener('click', () => {
    // make a request to the server to like the post
    fetch(`/posts/${id}/like`, {
      method: 'GET'
    })
    .then(response => response.json())
    .then(result => {
      console.log(result);
      // update the like button
      if (likeButton.innerText == "Like") {
        likeButton.innerText = "Unlike";
      } else {
        likeButton.innerText = "Like";
      }
      // update the like count
      likeCount.innerText = result.likes;
    });
  });
}
