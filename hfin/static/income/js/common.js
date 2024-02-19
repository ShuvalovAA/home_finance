/*
страница доступна только авторизованным и активным пользователям
наполнять таблицу
пагирировать по данным
запись данных
построение дашборда на рил данных
фильтрация
переход по страницам
копировать
удалить
скачать
изменени данных по клику на элемент
Логотип Finance Planner
Дизайн подшаманить
*/

function get_user_id(){
  user_id_div = document.getElementById('user_id')
  return user_id_div.textContent
}


function get_token(){
    token = document.getElementById('csrf_token').innerHTML
    return token
}

function filter_table(start=null, end=null){

}

function create_table(incomes){

  table_body = document.getElementById('table_body')
  for(i=0; i<incomes.items.length; ++i){
    income = incomes.items[i]
    var income_id = income.id
    var name = income.name
    var date = income.date
    var amount = income.amount
    var done = income.done
    var tr = document.createElement("tr");
    tr.className = 'd-flex'
    tr.id = income_id
    tr.innerHTML = '<tr>'+
            '<td class="col-3 text-left">'+name+'</td>' +
            '<td class="col-2 text-left">'+date+'</td>' +
            '<td class="col-3 text-left">'+amount+'</td>' +
            '<td class="col-1 text-right">'+done+'</td>' +
            '<td class="col-2 ">'+
              '<div class="row">'+
                '<div class="col text-right"><input class="form-check-input" name="get" type="checkbox" ></div>'+
              '</div>'+
            '</td>'+
          '</tr>'
    table_body.prepend(tr)
    create_events_on_click()
  }
}

function get_income_for_table(user_id, page=null){
  if(page==null){
    page = 1
  }

  data = $.ajax({
    url: '/income/get/bulk',         
    method: 'GET',             
    dataType: 'json',
    headers: {'X-CSRFToken':get_token()},
    data: {
        'page': page,
        'user_id': user_id
      },
    success: function(data){
      create_table(data)
    }
  });
}

function get_first_laste_date_this_month(){
  var date = new Date();
  var firstDay = new Date(date.getFullYear(), date.getMonth(), 1);
  var lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0);
  firstDay = firstDay.toISOString().split('T')[0]
  lastDay = lastDay.toISOString().split('T')[0]
  return [firstDay, lastDay]
}

function set_data_for_dashboard(start=null, end=null){
  dates = get_first_laste_date_this_month()
  if(!start){
    start=dates[0]
  }
  if(!end){
    end=dates[1]
  }
  get_incomes(start, end)

}
function get_incomes(start, end){
    $.ajax({
        url: '/reporter/get_income',         
        method: 'POST',             
        dataType: 'json',
        headers: {'X-CSRFToken':get_token()},
        data: {
            'user_id': get_user_id(),
            'start_period': start,
            'end_period': end
        },
        success: function(data){
          get_expenses(data, start, end)
        }
    });
}

function get_expenses(incomes, start, end){
    $.ajax({
        url: '/reporter/get_expense',         
        method: 'POST',             
        dataType: 'json',
        headers: {'X-CSRFToken':get_token()},
        data: {
            'user_id': get_user_id(),
            'start_period': start,
            'end_period': end
        },
        success: function(data){
          data = {'incomes': incomes, 'expense': data}
        create_dashbord(data)
        }
    });
}

function income_add(name, amount, date, done){
  $.ajax({
      url: '/income/create/',         
      method: 'POST',             
      dataType: 'json',
      headers: {'X-CSRFToken':get_token()},
      data: {
          'user_id': get_user_id(),
          'date': date,
          'name': name,
          'amount':amount,
          'done':done,
      },
      success: function(data){
        to_add_in_table = {items:[data]}
        create_table(to_add_in_table)
        set_data_for_dashboard()
        /*фильтровать таблицу*/
        /*фильтровать дашборд */
      }
  });
}

function income_delete_bulk(items){
  
  items_int = [] 
  for(i=0;i<items.length;i++){
    items_int.push(Number(items[i]))
  }
  user_id = get_user_id()
  data = {
    "user_id": user_id,
    "items": items_int,
  }
  console.log(items_int)
  $.ajax({
      url: '/income/delete/bulk/',         
      method: 'DELETE',             
      dataType: 'application/json',
      headers: {'X-CSRFToken':get_token()},
      data: data,
      success: function(data){
        get_income_for_table()
        set_data_for_dashboard()
        create_events_on_click()
      }
  });
}


