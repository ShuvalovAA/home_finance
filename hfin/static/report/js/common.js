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

// this is your saved/serialized config in a string
var serializedConfig = '{"rows":["name"], "cols":["month"],'+
                '"vals":["amount"],"aggregatorName":"Sum"}';

// deserialized it into an object
var deserializedConfig = JSON.parse(serializedConfig)

function create_dashbord(data) {
    $("#output").pivotUI(
        data,  {
          rows: ["name"],
          cols: ["year", 'month'],
          vals: ["amount"],
          aggregatorName: "Sum",
          rendererName: "Bar Chart",
          inclusions: {'type': ['расход']},
          renderers: $.extend(
            $.pivotUtilities.renderers, 
            $.pivotUtilities.plotly_renderers,
            deserializedConfig
          )
        });
  }

function create_dashbord_transaction(data) {
    $("#output_transation").pivotUI(
        data , {
          rows: ["name"],
          cols: ["year", 'month'],
          vals: ["amount"],
          aggregatorName: "Sum",
          rendererName: "Bar Chart",
          renderers: $.extend(
              $.pivotUtilities.renderers, 
            $.pivotUtilities.plotly_renderers
          )
        });
  }

  function create_dashbord_predict_day_of_year(data) {
    $("#output_predict_day_of_year").pivotUI(
        data , {
          rows: ["name"],
          cols: ["year", 'month'],
          vals: ["amount"],
          aggregatorName: "Sum",
          rendererName: "Bar Chart",
          renderers: $.extend(
              $.pivotUtilities.renderers, 
            $.pivotUtilities.plotly_renderers
          )
        });
  }

/*Дашборд */

function get_dataset(){
  //получить набор данных по расходам и доходам за соответствующий год
  $.ajax({
      url: '/reporter/get_years_dataset',
      method: 'GET',
      dataType: 'json',
      headers: {
          'X-CSRFToken': get_token()
      },
      data: {
          'user_id': get_user_id()
      },
      success: function(data) {
        create_dashbord(data)
      }
  });
}

function get_dataset_transaction(){
  //получить набор данных по транзакциям
  $.ajax({
      url: '/reporter/get_years_dataset_transaction',
      method: 'GET',
      dataType: 'json',
      headers: {
          'X-CSRFToken': get_token()
      },
      data: {
          'user_id': get_user_id()
      },
      success: function(data) {
        create_dashbord_transaction(data)
      }
  });
}

function get_predict_day_of_year(){
  //получить набор данных по предсказанию расходов на 2 года вперёд
  $.ajax({
      url: '/reporter/get_predict_day_of_year',
      method: 'GET',
      dataType: 'json',
      headers: {
          'X-CSRFToken': get_token()
      },
      data: {
          'user_id': get_user_id()
      },
      success: function(data) {
        create_dashbord_predict_day_of_year(data)
      }
  });
}

/*PUBLIC*/
window.addEventListener('load', function() {
  get_dataset()
  get_dataset_transaction()
  get_predict_day_of_year()
})