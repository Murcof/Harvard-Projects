document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('.btn.btn-outline-light.btn-sm').onclick = function() {
        random();
    };

    document.querySelector('.search_form').onsubmit = () => {
        console.log(document.querySelector('.form-control').value);
        search(document.querySelector('.form-control').value);
        return false;
    };

});

function art_api(word){
    // In this first fetch we search in the API for art pieces with the respective word in the title
    fetch(`https:${'//'}api.artic.edu/api/v1/artworks/search?q=${word}&query[match][title]=${word}`, {
        method:'GET',
        })
        .then(function (response) {
        return response.json()
        })
        .then(function (response) {
        console.log(response);
        if (response.data == '') {
            console.log('aaiiu');
            update_img_date("Sorry! We coudn't find any related Work of Art.\n =(");
            update_img_url('https://www.dpmarketingcommunications.com/wp-content/uploads/2016/11/404-Page-Featured-Image.png')
        } else{
            let title = response.data[0].title;
            update_img_title(response.data[0].title);

            // Secondly we use the first response 'api_link' in another fetch to get the image URL
            //fetch (`https:${'//'}api.artic.edu/api/v1/artworks/${response.data[0].id}`,{
            fetch(response.data[0].api_link,{
                method:'GET',
                })
                .then(function (response) {
                    return response.json()
                })
                .then(function (response) {
                console.log(response);
                console.log(response.data.artist_title);
                update_img_date(response.data.date_display);
                update_img_artist(response.data.artist_title);
                console.log(response.data.date_display);

                // This third fetch is to get the url of the art's image
                fetch(`https:${'//'}www.artic.edu/iiif/2/${response.data.image_id}/full/843,/0/default.jpg`,{
                    method:'GET',
                    })
                    .then(function(response){
                        console.log(response.url);
                        //let img_url = response.url;
                        update_img_url(response.url)
                    })
            });
        };

    });
};

function update_img_url(response_url){
    var img_element = document.querySelector('.art_image');
    img_element.setAttribute('src',response_url);
}

function update_img_title(img_title){
    var title_paragraph = document.querySelector('.img_title');
    title_paragraph.innerText = `${img_title.trim()},`;
}

function update_img_date(img_date){
    var date_paragraph = document.querySelector('.img_date');
    if (img_date == null){
        date_paragraph.innerText = 'Not dated';
    } else {
        date_paragraph.innerText = img_date.trim();
    };
}

function update_img_artist(img_artist){
    var artist_paragraph = document.querySelector('.img_artist');
    if (img_artist == null){
        artist_paragraph.innerText = 'Artist Unknown'
    } else {
        artist_paragraph.innerText = img_artist.trim();
    };
}

function random(){
    fetch('/random',{
        method:'GET'
    })
    .then(response => response.json())
    .then(function(word){ //response word
        let uuy = JSON.parse(word.word);
        console.log(uuy[0].pk); //response.word
        window.location.replace(`/${JSON.parse(word.word)[0].pk}`);
    })
}

function game(){
    fetch('/random',{
        method:'GET'
    })
    .then(response => response.json())
    .then(function(word){ //response word
        window.location.replace(`/game/${JSON.parse(word.word)[0].pk}`);
    })
}

function search(string){
    window.location.replace(`/search/${string.trim().toLowerCase()}`);
}