function create_dashbord(data){

    canvas_el = document.getElementById('chart')
    canvas_el.remove()
    
    conteiner_chart = document.getElementById('conteiner_chart')
    conteiner_chart.append(canvas_el)

    const ctx = canvas_el.getContext('2d');
    incomes = data.incomes.incomes
    expense = data.expense.expenses

    all_elemts = [expense, incomes]
    
    expenses_amount_list = []
    for(i=0; i < expense.length;i++){
      ex = expense[i]
      amount = ex[1]
      expenses_amount_list.push(amount)
    }

    incomes_amount_list = []
    for(i=0; i < incomes.length;i++){
      ex = incomes[i]
      amount = ex[1]
      incomes_amount_list.push(amount)
    }
    dts = []
    for(z=0; z<all_elemts.length;z++){
      el = all_elemts[z]
      for(i=0; i<el.length;i++){
        e = el[i]
        for(q=0;q<e.length;q++){
          date = e[0]
        dts.push(date)
        }        
      }
    }
    dts = Array.from(new Set(dts))

    const myChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: dts,
          datasets: [{
            label: 'Доходы',
            backgroundColor: '#324512',
            borderColor: 'rgb(47, 128, 237)',
            data: incomes_amount_list,
          },{
              label: 'Расходы',
              backgroundColor: '#deb99b',
              borderColor: 'rgb(47, 128, 237)',
              data: expenses_amount_list,
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


function _any_checkbox_checked(checkboxes){
  for(i=0; i < all_checkbox.length; i++){
    if(all_checkbox[i].checked){return true};
  }
  return false;
}

function add_action_for_all_checkboxes(all_checkbox){
  for(i=0; i<all_checkbox.length; i++){
    checkbox_element = all_checkbox[i].addEventListener('change', function() {
      need_show = _any_checkbox_checked(all_checkbox)
      if(need_show){
        button_delete.style.display = 'block';
        button_copy.style.display = 'block';
      }else{
        button_delete.style.display = 'none';
        button_copy.style.display = 'none';
      };})
  }
}

function create_events_on_click(){

  /*add*/
  document.getElementById('button_add').onclick = function(e){
    name_i = document.getElementById('add_name_income')
    date = document.getElementById('add_date_income')
    amount = document.getElementById('add_amount_income')
    done = document.getElementById('add_done_income')

    name_value = name_i.value
    date_value = date.value
    amount_value = amount.value
    done_value = done.selectedOptions[0].value


    document.getElementById('button_exit').click();
    /*
    прочитать данные с формы
    валидировать
    отправить
    получить
    внести в таблицу(на странице 10 элементов, последний добавленный вверх таблицы вставлять, последний удалять из таблицы)
    */
    income_add(name_value, amount_value, date_value, done_value);
    name_i.value = ""
    date.value = ""
    amount.value = ""
    done.value = ""
    set_data_for_dashboard()
  }
  /*события выбора чебокса*/
  get_all = document.getElementById('get_all')
  all_checkbox = document.getElementsByName('get')
  add_action_for_all_checkboxes(all_checkbox)
  button_delete = document.getElementById('button_delete')
  button_copy = document.getElementById('button_copy')
  get_all.addEventListener('change', function() {
    if (this.checked) {
      for(i=0; i<all_checkbox.length;i++){
        all_checkbox[i].checked = true
      };
      button_delete.style.display = 'block';
      button_copy.style.display = 'block';
    } else {
      for(i=0; i<all_checkbox.length;i++){
        all_checkbox[i].checked = false
      };
      button_delete.style.display = 'none';
      button_copy.style.display = 'none';
    }
  });

  button_delete.onclick = function(e){
    items = []
    checked_checkbox = []
    for(i=0; i<all_checkbox.length;i++){
      if(all_checkbox[i].checked){
        checked_checkbox.push(all_checkbox[i])
    };
    
    /*собрать все чекбоксы, которые выбраны  */
    };
    for(i=0;i<checked_checkbox.length;i++){
      el = checked_checkbox[i]
      items.push(el.parentNode.parentNode.parentNode.parentNode.id)
      console.log(el.parentNode.parentNode.parentNode.parentNode.id)
      
    };
    income_delete_bulk(items)
  }

  /*при нажатии на ячейкку переходить к редактированию(сохранение по ентер или клику на другое место)
    при нажатии на другую ячейку закрыть редактирование здесь и открыть ту ячейку, которую нажали
  */

}

/*PUBLIC*/
window.addEventListener('load', function () {
  create_events_on_click()
  get_income_for_table(get_user_id())
  set_data_for_dashboard()

})

