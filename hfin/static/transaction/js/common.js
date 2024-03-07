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
  
  function apply_names_for_filter(){
      data = $.ajax({
          url: '/expense/get_name_list/',//nen
          method: 'GET',
          dataType: 'json',
          headers: {
              'X-CSRFToken': get_token()
          },
          data: {
              'user_id': get_user_id()
          },
          success: function(data) {
              set_name_list(data.names)
          }
      });
  
  }
  
  function set_name_list(names){
      selecter = document.getElementsByClassName('name-filter-custom')[0]
      for(i=selecter.children.length-1; i >= 0; i--){
          if(selecter.children[i].textContent != '...'){
              selecter.removeChild(selecter.children[i])
          }
      }
      
      for(i in names){
          option_element = document.createElement('option')
          option_element.textContent = names[i]
          option_element.setAttribute('value', i)
          selecter.append(option_element)
      }

    select_options = document.getElementsByClassName('form-multi-select-options')[0]
    for(i=select_options.children.length-1; i >= 0; i--){
    if(select_options.children[i].textContent != '...'){
        select_options.removeChild(select_options.children[i])
    }
    }
    for(i in names){
        select_opt = document.createElement('div')
        select_opt.className = 'form-multi-select-option form-multi-select-option-with-checkbox'
        select_opt.setAttribute('data-value', i)
        select_opt.setAttribute('tabindex', i)
        select_opt.textContent = names[i]
        select_options.append(select_opt)

    }  
  }
  function set_page(page, page_link_obj){
      
      
      old_parent_page_link_obj = document.getElementsByClassName('page-item active')[0]
      old_parent_page_link_obj.className = 'page-item'
      span_obj = old_parent_page_link_obj.children[0]
      ahref = document.createElement('a')
      ahref.href = '#'
      ahref.textContent = span_obj.textContent
      ahref.className = 'page-link'
      ahref.addEventListener('click', function(e){
          set_page(e.target.textContent, e.target)
      })
      old_parent_page_link_obj.appendChild(ahref)
      old_parent_page_link_obj.removeChild(span_obj)
  
      page_link_obj.parentElement.className = 'page-item active'
      start_period = document.getElementById('start-filter').value
      end_period = document.getElementById('end-filter').value
      name_income = document.getElementById('name-filter').selectedOptions[0].textContent
      if(start_period == ''){
          start_period = '1000-01-01'
      }
      if(end_period == ''){
          end_period = '3000-01-01'
      }
      if(name_income == '...'){
          name_income = null
      }
  
  
      get_transaction_for_table(
          page = page,
          start_date=start_period,
          end_date=end_period,
          name=name_income,
          pag_need_update=true
      )
  }
  
  function _generate_pagination_menu(data, start_page=1){
      
      page_count = data.count
      pag_menu = document.getElementById('pag_menu')
      lenth_menu = pag_menu.children.length
      for(i=lenth_menu-1;i>=0;i--){
          pag_menu.removeChild(pag_menu.children[i])
      }
      count_preview = 3
      need_pag_next_preview = (page_count > count_preview) && (start_page < (page_count-count_preview))
      nexstartpagebase = 0
  
      if(start_page>=count_preview){
          li = document.createElement('li')
          li.className = 'page-item'
  
          ahref_next = document.createElement('a')
          ahref_next.className = 'page-link'
          ahref_next.id = 'pag_prev_preview'
          ahref_next.setAttribute('new_start_page',i)
          ahref_next.textContent = '...'
          li.appendChild(ahref_next)
          pag_menu.prepend(li)
          
      }
  
      pag_prev_preview = document.getElementById('pag_prev_preview')
      if(pag_prev_preview){
          pag_prev_preview.addEventListener(
              'click',
              function(e){
                  if(start_page == 1){
                      page = 1
                  }else{
                      page = start_page - 3
                  }
                  get_transaction_for_table(page=page)
                  _generate_pagination_menu(data, page)
              }
          )
      }
      
      for(i=start_page;i<=page_count;i++){
          
          if(count_preview==0 && i < page_count){
              break
          }
          
          if(count_preview >0 || i == page_count){
              if(start_page==i){
                  first_li = document.createElement('li')
                  first_li.className = 'page-item active'
                  first_li.setAttribute('aria-current', 'page')
                  
                  span = document.createElement('span')
                  span.className = 'page-link'
                  span.textContent = i
  
                  first_li.appendChild(span)
                  pag_menu.appendChild(first_li)
                  count_preview -=1
                  continue
              }else{
                  li = document.createElement('li')
                  li.className = 'page-item'
  
                  ahref = document.createElement('a')
                  ahref.className = 'page-link'
                  ahref.href = '#'
                  ahref.textContent = i
                  li.appendChild(ahref)
                  pag_menu.appendChild(li)
                  count_preview -=1
                  nexstartpagebase = i+1
              }
          }
      }
  
      if(need_pag_next_preview){
          li = document.createElement('li')
          li.className = 'page-item'
  
          ahref_next = document.createElement('a')
          ahref_next.className = 'page-link'
          ahref_next.id = 'pag_next_preview'
          ahref_next.setAttribute('new_start_page',i)
          ahref_next.textContent = '...'
          li.appendChild(ahref_next)
          pag_menu.appendChild(li)
          
          li = document.createElement('li')
          li.className = 'page-item'
  
          ahref = document.createElement('a')
          ahref.className = 'page-link'
          ahref.href = '#'
          ahref.textContent = page_count
          li.appendChild(ahref)
          pag_menu.appendChild(li)
      }
  
      pag_next_preview = document.getElementById('pag_next_preview')
      if(pag_next_preview){
          pag_next_preview.addEventListener(
              'click',
              function(e){
                  get_transaction_for_table(page=nexstartpagebase)
                  _generate_pagination_menu(data, nexstartpagebase)
              }
          )
      }
  
      page_links = document.getElementsByClassName('page-link')
      for(i=0; i < page_links.length; i++){
          page_link = page_links[i]
          if(page_link.textContent != '...' && page_link.parentElement.className != 'page-item active'){
              page_link.addEventListener('click', function(e){
                  set_page(e.target.textContent, e.target)
              })
          }
          
      }
      
  }
  
  function get_sec_page(filter_data = null){
      if(!filter_data){
          filter_data = {
              'user_id': get_user_id()
          }
      }
      data = $.ajax({
          url: '/transaction/get_count_for_paggination/',
          method: 'GET',
          dataType: 'json',
          headers: {
              'X-CSRFToken': get_token()
          },
          data: filter_data,
          success: function(data) {
              _generate_pagination_menu(data)
          }
      });
  }
  
  function get_token() {
    token = document.getElementById('csrf_token').innerHTML
    return token
  }
  
  function update_sec_pag(){
  
      start_period = document.getElementById('start-filter').value
      end_period = document.getElementById('end-filter').value
      name_income = document.getElementById('name-filter').selectedOptions[0].textContent
      if(start_period == ''){
          start_period = '1000-01-01'
      }
      if(end_period == ''){
          end_period = '3000-01-01'
      }
      if(name_income == '...'){
          name_income = null
      }
  
      if(page == null){
          page=1
      }
  
      params = {
          'page': page,
          'start_date': start_date,
          'end_date': end_date,
          'target_name': name_income,
          'user_id': get_user_id()
        }
      
        request_data = {}
      
        for(i in params){
          if(params[i]){
              request_data[i] = params[i]
          }
        }
  
      get_sec_page(filter_data=request_data)
  }
  
  function filter_table(start_period, end_period, name_income, target_name) {
      if(start_period == ''){
          start_period = '1000-01-01'
      }
      if(end_period == ''){
          end_period = '3000-01-01'
      }
      if(name_income == '...'){
          name_income = null
      }
      if(target_name == '...'){
        target_name = null
    }
      
      set_data_for_dashboard(start=start_period, end=end_period)
      
      get_transaction_for_table(
          page = null,
          start_date=start_period,
          end_date=end_period,
          name=name_income,
          target_name=target_name,
          pag_need_update=true
      )
  
      //update_sec_pag()
      
      if(page == null){
          page=1
      }
  
      params = {
          'page': page,
          'start_date': start_date,
          'end_date': end_date,
          'target_name': name_income,
          'name': name,
          'user_id': get_user_id()
        }
      
        request_data = {}
      
        for(i in params){
          if(params[i]){
              request_data[i] = params[i]
          }
        }
  
      get_sec_page(filter_data=request_data)
  
  }
  
  function create_table(transaction_items, update_all = null) {
  
    this_tabel = document.getElementById('the_table')
    table_body = document.getElementById('table_body')
  
    if (update_all) {
  
        children = table_body.children
        steps = children.length
        if(children.length>0){
          for (i = steps-1; i >=0 ; i--){
              table_body.removeChild(children[i])
          }
        }
  
    }
    for (i = 0; i < transaction_items.items.length; i++) {
        transaction = transaction_items.items[i]
        var transaction_id = transaction.id
        var name = transaction.name
        var target_name = transaction.target_name
        var date = transaction.date
        var amount = transaction.amount
        var tr = document.createElement("tr");
        tr.className = 'd-flex'
        tr.id = transaction_id
        tr.innerHTML = '<tr>' +
            '<td class="col-3 text-left" id="td_text" >' + name + '</td>' +
            '<td class="col-3 text-left" id="td_text" >' + target_name + '</td>' +
            '<td class="col-2 text-left" id="td_date" >' + date.split('T')[0] + '</td>' +
            '<td class="col-3 text-left" id="td_number" >' + amount + '</td>' +
            '<td class="col-2" id="td_get">' +
            '<div class="row">' +
            '<div class="col text-right"><input class="form-check-input" name="get" type="checkbox" ></div>' +
            '</div>' +
            '</td>' +
            '</tr>'
        table_body.prepend(tr)
    }
    create_events_on_click()
  }
  
  
  function get_transaction_for_table(
      page = null,
      start_date = null,
      end_date = null,
      name = null,
      target_name,
      pag_need_update = false
      ) {
  
    params = {
      'page': page,
      'start_date': start_date,
      'end_date': end_date,
      'target_name': target_name,
      'name': name,
      'user_id': get_user_id()
    }
  
    request_data = {}
  
    for(i in params){
      if(params[i]){
          request_data[i] = params[i]
      }
    }
  
    if (page == null) {
      request_data['page'] = 1
    }
  
    data = $.ajax({
        url: '/transaction/get/bulk',
        method: 'GET',
        dataType: 'json',
        headers: {
            'X-CSRFToken': get_token()
        },
        data: request_data,
        success: function(data) {
          create_table(data, update_all= true)
        }
    });
  }
  
  function get_first_laste_date_this_month() {
    var date = new Date();
    var firstDay = new Date(date.getFullYear(), date.getMonth(), 1);
    var lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0, 23, 59, 59);
    UTC_CODE  = date.getTimezoneOffset() * (-1) / 60
    firstDay = firstDay.toISOString().split('T')[0]
    lastDay = lastDay.toISOString().split('T')[0]
    return [firstDay, lastDay]
  }
  
  function set_data_for_dashboard(start = null, end = null) {
    dates = get_first_laste_date_this_month()
      if (!start) {
          start = dates[0]
      }
      if (!end) {
          end = dates[1]
      }
    get_transaction(start, end)
  
  }
  
  function get_transaction(start, end) {
    $.ajax({
        url: '/reporter/get_transaction',
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
            get_incomes(data, start, end)
        }
    });
  }
  
  function get_incomes(transaction, start, end) {
    $.ajax({
        url: '/reporter/get_transaction',
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
                'transaction': transaction,
                'incomes': data
            }
            create_dashbord(data)
        }
    });
  }
  
  function income_add(name, amount, date, target_name) {
    $.ajax({
        url: '/transaction/create/',
        method: 'POST',
        dataType: 'json',
        headers: {
            'X-CSRFToken': get_token()
        },
        data: {
            'user_id': get_user_id(),
            'date': date,
            'target_name': target_name,
            'name': name,
            'amount': amount
        },
        success: function(data) {
            to_add_in_table = {
                items: [data]
            }
            create_table(to_add_in_table)
            set_data_for_dashboard()
        }
    });
  }
  
  function income_delete_bulk(items) {
    /* либо забрать из фильтра*/
    dates = get_first_laste_date_this_month()
    start = dates[0]
    end = dates[1]
    items_int = []
    for (i = 0; i < items.length; i++) {
        items_int.push(Number(items[i]))
    }
    user_id = get_user_id()
    data = {
        "user_id": user_id,
        "items": JSON.stringify(items_int),
    }
    $.ajax({
        url: '/transaction/delete/bulk/',
        method: 'DELETE',
        dataType: 'json',
        headers: {
            'X-CSRFToken': get_token()
        },
        data: data,
        success: function(data) {
            create_table(transaction = data, update_all = true);
            set_data_for_dashboard(start, end);
            create_events_on_click();
        }
    });
  }
  
  function with_preprocess_update(income, update_field, new_value){
    if(new_value =='Да'){
      new_value=true
    }
    if(new_value =='Нет'){
      new_value=false
    }
    data = {
      "id": income.id,
      "user_id": get_user_id(),
      "name": income.name,
      "date": income.date,
      "amount": income.amount
    }
    data[update_field] = new_value
    income_update(income_data=data)
  }
  
  
  function income_update( income_data) {
    /* либо забрать из фильтра*/
    dates = get_first_laste_date_this_month()
    start = dates[0]
    end = dates[1]
    $.ajax({
        url: '/transaction/update/',
        method: 'PATCH',
        dataType: 'json',
        headers: {
            'X-CSRFToken': get_token()
        },
        data: income_data,
        success: function(data) {
            set_data_for_dashboard(start, end);
            apply_names_for_filter()
        }
    });
  }
  
  function income_copy_bulk(items) {
    /* либо забрать из фильтра*/
    dates = get_first_laste_date_this_month()
    start = dates[0]
    end = dates[1]
    items_int = []
    for (i = 0; i < items.length; i++) {
        items_int.push(Number(items[i]))
    }
    user_id = get_user_id()
    data = {
        "user_id": user_id,
        "items": JSON.stringify(items_int),
    }
    $.ajax({
        url: '/transaction/copy/bulk/',
        method: 'POST',
        dataType: 'json',
        headers: {
            'X-CSRFToken': get_token()
        },
        data: data,
        success: function(data) {
            create_table(transaction = data, update_all = true);
            set_data_for_dashboard(start, end);
            create_events_on_click();
        }
    });
  }
  
  
  function create_dashbord(data) {
  
    // canvas_el = document.getElementById('chart')
    // canvas_el.remove()
    // canvas_el_new = document.createElement('canvas')
    // canvas_el_new.style.width = '600px'
    // canvas_el_new.style.height = '300px'
    // canvas_el_new.id = 'chart'
  
    // conteiner_chart = document.getElementById('conteiner_chart')
    // conteiner_chart.append(canvas_el_new)
  
    // const ctx = canvas_el_new.getContext('2d');
      
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
    //             data: transaction_amount_list,
    //         }]
    //     },
    //     options: {
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
  
  
  function _any_checkbox_checked(checkboxes) {
    for (i = 0; i < all_checkbox.length; i++) {
        if (all_checkbox[i].checked) {
            return true
        };
    }
    return false;
  }
  
  function add_action_for_all_checkboxes(all_checkbox) {
    for (i = 0; i < all_checkbox.length; i++) {
        checkbox_element = all_checkbox[i].addEventListener('change', function() {
            need_show = _any_checkbox_checked(all_checkbox)
            if (need_show) {
                button_delete.style.display = 'block';
                button_copy.style.display = 'block';
            } else {
                button_delete.style.display = 'none';
                button_copy.style.display = 'none';
            };
        })
    }
  }
  
  function set_event_button_filter(){
      button_filter = document.getElementById('button-filter')
      button_filter.addEventListener(
          'click',
          function(e){
              start_period = document.getElementById('start-filter').value
              end_period = document.getElementById('end-filter').value
              name_income = document.getElementById('name-filter').selectedOptions[0].textContent

              filter_table(
                  start_period,
                  end_period,
                  name_income,

              )
          }
      )
  }
  
  function create_events_on_click() {
  
    all_td_to_click = []
    all_td = document.getElementsByTagName('td')
    for (i = 0; i < all_td.length; i++) {
        if (all_td[i].id != 'td_get') {
            all_td_to_click.push(all_td[i])
        }
  
    }
  
    function _get_input_by_type(element_type_input) {
  
        if (element_type_input == 'td_text') {
            input_obj = document.createElement('input')
            input_obj.className = 'form-control'
            input_obj.type = 'text'
        }
  
        if (element_type_input == 'td_date') {
            input_obj = document.createElement('input')
            input_obj.className = 'form-control'
            input_obj.type = 'date'
        }
  
        if (element_type_input == 'td_number') {
            input_obj = document.createElement('input')
            input_obj.className = 'form-control'
            input_obj.type = 'number'
        }
  
        if (element_type_input == 'td_selector') {
            input_obj = document.createElement('select')
            input_obj.className = 'form-select text-right'
            op_1 = document.createElement('option')
            op_1.innerHTML = 'Да'
            input_obj_op_1 = input_obj.appendChild(op_1)
  
            op_2 = document.createElement('option')
            op_2.innerHTML = 'Нет'
            input_obj_op_2 = input_obj.appendChild(op_2)
  
        }
  
        return input_obj
    }
  
    for (i = 0; i < all_td_to_click.length; i++) {
        all_td_to_click[i].addEventListener('click', function(e) {
            id_name = "input_update"
            input_obj_already_exists = document.getElementById(id_name)
            if (input_obj_already_exists) {
                return
            }
            td_elemnt = e.target
            input_obj = _get_input_by_type(td_elemnt.id)
  
            input_obj.id = id_name
            old_value = td_elemnt.textContent
            td_elemnt.innerHTML = ""
  
            td_elemnt.appendChild(input_obj)
  
  
            input_obj.focus()
            input_obj.value = old_value
            $(document).keyup(function(e) {
              if(e.keyCode == 13){
                new_value = input_obj.value
                var container = $("#input_update");
                if ((new_value.length > 0) && (new_value != old_value)) {
                    parent = input_obj.parentElement.parentElement
                    
                    update_field = input_obj.type
                    if(update_field == 'date'){
                      update_field = 'date'
                    }
                    if(update_field == 'number'){
                      update_field = 'amount'
                    }
                    if(update_field == 'text'){
                      update_field = 'target_name'
                    }
                    td_elemnt.textContent = new_value
                    with_preprocess_update(parent, update_field, new_value)
                    $(document).off('keyup')
                    $(document).off('mouseup')
  
  
                } else {
                    td_elemnt.textContent = old_value
                    $(document).off('keyup')
                    $(document).off('mouseup')
                }
              }
              
            })
            $(document).mouseup(function(e) {
                var container = $("#input_update");
                if (container.has(e.target).length == 0) {
  
                    if (container.length > 0) {
                        if (e.target.id == container[0].id) {
                            return
                        }
                    }
                    if (container[0] != td_elemnt) {
                        new_value = input_obj.value
  
                        if ((new_value.length > 0) && (new_value != old_value)) {
                            parent = input_obj.parentElement.parentElement
                            
  
                            td_elemnt.textContent = new_value
                            update_field = input_obj.type
                            if(update_field == 'date'){
                              update_field = 'date'
                            }
                            if(update_field == 'number'){
                              update_field = 'amount'
                            }
                            if(update_field == 'text'){
                              update_field = 'target_name'
                            }
                            td_elemnt.textContent = new_value
                            with_preprocess_update(parent, update_field, new_value)
  
  
                        } else {
                            td_elemnt.textContent = old_value
                        }
                    }
  
                }
                $(document).off('mouseup')
                $(document).off('keyup')
            });
        })
    }
  
    document.getElementById('button_add').onclick = function(e) {
        name_i = document.getElementById('add_name_transaction')
        date = document.getElementById('add_date_transaction')
        amount = document.getElementById('add_amount_transaction')
        target_name = document.getElementById('add_target_name_transaction')
  
        name_value = name_i.value
        date_value = date.value
        amount_value = amount.value
        target_name_value = target_name.value
  
  
        document.getElementById('button_exit').click();
        
        income_add(name_value, amount_value, date_value, target_name_value);
        name_i.value = ""
        date.value = ""
        amount.value = ""
        target_name.value = ""
        set_data_for_dashboard()
    }
    get_all = document.getElementById('get_all')
    all_checkbox = document.getElementsByName('get')
    add_action_for_all_checkboxes(all_checkbox)
    button_delete = document.getElementById('button_delete')
    button_copy = document.getElementById('button_copy')
    get_all.addEventListener('change', function() {
        if (this.checked) {
            for (i = 0; i < all_checkbox.length; i++) {
                all_checkbox[i].checked = true
            };
            button_delete.style.display = 'block';
            button_copy.style.display = 'block';
        } else {
            for (i = 0; i < all_checkbox.length; i++) {
                all_checkbox[i].checked = false
            };
            button_delete.style.display = 'none';
            button_copy.style.display = 'none';
        }
    });
  
    button_delete.onclick = function(e) {
        items = []
        to_delete = []
        checked_checkbox = []
        for (i = 0; i < all_checkbox.length; i++) {
            if (all_checkbox[i].checked) {
                checked_checkbox.push(all_checkbox[i])
            };
        };
        for (i = 0; i < checked_checkbox.length; i++) {
            el = checked_checkbox[i]
            items.push(el.parentNode.parentNode.parentNode.parentNode.id)
            to_delete.push(el.parentNode.parentNode.parentNode.parentNode)
        };
        income_delete_bulk(items)
  
        for (i = 0; i < to_delete.length; i++) {
            to_delete[i].remove()
        }
        button_delete.style.display = 'none';
        button_copy.style.display = 'none';
    }
  
    button_copy.onclick = function(e) {
        items = []
        checked_checkbox = []
        for (i = 0; i < all_checkbox.length; i++) {
            if (all_checkbox[i].checked) {
                checked_checkbox.push(all_checkbox[i])
            };
  
        };
        for (i = 0; i < checked_checkbox.length; i++) {
            el = checked_checkbox[i]
            items.push(el.parentNode.parentNode.parentNode.parentNode.id)
        };
        income_copy_bulk(items)
  
        button_delete.style.display = 'none';
        button_copy.style.display = 'none';
    }
  }
  
  /*PUBLIC*/
  window.addEventListener('load', function() {
      apply_names_for_filter()
      get_sec_page()
      create_events_on_click()
      get_transaction_for_table()
      set_data_for_dashboard()
      set_event_button_filter()
  })