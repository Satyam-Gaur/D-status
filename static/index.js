$(document).ready(function(){

    // to enable csrf authentication
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');
    //////////////////////////////////////////// end

    $("#logcan").click(function() {
        $("#username").val('');
        $("#pwd").val('');
       
    })

    

    //registration
    $('#regsub').click(function () {
        
        fd = new FormData(document.getElementById('frm2'))
        
        fetch('/register_user',{
            headers: {'X-CSRFToken': csrftoken},
            body:fd,
            method: 'POST',
        }).then(function(res){
            return res.text()
        }).then(function(res){+
            console.log(res)
        })
    })
  });