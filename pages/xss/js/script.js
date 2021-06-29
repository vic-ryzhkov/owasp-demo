async function post_data(url = '', data = {}) {
  // Default options are marked with *
      const response = await fetch(url, {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data) // body data type must match "Content-Type" header
      });
      return await response.json(); // parses JSON response into native JavaScript objects
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

document.getElementById("comment-button").addEventListener("click", add_comment)