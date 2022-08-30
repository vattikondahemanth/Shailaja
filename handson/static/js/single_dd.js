


$(document).ready(function () {


const container = document.getElementById('example');
const hot = new Handsontable(container, {
          data: data,
          rowHeaders: true,
          fixedRowsTop: 0,
          colwidths:200,
          colHeaders: ['ID','Name','Salary'],
          cells(row, col) {
            const cellPrp = {};

            if (row === 0) {
              cellPrp.renderer = mySearchBox;
              cellPrp.readOnly = true;
            }

            return cellPrp
          },
          columns:[
          {data:'fields.id'},
          {data:'fields.name'},
          {data:'fields.salary'}],
          height: 500,
          width: 500,
          dropdownMenu: true,
          filters: true,
          strechHall: true,
          licenseKey: 'non-commercial-and-evaluation'
        });
Handsontable.hooks.add('afterScrollVertically', hookgetdata);
bind_search_events();
column_ddl_mapper = {
    "0" : "name",
    "1": "salary",
    "2": "",
    "3": "",
    "4": "",
    "5": "",


}
var ddlcount = 0;
var prev_ScrollTop = 0;

function dropdown_html(list_values, drp_num){
    var ddlopt = "";
    if(list_values){

        for (var i = 0; i < list_values.length; i++) {

            ddlopt += "<option value=" + list_values[i] + ">" + column_ddl_mapper[drp_num] + ": " +  list_values[i] + "  </option>"
        }
    }
    return ddlopt;
}

function bind_drop_down_data(ddlopt){
        $(drop_down_id).prop('multiple', 'multiple');

        if($(drop_down_id).html().length > 0){
            $(drop_down_id).multiselect('rebuild');
            $(drop_down_id).html(ddlopt);
            $(drop_down_id).multiselect({enableFiltering: true,
         maxHeight: 250});
        }else{
            $(drop_down_id).html(ddlopt);
           $(drop_down_id).multiselect({enableFiltering: true,
         maxHeight: 250});
        }


}

var didScroll = false;

setInterval(function() {
    if ( didScroll ) {
        didScroll = false;
    }
}, 250);

function drop_down_scroll_event(){
    $('.dropdown-menu').on('scroll', function (event) {
            didScroll = true;
            // each element height - 34
            var total_num_elems = $('.multiselect-container').find('li').length; // 303
            var each_ele_height = $('.multiselect-container li:first-child').height(); // 34
            var scroll_height = $(this).scrollTop();  // 9470
            var cal_val = ((total_num_elems * each_ele_height * each_ele_height)/ 250);

//              if($(this).scrollTop() + $(this).innerHeight() >= $(this)[0].scrollHeight){
               if ($(this)[0].scrollHeight - $(this).scrollTop() === $(this)[0].clientHeight){

//            if(didScroll && (scroll_height > (each_ele_height * total_num_elems) - (cal_val))){
                $('.dropdown-menu').on('scroll', function(event){
                });
                prev_ScrollTop = $(this).scrollTop();
                SearchMain(true);
                 $(drop_down_id).multiselect('rebuild').multiselect({enableFiltering: true,
                    maxHeight: 250});
            }
         event.stopPropagation();
         });

}

function load_dynamic_dropdown_values(result, drop_down_scroll){
    var ddl_select = "<option>select</option>";
    var ddlopt = "";
    if (result) {
        for (var i = 0; i < result.length; i++) {
            for(var drp_num in result[i]){
                drop_down_id = "#dd";
                ddlopt += dropdown_html(result[i][drp_num], drp_num);
            }
            ddlcount += result[i][i].length;
        }
        ddl_select = ddl_select + ddlopt;
        bind_drop_down_data(ddlopt);

        if(!drop_down_scroll){
            drop_down_scroll_event();
        }
        else{
            setTimeout(function(){
                drop_down_scroll_event();
            }, 5000);
        }
    }
    else {
        alert("No data is present for this search");
    }



 }

function SearchMain(drop_down_scroll) {
                $.ajax(
                    {
                        type: "GET",
                        url: getall_ddl_data,
                        data:{
                          'search': $('#txtmainsearch').val(),
                          'ddlcount': ddlcount
                        },
                        success: function (result) {
                            load_dynamic_dropdown_values(result, drop_down_scroll)
                        },
                        error: function (result) {
                            alert("There are some error");
                        },
                    });
            }

function FullClear(){

    $("body").addClass("loading");
    $.each(column_ddl_mapper, function(index, value){
        if(value){
            drop_down_id = "#dd" + index;
            $(drop_down_id).html("");
            $(drop_down_id).multiselect('destroy').multiselect();
        }
    });

    $("#txtmainsearch").val("");

    hot.loadData([]);

    $('.search_values').html("")
}

function FullSearch(pageNo) {

        selected_elemets = $("#dd").parent().children('div').find('li.active')
        ddl0_values = [];
        if(selected_elemets){
            for(i=0; i < selected_elemets.length; i++){
                ddl0_values.push($.trim(selected_elemets[i].innerText));
            }
        }



                var resultSelected = {};
                resultSelected['0'] = ddl0_values;

                show_filter_values(resultSelected);

                $.ajax(
                    {
                        type: "GET",
                        url: get_hot_data,
                        data: { "hot_filter_values": JSON.stringify(resultSelected) },
                        success: function (result) {
                            if (result) {
                                hot.loadData(result)
                            }
                            else {
                                alert("There is no data");
                            }

                        },
                        error: function (result) {
                            alert("There are some error");
                        },
                    });
}

function show_filter_values(resultSelected){
    txt = "<ul class='list-group'>"

    $.each(resultSelected, function(index, value){
            $.each(value, function(sub_index, sub_value){
                if(value){
                    txt += "<li class='list-group-item'>" + sub_value  +  "</li>"
                }
        });

    });

    txt += "</ul>"

    $(".search_values").html(txt);
}
function bind_search_events(){
    $(document).off("click", "#btnmainsearch").on('click', '#btnmainsearch', function () {
                ddlcount = 0;
                SearchMain();
            });
    $(document).off("click", "#btnfullsearch").on('click', '#btnfullsearch', function () {
        FullSearch(1)

    });
    $(document).off("click", "#btnmainclear").on('click', '#btnmainclear', function () {
        FullClear()

    });

}
function hookgetdata(){
if (hot.getPlugin('autoRowSize').getLastVisibleRow() === hot.countRows() - 1) {
      scroll_getdata(hot.getPlugin('autoRowSize').getLastVisibleRow())
    }
}

function scroll_getdata(rowcount){
$.ajax({
      type:'GET',
      url:"{% url 'ajax_infinite' %}",
      data:{
         'rowcount':rowcount
      },
      success:function(response){
       hot.loadData(response)
       }
  });
}


function mySearchBox(instance, td, row, col, prop, value, cellProperties) {
  Handsontable.renderers.TextRenderer.apply(this, [instance, td, row, col, prop, value, cellProperties]);
  if(typeof value==='string'){
  value = value.replace('\"', "");
  }

  td.innerHTML = `<input class="hotSearch txt-${col}"  value="${value}" onkeyup="searchData(event)">`;
}
function searchData(event){
    var focus_txt = document.getElementsByClassName(event.target.className)[0].value;
    var emp_val= document.getElementsByClassName("hotSearch txt-1")[0].value;
    var salary_val= document.getElementsByClassName("hotSearch txt-2")[0].value;

    if ((focus_txt == null | focus_txt == "") & (event.key == 'Backspace')){
        load_data("")
    }
    if (emp_val.length >= 3 | salary_val.length >= 3){
        if (emp_val && salary_val){
            search_val = emp_val + "|" + salary_val
        } else if(emp_val){
            search_val = emp_val
        }
        else
        {
            search_val = salary_val
        }

        if(((focus_txt!= null) && (focus_txt.length >= 3))){
            load_data(search_val)
        }

    }
 }
function load_data(search_val){

    $.ajax({
          type:'GET',
          url:'http://localhost:8000/colsearch',
          dataType: "json",
          data:{
             'searchString':search_val
          },
          success:function(response){
           console.log("Success")
           hot.loadData(response)
           },
           error: function(response){
           console.log("Error")
           }
      });
}

  });