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
    //перейти на это

    //expaple tipsData = [['row', 'total_bill', 'tip', 'sex', 'smoker', 'day', 'time', 'size']['1', 16.99, 1.01, 'Female', 'No', 'Sun', 'Dinner', 2]['2', 10.34, 1.66, 'Male', 'No', 'Sun', 'Dinner', 3]]
    //need [['row','type','amount','date','name']['1','expense',100,2024-14-01,'связь']['2','income',90, 2024-14-01,'зп артём']]
    //$.pivotUtilities.tipsData
    $("#output").pivotUI(
        data , {
          rows: ["sex"],
          cols: ["smoker"],
          vals: ["tip", "total_bill"],
          aggregatorName: "Sum over Sum",
          rendererName: "Bar Chart",
          renderers: $.extend(
              $.pivotUtilities.renderers, 
            $.pivotUtilities.plotly_renderers
          )
        });
    //

    // canvas_el = document.getElementById('chart')
    // canvas_el.remove()
    // canvas_el_new = document.createElement('canvas')
    // canvas_el_new.style.width = '600px'
    // canvas_el_new.style.height = '300px'
    // canvas_el_new.id = 'chart'
  
    // conteiner_chart = document.getElementById('conteiner_chart')
    // conteiner_chart.append(canvas_el_new)
  
    // const ctx = canvas_el_new.getContext('2d');
    // incomes = data.incomes.incomes
    // expense = data.expense.expenses
    // incomes_dict = {}
    // for(i in incomes){
    //   incomes_dict[incomes[i][0]] = incomes[i][1]
    // }
  
    // expense_dict = {}
    // for(i in expense){
    //   expense_dict[expense[i][0]] = expense[i][1]
    // }
  
    // for(i in incomes_dict){
    //   expense_on_date = expense_dict[i]
    //   if(!expense_on_date){
    //       expense_dict[i] = 0
    //   }
    // }
    // for(i in expense_dict){
    //   income_on_date = incomes_dict[i]
    //   if(!income_on_date){
    //       incomes_dict[i] = 0
    //   }
    // }
  
    // sorted_keys_income = Object.keys(incomes_dict).sort()
    // income_dict_result = {}
    // for(i in sorted_keys_income){
    //   income_dict_result[sorted_keys_income[i]] = incomes_dict[sorted_keys_income[i]]
    // }
  
    // sorted_keys_expense = Object.keys(expense_dict).sort()
    // expense_dict_result = {}
    // for(i in sorted_keys_expense){
    //   expense_dict_result[sorted_keys_expense[i]] = expense_dict[sorted_keys_expense[i]]
    // }
  
    // dts = sorted_keys_expense
    // incomes_amount_list = Object.values(income_dict_result)
    // expenses_amount_list = Object.values(expense_dict_result)
  
  
    // const myChart = new Chart(ctx, {
    //     type: 'bar',
    //     data: {
    //         labels: dts,
    //         datasets: [{
    //             label: 'Доходы',
    //             backgroundColor: '#324512',
    //             borderColor: 'rgb(47, 128, 237)',
    //             data: incomes_amount_list,
    //         }, {
    //             label: 'Расходы',
    //             backgroundColor: '#deb99b',
    //             borderColor: 'rgb(47, 128, 237)',
    //             data: expenses_amount_list,
    //         }]
    //     },
    //     options: {
    //             title: {
    //                 display: true,
    //                 text: 'Информация на текущий месяц', 
    //                 color: 'dark',
    //                 font: {
    //                     weight: 'bold',
    //                     size: 24
    //                 }
    //             },
    //         scales: {
    //             yAxes: [{
    //                 ticks: {
    //                     beginAtZero: true,
    //                 }
    //             }]
    //         }
    //     },
    // });
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

function set_year_list(years){
  //установить список годов в кнопку
  div_options = document.getElementById('year_for_report')
  for(i=0; i < years.length; i++){
    year = years[i]
    opt = document.createElement('option')
    opt.textContent = year
    opt.value = year
    div_options.append(opt)
  }  
}

function get_years_list(){
//получилить список годов, которые есть в доходах и расходах
  $.ajax({
    url: '/reporter/get_years_list',
    method: 'GET',
    dataType: 'json',
    headers: {
        'X-CSRFToken': get_token()
    },
    data: {'user_id': get_user_id()},
    success: function(years) {
      set_year_list(years)
    }
  });  
}

function get_year_from_button(){
  //забрать год из кнопки
  button = document.getElementById('year_for_report')
  value = button.selectedOptions[0].value
  return value
}
function prepare_for_years_report(){
//подготовить всё для работы с отчётом за год
  year = get_year_from_button()
  if(!year){
    return
  }
  get_dataset(year)
}
function set_event_by_get_inc_exp_data(){
  //повесить событие клика на кнопку формирирования датасета
  button = document.getElementById('prepare_dataset')
  button.addEventListener('click', function(e){
    prepare_for_years_report()
  })

}
function get_dataset(year){
  //получить набор данных по расходам и доходам за соответствующий год
  $.ajax({
      url: '/reporter/get_years_dataset',
      method: 'GET',
      dataType: 'json',
      headers: {
          'X-CSRFToken': get_token()
      },
      data: {
          'user_id': get_user_id(),
          'year': year
      },
      success: function(data) {
        create_dashbord(data)
      }
  });
}

/*PUBLIC*/
window.addEventListener('load', function() {
  get_years_list()
  // set_data_for_dashboard()
  get_dataset(new Date().getFullYear())
  set_event_by_get_inc_exp_data()
})