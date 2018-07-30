$(() => {

    $('.buttonBar, .buttonBar50').on('click', (e) => {

        const url = '/' + $(e.currentTarget).attr('data-event');
        
        if (url == "/shutdown") {
            if (confirm("Shut down?")) {
                try {
                    $.getJSON(url); // Initiates shutdown immediately, so the call fails
                } catch(err) {    
                }
                alert("Shutting down");
            }
            return;
        }

        $.getJSON(url, (data) => {

            if (data != true) {
                alert('Unexpected response from server!');
            } else {

                let tmpHtml = $(e.currentTarget).find('.buttonBarContainer').html();
                $(e.currentTarget).find('.buttonBarContainer').html("<i class=\"fas fa-check\"></i>");
                setTimeout(() => {resetIcon(e.currentTarget, tmpHtml)} , 1000);

            }

        });

    });

});

function resetIcon(target, html) {
    $(target).find('.buttonBarContainer').html(html);
}