
url = new URL(document.location.href);
lang = url.searchParams.get("lang");
document.getElementById("current-lang").innerHTML += lang;


async function post_data(url = '', data = {}) {
      const response = await fetch(url, {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });
      return await response.json();
}

function add_comment(){
    comment = document.getElementById("comment-text").value;

    if(comment){
        var name = "Виктор Рыжков";
        var hours_ago = "только что";
        post_data('/post_comment', {"name": name, "hours_ago": hours_ago, "comment": comment});
        document.location.reload();
    }
}

function get_search_results(){
    search_text = document.getElementById("search-text").value;
    if(search_text != ""){
        document.location = "/search?q=" + search_text;
    }
}


document.getElementById("search-button").addEventListener("click", get_search_results);
document.getElementById("comment-button").addEventListener("click", add_comment);