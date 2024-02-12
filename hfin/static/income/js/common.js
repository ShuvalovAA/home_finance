function get_token(){
    token = document.getElementById('csrf_token').innerHTML
    return token
}

function get_incomes(){
    $.ajax({
        url: '/reporter/get_income',         /* Куда пойдет запрос */
        method: 'POST',             /* Метод передачи (post или get) */
        dataType: 'json',
        headers: {'X-CSRFToken':get_token()},         /* Тип данных в ответе (xml, json, script, html). */
        data: {
            'csrftoken':get_token(),
            'user_id': 1,
            'start_period': '2020-01-01',
            'end_period': '2030-01-01'
        },     /* Параметры передаваемые в запросе. */
        success: function(data){   /* функция которая будет выполнена после успешного запроса.  */
        result = data;            /* В переменной data содержится ответ от index.php. */
        }
    });
}

function get_expenses(){
    $.ajax({
        url: '/reporter/get_expense',         /* Куда пойдет запрос */
        method: 'POST',             /* Метод передачи (post или get) */
        dataType: 'json',
        headers: {'X-CSRFToken':get_token()},         /* Тип данных в ответе (xml, json, script, html). */
        data: {
            'csrftoken':get_token(),
            'user_id': 1,
            'start_period': '2020-01-01',
            'end_period': '2030-01-01'
        },     /* Параметры передаваемые в запросе. */
        success: function(data){   /* функция которая будет выполнена после успешного запроса.  */
        result = data;            /* В переменной data содержится ответ от index.php. */
        }
    });
}


function create_dashbord(){
    const ctx = document.getElementById("chart").getContext('2d');
    incomes = get_incomes()
    incomes = get_expenses()
    const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: ["2023-05", "2023-25"],
          datasets: [{
            label: 'Доходы',
            backgroundColor: '#324512',
            borderColor: 'rgb(47, 128, 237)',
            data: [300, 400],
          },{
              label: 'Расходы',
              backgroundColor: '#deb99b',
              borderColor: 'rgb(47, 128, 237)',
              data: [300, 400],
            }]
        },
        options: {
          scales: {
            yAxes: [{
              ticks: {
                beginAtZero: true,
              }
            }]
          }
        },
      });
}

window.addEventListener('load', function () {
    create_dashbord()
  })

