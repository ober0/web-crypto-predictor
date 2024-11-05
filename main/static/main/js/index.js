document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', function () {
            console.log(1)
            let coin_name = btn.id
            window.location.href = '/coin/' + coin_name + '/'
        })
    })
})