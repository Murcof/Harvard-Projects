document.addEventListener('DOMContentLoaded', function() {


    //pause animations of like and unlike icons
    document.querySelectorAll('.like_icon').forEach(function(icon){
        icon.style.animationPlayState = 'paused';
    });

    document.querySelectorAll('.unlike_icon').forEach(function(icon){
        icon.style.animationPlayState = 'paused';
    });

    //call functions of changing number of post's likes and animating the like icon
    document.querySelectorAll('.like_paragraph').forEach(function(like_paragraph) {
        like_paragraph.onclick = function() {
            like_post(this.dataset.value);
            like_post_animation(this.dataset.value);
        }
    });

    //call function to edit posts
    document.querySelectorAll('.btn.btn-outline-dark.btn-sm').forEach(function(button) {
        button.onclick = function() {
            edit_post(this.dataset.value);
        }
    });

    //call functions of follow/unfollow
    document.querySelector('#unfollow_button').onclick = function() {
        follow_unfollow(this.dataset.value, true);
        this.style.display = 'none';
        let follow_button = document.querySelector('#follow_button');
        follow_button.style.display = 'block';
    };
    document.querySelector('#follow_button').onclick = function() {
        follow_unfollow(this.dataset.value, false);
        this.style.display = 'none';
        let unfollow_button = document.querySelector('#unfollow_button');
        unfollow_button.style.display = 'block';
    };


});

function follow_unfollow(profile_user, following){
    if (following == true) {
        fetch(`/unfollow/${profile_user}`, {
            method: 'DELETE'
        });
        //decrease number of followers
        let followers_count = document.querySelector('.followers_count');
        let counter = parseInt(followers_count.innerHTML);
        console.log(counter)
        counter -= 1;
        followers_count.innerHTML = counter;
    } else{
        fetch(`/follow/${profile_user}`, {
            method: 'POST'
        });
        //increase number of followers
        let followers_count = document.querySelector('.followers_count');
        let counter = parseInt(followers_count.innerHTML);
        console.log(counter)
        counter += 1;
        followers_count.innerHTML = counter;
    };
}

function send_new_post() {

    const form_content = document.querySelector('#id_content').value;

    fetch('/newpost', {
        method: 'POST',
        body: JSON.stringify({
            content: form_content
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
    });

    document.querySelector('#id_content').value = '';
}

function like_post(post_id){

    fetch(`/like_post/${post_id}`, {
        method:'PUT',
        })
        .then(response => response.json())
        .then(data => number_of_likes(data.message, post_id));
}

function number_of_likes(server_response, post_id){
    if (server_response == 'Post Unliked'){
        let number_of_likes = parseInt(document.querySelector(`#like_counter_number_${post_id}`).innerHTML)
        document.querySelector(`#like_counter_number_${post_id}`).innerHTML = number_of_likes-1
    } else if (server_response == 'Post Liked'){
        let number_of_likes = parseInt(document.querySelector(`#like_counter_number_${post_id}`).innerHTML)
        document.querySelector(`#like_counter_number_${post_id}`).innerHTML = number_of_likes+1
    } else {
        console.log('abubli')
    }
}

function like_post_animation(post_id){ //although its name this function works for like and unlike posts
    let icon = document.querySelector(`#like_icon_number_${post_id}`);
    icon.style.animationPlayState == 'running';
    if (icon.className == 'like_icon') {
        icon.classList.add('unlike_icon');
        icon.classList.remove('like_icon');
    } else {
        icon.classList.add('like_icon');
        icon.classList.remove('unlike_icon');
    }
}

function edit_post(post_id){
    //edita ai p mim pf <3
    var content_div = document.querySelector(`#postid${post_id}`);
    var post_content = content_div.getElementsByClassName("post_content")[0]; //innerText
    var like_paragraph = content_div.getElementsByClassName("like_paragraph")[0];
    var aux_parent = like_paragraph.parentNode;

    //hidding elements
    post_content.style.display = 'none';
    //content_div.querySelector("br").style.display = 'none';
    content_div.querySelectorAll("br").forEach(function(br){
       br.style.display = 'none';
    });

    const edit_button = content_div.querySelector("button");
    edit_button.style.display = 'none';

    //create form element to edit the post
    const edit_post_form = document.createElement("form");

    const form_input = document.createElement("textarea"); //input
    form_input.setAttribute('class','form-control');
    form_input.setAttribute('rows','2');
    form_input.setAttribute('maxlength','280');
    form_input.innerHTML = post_content.innerText;

    const form_submit = document.createElement("input");

    form_submit.setAttribute('type','submit');
    form_submit.setAttribute('class','btn btn-outline-dark btn-sm');

    //adding new elements to the post div
    edit_post_form.appendChild(form_input);
    edit_post_form.appendChild(form_submit);

    aux_parent.insertBefore(edit_post_form, like_paragraph);

    edit_post_form.onsubmit = () => {

        //send information to backend
        fetch(`/edit_post/${post_id}`, {
            method:'PUT',
            body: JSON.stringify({
                content: form_input.value
            })
        })
        .then(response => response.json())
        .then(data => console.log(data));

        //update the text of original post element
        post_content.innerText = form_input.value.trim();


        //hide new elements
        edit_post_form.style.display = 'none';
        //show old elements
        post_content.style.display = 'block';
        post_content.style.margin = '0';

        //add 'edited' tag
        const edited_tag = document.createElement('span');
        edited_tag.setAttribute('class','badge badge-pill badge-light');
        edited_tag.innerHTML = "Edited";
        aux_post_content = post_content.parentNode;
        aux_post_content.insertBefore(edited_tag,post_content);

        //content_div.querySelector("br").style.display = 'block';
        edit_button.style.display = 'block';
        edit_button.style.display = 'inline';
        return false;
    };
}