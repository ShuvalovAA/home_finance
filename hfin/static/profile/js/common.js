/*
добавить валидацию при добавлении
скачать
Логотип Finance Planner
Дизайн подшаманить
*/

function get_user_id() {
  user_id_div = document.getElementById('user_id')
  return user_id_div.textContent
}
function get_token() {
token = document.getElementById('csrf_token').innerHTML
return token
}

/*Дашборд */
function get_first_laste_date_this_month() {
    var date = new Date();
    var firstDay = new Date(date.getFullYear(), date.getMonth(), 1);
    var lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0, 23, 59, 59);
    UTC_CODE  = date.getTimezoneOffset() * (-1) / 60
    firstDay = firstDay.toISOString().split('T')[0]
    lastDay = lastDay.toISOString().split('T')[0]
    return [firstDay, lastDay]
  }

function create_dashbord(data) {

    canvas_el = document.getElementById('chart')
    canvas_el.remove()
    canvas_el_new = document.createElement('canvas')
    canvas_el_new.style.width = '600px'
    canvas_el_new.style.height = '300px'
    canvas_el_new.id = 'chart'
  
    conteiner_chart = document.getElementById('conteiner_chart')
    conteiner_chart.append(canvas_el_new)
  
    const ctx = canvas_el_new.getContext('2d');
    incomes = data.incomes.incomes
    expense = data.expense.expenses
    incomes_dict = {}
    for(i in incomes){
      incomes_dict[incomes[i][0]] = incomes[i][1]
    }
  
    expense_dict = {}
    for(i in expense){
      expense_dict[expense[i][0]] = expense[i][1]
    }
  
    for(i in incomes_dict){
      expense_on_date = expense_dict[i]
      if(!expense_on_date){
          expense_dict[i] = 0
      }
    }
    for(i in expense_dict){
      income_on_date = incomes_dict[i]
      if(!income_on_date){
          incomes_dict[i] = 0
      }
    }
  
    sorted_keys_income = Object.keys(incomes_dict).sort()
    income_dict_result = {}
    for(i in sorted_keys_income){
      income_dict_result[sorted_keys_income[i]] = incomes_dict[sorted_keys_income[i]]
    }
  
    sorted_keys_expense = Object.keys(expense_dict).sort()
    expense_dict_result = {}
    for(i in sorted_keys_expense){
      expense_dict_result[sorted_keys_expense[i]] = expense_dict[sorted_keys_expense[i]]
    }
  
    dts = sorted_keys_expense
    incomes_amount_list = Object.values(income_dict_result)
    expenses_amount_list = Object.values(expense_dict_result)
  
  
    const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: dts,
            datasets: [{
                label: 'Доходы',
                backgroundColor: '#324512',
                borderColor: 'rgb(47, 128, 237)',
                data: incomes_amount_list,
            }, {
                label: 'Расходы',
                backgroundColor: '#deb99b',
                borderColor: 'rgb(47, 128, 237)',
                data: expenses_amount_list,
            }]
        },
        options: {
                title: {
                    display: true,
                    text: 'Информация на текущий месяц', 
                    color: 'dark',
                    font: {
                        weight: 'bold',
                        size: 24
                    }
                },
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

function get_expenses(incomes, start, end) {
    $.ajax({
        url: '/reporter/get_expense',
        method: 'POST',
        dataType: 'json',
        headers: {
            'X-CSRFToken': get_token()
        },
        data: {
            'user_id': get_user_id(),
            'start_period': start,
            'end_period': end
        },
        success: function(data) {
            data = {
                'incomes': incomes,
                'expense': data
            }
            create_dashbord(data)
        }
    });
  }

function get_incomes(start, end) {
    $.ajax({
        url: '/reporter/get_income',
        method: 'POST',
        dataType: 'json',
        headers: {
            'X-CSRFToken': get_token()
        },
        data: {
            'user_id': get_user_id(),
            'start_period': start,
            'end_period': end
        },
        success: function(data) {
            get_expenses(data, start, end)
        }
    });
  }

function set_data_for_dashboard(start = null, end = null) {
    dates = get_first_laste_date_this_month()
      if (!start) {
          start = dates[0]
      }
      if (!end) {
          end = dates[1]
      }
    get_incomes(start, end)
  
  }
/*Дашборд */
//Изменить персональные данные
function change_personal_data(
    first_name, last_name, middle_name, birth_date
){
    data = {}
    if(first_name){
        data['first_name'] = first_name
    }
    if(first_name){
        data['last_name'] = last_name
    }
    if(first_name){
        data['middle_name'] = middle_name
    }
    if(first_name){
        data['birth_date'] = birth_date
    }

    if(Object.keys(data).length === 0){
        return
    }

    data['user_id'] = get_user_id()

    $.ajax({
        url: '/user/update/',
        method: 'PATCH',
        dataType: 'json',
        headers: {
            'X-CSRFToken': get_token()
        },
        data: data,
        success: function(data) {
            location.reload();
        }
    });
}
//
//Изменить персональные данные(повесить событие на кнопку)
function set_event_on_personal_change_button(){
    button = document.getElementById('change_personal_data')
    button.addEventListener('click',function(e){
        first_name = document.getElementById('PersonalDataFirstName').value
        last_name = document.getElementById('PersonalDataLastName').value
        middle_name = document.getElementById('PersonalDataMiddleName').value
        birth_date = document.getElementById('PersonalDataBirthdate').value
        empty_all = first_name == '' && last_name == '' && middle_name == '' && birth_date == ''
        if(empty_all){
            return
        }
        change_personal_data(first_name, last_name, middle_name, birth_date)
    })
}
//



/*PUBLIC*/
window.addEventListener('load', function() {
    set_event_on_personal_change_button()
    set_data_for_dashboard()
})