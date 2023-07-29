$(document).ready(function() {
    $("tbody").sortable({
     update: function(event, ui) {
        sort =[];
        window.CSRF_TOKEN = "{{ csrf_token }}";
        $("tbody").children().each(function(){
            sort.push({'pk':$(this).data('pk'),'order':$(this).index()})

    });

    $.ajax({
      url: "{% url 'task-sorting' %}",
      type: "post",
      datatype:'json',
      data:{'sort':JSON.stringify(sort),
       'csrfmiddlewaretoken': window.CSRF_TOKEN
      },

    });
     console.log(sort)
      },
    }).disableSelection();
  });