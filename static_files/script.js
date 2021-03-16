const end_time = document.getElementById('end-time')
const countdown = document.getElementById('countdown')
const start_time = document.getElementById('start-time')


function timer(url) {
    setInterval(() => {
        const now = new Date().getTime()
        const time_left = Date.parse(end_time.textContent)
        const difference = time_left - now
        const minutes = Math.floor((time_left / (1000 * 60) - (now / (1000 * 60))) % 60)
        let seconds = Math.floor((time_left / (1000) - (now / (1000))) % 60)
        seconds = seconds < 10 ? '0' + seconds : seconds
        seconds = seconds == 60 ? '00' : seconds
        if (difference > 0) {
            countdown.innerHTML = minutes + ":" + seconds
        }
        else {
            var cells = document.getElementsByClassName("rb")
            for (var i = 0; i < cells.length; i++) {
                cells[i].disabled = true;
                countdown.innerHTML = 'Time Over'
                location.href = url
            }
        }


    }, 1000);
}
