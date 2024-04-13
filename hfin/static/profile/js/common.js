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

//формирование таблицы платажей за попдиску
function clear_table(table_body){
    children = table_body.children
        steps = children.length
        if(children.length>0){
          for (i = steps-1; i >=0 ; i--){
              table_body.removeChild(children[i])
          }
        }
        
}
function create_payments_table(data){
    
    table_body = document.getElementById('table_body_payments')
    footer = document.getElementById('payments_tfoot')
    clear_table(table_body)
    clear_table(footer)
    total_amount = 0
    total_months = 0
    for(i=0; i<data.length;i++ ){
        tr = document.createElement('tr')
        tr.id = i
        row = data[i]
        for(z=0; z < row.length; z++){
            td = document.createElement('td')
            
            td_value = row[z]
            td.textContent = td_value
            if(z==1){
                total_amount += Number(td_value)
            }
            if(z==2){
                total_months += Number(td_value)
            }
            tr.append(td)
        }
        table_body.append(tr)
    }

    tr_f = document.createElement('tr')
    td0 = document.createElement('td')
    td0.textContent = ''
    td1 = document.createElement('td')
    td1.textContent = total_amount
    td2 = document.createElement('td')
    td2.textContent = total_months
    tr_f.append(td0)
    tr_f.append(td1)
    tr_f.append(td2)
    footer.append(tr_f)

}
function get_payments(){
    $.ajax({
        url: '/payment/get/',
        method: 'GET',
        dataType: 'json',
        headers: {
            'X-CSRFToken': get_token()
        },
        data: {'user_id': get_user_id()},
        success: function(data) {
            create_payments_table(data)
        }
    });
}
//

//Перейти на сервис банка для оплаты
function send_pay_on_webhook(data){
    $.ajax({
        url: 'http://127.0.0.1:9393/payment/webhook_get_pay',
        method: 'GET',
        dataType: 'json',
        headers: {
            'X-CSRFToken': get_token()
        },
        data: data,
        success: function(data) {
            url = 'http://127.0.0.1:9393/user/'
            window.location.replace(url);
        }
    });
}
function set_event_fixutre_pay_ok(){
    id = 'fixutre_pay_ok'
    button = document.getElementById(id)
    button.addEventListener('click', function(e){
        data = {}
        data['sum'] = document.getElementById('sum').textContent
        data['good']= document.getElementById('good').textContent
        data['done'] = true
        data['user_id'] = document.getElementById('user_id').textContent
       
        send_pay_on_webhook(data)
       
    })
}

function set_event_click_for_pay(){
    button = document.getElementById('BuyGoToBank')
    url = "fixtures/bank_source?"
    cart_number = document.getElementById('BankCartNumber').value
    cvc = document.getElementById('CartCVC').value
    actvie_date = document.getElementById('ACtiveDate').value
    sum = document.getElementById('AmountPay').textContent
    good = document.getElementById('PeriodPay').value

    url += 'cart_number=' + cart_number + '&'
    url += 'cvc=' + cvc + '&' 
    url += 'actvie_date=' + actvie_date + '&' 
    url += 'sum=' + sum + '&' 
    url += 'good=' + good + '&' 
    button.addEventListener('click', function(e){
        window.location.replace(url);
    })
}
//



/*PUBLIC*/
window.addEventListener('load', function() {
    if(window.location.href == 'http://127.0.0.1:9393/user/fixtures/bank_source?'){
        set_event_fixutre_pay_ok()
    }else{
        set_event_click_for_pay()
        get_payments()
        set_event_on_personal_change_button()
        set_data_for_dashboard()
    }
})