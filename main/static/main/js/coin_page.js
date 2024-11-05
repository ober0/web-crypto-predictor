document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const timeArg = btn.getAttribute('arg');
            let coin_name = document.getElementById('coin_name').innerText
            if (timeArg === '1d') {
                window.location.href = `http://localhost:8000/coin/${coin_name}/?time=1d`;
            }
            if (timeArg === '7d') {
                window.location.href = `http://localhost:8000/coin/${coin_name}/?time=7d`;
            }
            if (timeArg === '20d') {
                window.location.href = `http://localhost:8000/coin/${coin_name}/?time=20d`;
            }
        });
    });

    document.getElementById('go_predict').addEventListener('click', function () {
        document.getElementById('predict_col').innerHTML = 'Загрузка...'
        const task_id = document.getElementById('task_id').value;
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        let data = {
            'task_id': task_id
        }
        const intervalId = setInterval(() => {
            fetch(`/api/result/${task_id}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const predict = data.result.Close;
                    document.getElementById('predict_col').innerHTML = predict
                    clearInterval(intervalId);
                    console.log("Prediction received:", predict);
                }
            })
            .catch(error => {
                console.error('Error fetching prediction:', error);
            });
        }, 3000);
    });
});
